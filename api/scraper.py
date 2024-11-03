import aiohttp
import asyncio
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
from dataclasses import dataclass
import logging
from urllib.parse import quote_plus
import re
from fake_useragent import UserAgent
from schemas import QueryRequest, SearchResult

@dataclass
class ScrapedContent:
    url: str
    title: str
    content: str
    snippet: str

class WebScraper:
    def __init__(self):
        self.ua = UserAgent()
        self.logger = logging.getLogger(__name__)
        self.session = None
        
        # Configure base URLs and parameters
        self.search_base_url = "https://www.google.com/search"
        self.max_results_per_query = 5
        self.concurrent_requests = 3  # Limit concurrent requests to avoid rate limiting
        
        # Rate limiting parameters
        self.request_delay = 2  # Delay between requests in seconds
        self.last_request_time = 0
        
    async def __aenter__(self):
        """Context manager entry for async with"""
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit for async with"""
        if self.session:
            await self.session.close()

    def _construct_search_query(self, question: str, organization: str) -> str:
        """Construct an effective search query combining question and organization"""
        # Remove special characters and normalize spaces
        cleaned_question = re.sub(r'[^\w\s]', ' ', question)
        cleaned_org = re.sub(r'[^\w\s]', ' ', organization)
        
        # Combine terms and encode for URL
        query = f"{cleaned_question} {cleaned_org} financial data report analysis"
        return quote_plus(query)

    async def _fetch_url(self, url: str) -> Optional[str]:
        """Fetch content from a URL with error handling and rate limiting"""
        headers = {
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
        }
        
        try:
            # Implement rate limiting
            current_time = asyncio.get_event_loop().time()
            time_since_last = current_time - self.last_request_time
            if time_since_last < self.request_delay:
                await asyncio.sleep(self.request_delay - time_since_last)
            
            async with self.session.get(url, headers=headers, timeout=30) as response:
                self.last_request_time = asyncio.get_event_loop().time()
                if response.status == 200:
                    return await response.text()
                else:
                    self.logger.warning(f"Failed to fetch {url}, status: {response.status}")
                    return None
                    
        except Exception as e:
            self.logger.error(f"Error fetching {url}: {str(e)}")
            return None

    def _extract_search_results(self, html_content: str) -> List[str]:
        """Extract URLs from Google search results"""
        soup = BeautifulSoup(html_content, 'html.parser')
        urls = []
        
        # Find all search result divs
        for result in soup.find_all('div', class_='g'):
            link = result.find('a', href=True)
            if link and 'href' in link.attrs:
                url = link['href']
                if url.startswith('http') and not any(x in url for x in ['google.com', 'youtube.com']):
                    urls.append(url)
                    
        return urls[:self.max_results_per_query]

    def _extract_content(self, html_content: str, url: str) -> Optional[ScrapedContent]:
        """Extract relevant content from a webpage"""
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Remove unwanted elements
            for element in soup.find_all(['script', 'style', 'nav', 'footer', 'header']):
                element.decompose()
            
            # Extract title
            title = soup.title.string if soup.title else ''
            
            # Extract main content
            main_content = []
            for paragraph in soup.find_all(['p', 'article', 'section']):
                text = paragraph.get_text(strip=True)
                if len(text) > 50:  # Filter out short snippets
                    main_content.append(text)
            
            if not main_content:
                return None
            
            # Combine content and create snippet
            content = ' '.join(main_content)
            snippet = ' '.join(main_content[:2])  # First two substantial paragraphs
            
            return ScrapedContent(
                url=url,
                title=title,
                content=content,
                snippet=snippet
            )
            
        except Exception as e:
            self.logger.error(f"Error extracting content from {url}: {str(e)}")
            return None

    async def _scrape_single_query(self, question: str, organization: str) -> List[SearchResult]:
        """Scrape results for a single question-organization pair"""
        query = self._construct_search_query(question, organization)
        search_url = f"{self.search_base_url}?q={query}"
        
        # Fetch search results
        search_html = await self._fetch_url(search_url)
        if not search_html:
            return []
        
        urls = self._extract_search_results(search_html)
        results = []
        
        # Fetch and process each URL
        async def process_url(url):
            html_content = await self._fetch_url(url)
            if html_content:
                content = self._extract_content(html_content, url)
                if content:
                    return SearchResult(
                        question=question,
                        organization=organization,
                        content=content.content,
                        url=url
                    )
            return None
        
        # Process URLs concurrently with rate limiting
        tasks = []
        for url in urls:
            task = asyncio.create_task(process_url(url))
            tasks.append(task)
            if len(tasks) >= self.concurrent_requests:
                completed = await asyncio.gather(*tasks)
                results.extend([r for r in completed if r])
                tasks = []
                
        if tasks:
            completed = await asyncio.gather(*tasks)
            results.extend([r for r in completed if r])
        
        return results

    async def scrape_matrix(self, questions: List[str], organizations: List[str]) -> List[SearchResult]:
        """Scrape data for all question-organization pairs"""
        async with self:  # Use context manager for session handling
            all_results = []
            
            # Create tasks for each question-organization pair
            tasks = []
            for question in questions:
                for org in organizations:
                    task = asyncio.create_task(
                        self._scrape_single_query(question, org)
                    )
                    tasks.append(task)
            
            # Execute all tasks and gather results
            results_lists = await asyncio.gather(*tasks)
            for result_list in results_lists:
                all_results.extend(result_list)
            
            return all_results

# # Example usage in /endpoints.py
# async def process_queries(request: QueryRequest):
#     scraper = WebScraper()
#     search_results = await scraper.scrape_matrix(
#         questions=request.questions,
#         organizations=request.organizations
#     )
    
#     # Process results with RAG...
#     return search_results




async def main():
    questions = ["What is the revenue growth?", "What is the gross income?"]
    organizations = ["Apple Inc", "Microsoft"]
    
    scraper = WebScraper()
    results = await scraper.scrape_matrix(questions, organizations)
    
    for result in results:
        print(f"Question: {result.question}")
        print(f"Organization: {result.organization}")
        print(f"URL: {result.url}")
        print(f"Content snippet: {result.content[:200]}...")
        print("---")

if __name__ == "__main__":
    asyncio.run(main())