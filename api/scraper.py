from datetime import datetime
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
import ssl
from enum import Enum

class ContentType(str, Enum):
    FINANCIAL_REPORT = 'financial_report'
    NEWS_ARTICLE = 'news_article'
    PRESS_RELEASE = 'press_release'
    REGULATORY_FILING = 'regulatory_filing'
    COMPANY_WEBSITE = 'company_website'
    OTHER = 'other'

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
        self.request_delay = 3  # Delay between requests in seconds
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
        """Construct a more targeted search query"""
        # Clean and prepare question
        cleaned_question = re.sub(r'[^\w\s]', ' ', question).lower()
        
        # Add specific keywords based on question type
        keywords = []
        if 'revenue' in cleaned_question:
            keywords.extend(['quarterly results', 'earnings report', 'financial results'])
        elif 'profit' in cleaned_question or 'margin' in cleaned_question:
            keywords.extend(['profit margin', 'earnings', 'financial performance'])
        elif 'growth' in cleaned_question:
            keywords.extend(['year over year', 'YoY', 'growth rate'])
            
        # Add time context
        keywords.append('2023 OR 2024')
        
        # Combine terms with organization and encode
        query = f"{organization} {' '.join(keywords)} {question} site:(.com OR .gov)"
        return quote_plus(query)
    
    def _determine_content_type(self, url: str) -> ContentType:
        """Determine content type based on URL patterns"""
        url_lower = url.lower()
        
        if any(x in url_lower for x in ['sec.gov', 'edgar']):
            return ContentType.REGULATORY_FILING
        elif any(x in url_lower for x in ['investor', 'earnings', 'financial-results']):
            return ContentType.FINANCIAL_REPORT
        elif any(x in url_lower for x in ['press', 'news', 'pr-']):
            return ContentType.PRESS_RELEASE
        elif any(x in url_lower for x in ['cnbc.com', 'reuters.com', 'bloomberg.com']):
            return ContentType.NEWS_ARTICLE
        elif any(x in url_lower for x in ['apple.com', 'microsoft.com']):
            return ContentType.COMPANY_WEBSITE
        else:
            return ContentType.OTHER

    async def _fetch_url(self, url: str) -> Optional[str]:
        """Enhanced fetch with retry logic"""
        if not self.session:
            self.session = aiohttp.ClientSession()
            
        headers = {
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        
        # Sites that typically block scraping
        blocked_domains = ['bloomberg.com', 'ft.com', 'wsj.com']
        if any(domain in url for domain in blocked_domains):
            return None
            
        retries = 3
        for attempt in range(retries):
            try:
                # Implement rate limiting
                current_time = asyncio.get_event_loop().time()
                time_since_last = current_time - self.last_request_time
                if time_since_last < self.request_delay:
                    await asyncio.sleep(self.request_delay - time_since_last)
                
                timeout = aiohttp.ClientTimeout(total=20)
                async with self.session.get(
                    url, 
                    headers=headers, 
                    timeout=timeout,
                    ssl=False,
                    allow_redirects=True
                ) as response:
                    self.last_request_time = asyncio.get_event_loop().time()
                    if response.status == 200:
                        return await response.text()
                    elif response.status == 403 or response.status == 429:
                        # If rate limited, wait longer before retry
                        await asyncio.sleep(5 * (attempt + 1))
                        continue
                    else:
                        self.logger.warning(f"Failed to fetch {url}, status: {response.status}")
                        return None
                        
            except Exception as e:
                self.logger.error(f"Attempt {attempt + 1} failed for {url}: {str(e)}")
                if attempt < retries - 1:
                    await asyncio.sleep(2 * (attempt + 1))
                continue
                
        return None

    def _extract_search_results(self, html_content: str) -> List[str]:
        """Extract URLs with better filtering"""
        soup = BeautifulSoup(html_content, 'html.parser')
        urls = []
        
        # Find all search result divs
        for result in soup.find_all('div', class_='g'):
            try:
                # Get the link
                link = result.find('a', href=True)
                if not link or not link['href'].startswith('http'):
                    continue
                    
                url = link['href']
                
                # Skip unwanted domains
                skip_domains = ['google.com', 'youtube.com', 'facebook.com', 'twitter.com']
                if any(domain in url for domain in skip_domains):
                    continue
                    
                # Prioritize financial and news websites
                priority_domains = ['ir.', 'investors.', 'reuters.com', 'seekingalpha.com', 'finance.yahoo.com']
                if any(domain in url for domain in priority_domains):
                    urls.insert(0, url)
                else:
                    urls.append(url)
                    
            except Exception as e:
                self.logger.error(f"Error extracting URL: {str(e)}")
                continue
                
        return urls[:self.max_results_per_query]

    def _extract_content(self, html_content: str, url: str) -> Optional[ScrapedContent]:
        """Enhanced content extraction"""
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Remove unwanted elements
            for element in soup.find_all(['script', 'style', 'nav', 'footer', 'header', 'aside']):
                element.decompose()
                
            # First try to find article or main content
            main_content = soup.find('article') or soup.find('main')
            if main_content:
                paragraphs = main_content.find_all(['p', 'h1', 'h2', 'h3', 'table'])
            else:
                paragraphs = soup.find_all(['p', 'h1', 'h2', 'h3', 'table'])
            
            # Extract title
            title = soup.title.string if soup.title else ''
            
            # Process paragraphs
            content_parts = []
            for p in paragraphs:
                text = p.get_text(strip=True)
                # Keep only substantial paragraphs
                if len(text) > 30 and not any(skip in text.lower() for skip in ['cookie', 'subscribe', 'privacy policy']):
                    content_parts.append(text)
            
            if not content_parts:
                return None
            
            # Join content with proper spacing
            content = ' '.join(content_parts)
            
            # Create a focused snippet
            snippet = ' '.join(content_parts[:3])  # First three substantial paragraphs
            
            return ScrapedContent(
                url=url,
                title=title,
                content=content[:8000],  # Limit content length
                snippet=snippet[:500]  # Limit snippet length
            )
            
        except Exception as e:
            self.logger.error(f"Error extracting content from {url}: {str(e)}")
            return None

    async def _scrape_single_query(self, question: str, organization: str) -> List[SearchResult]:
        """Scrape results for a single question-organization pair with enhanced error handling"""
        try:
            query = self._construct_search_query(question, organization)
            search_url = f"{self.search_base_url}?q={query}"
            
            # Fetch search results
            search_html = await self._fetch_url(search_url)
            if not search_html:
                self.logger.warning(f"No search results found for query: {query}")
                return []
            
            urls = self._extract_search_results(search_html)
            results = []
            
            # Process URLs with enhanced error handling
            async def process_url(url):
                try:
                    html_content = await self._fetch_url(url)
                    if html_content:
                        content = self._extract_content(html_content, url)
                        if content:
                            content_type = self._determine_content_type(url)
                            return SearchResult(
                                question=question,
                                organization=organization,
                                content=content.content,
                                url=url,
                                timestamp=datetime.now(),
                                content_type=content_type,  # Using proper enum value
                                relevance_score=0.5
                            )
                except Exception as e:
                    self.logger.error(f"Error processing URL {url}: {str(e)}")
                return None
            
            # Process URLs with concurrent limiting
            tasks = []
            for url in urls:
                if len(tasks) >= self.concurrent_requests:
                    # Wait for some tasks to complete before adding more
                    completed = await asyncio.gather(*tasks, return_exceptions=True)
                    results.extend([r for r in completed if r and not isinstance(r, Exception)])
                    tasks = []
                tasks.append(asyncio.create_task(process_url(url)))
            
            if tasks:
                completed = await asyncio.gather(*tasks, return_exceptions=True)
                results.extend([r for r in completed if r and not isinstance(r, Exception)])
            
            return results
            
        except Exception as e:
            self.logger.error(f"Error in _scrape_single_query: {str(e)}")
            return []

    async def scrape_matrix(self, questions: List[str], organizations: List[str]) -> List[SearchResult]:
        """Enhanced matrix scraping with proper session handling"""
        try:
            self.session = aiohttp.ClientSession()  # Create session
            all_results = []
            
            # Process in batches to avoid overwhelming resources
            batch_size = 4  # Adjust based on your needs
            for i in range(0, len(questions), batch_size):
                question_batch = questions[i:i + batch_size]
                for j in range(0, len(organizations), batch_size):
                    org_batch = organizations[j:j + batch_size]
                    
                    tasks = []
                    for question in question_batch:
                        for org in org_batch:
                            tasks.append(self._scrape_single_query(question, org))
                    
                    batch_results = await asyncio.gather(*tasks, return_exceptions=True)
                    for results in batch_results:
                        if isinstance(results, list):
                            all_results.extend(results)
                    
                    # Add delay between batches
                    await asyncio.sleep(self.request_delay)
            
            return all_results
            
        finally:
            if self.session:
                await self.session.close()




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