import requests
import re
from datetime import datetime
import dotenv
import os

dotenv.load_dotenv()


# Custom Google API for Search
cse_id = os.getenv("CSE_ID")
cse_api_key = os.getenv("CSE_API_KEY")

def google_search(query, api_key, cse_id, **kwargs):
    base_url = "https://www.googleapis.com/customsearch/v1"
    params = {"q": query, "key": api_key, "cx": cse_id}
    params.update(kwargs)
    response = requests.get(base_url, params=params)
    result = response.json()
    return result

search_query = "University of Maryland, College Park ESPORTS"

# Execute the search
search_results = google_search(search_query, cse_api_key, cse_id)

# Process and print only the first three results
for item in search_results.get('items', []):
    print(item['title'], item['link'])


import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

def extract_date_from_url(url):
    # Regex to find dates in format 'YYYY/MM/DD' in URLs
    date_pattern = r"/(\d{4}/\d{1,2}/\d{1,2})/"
    match = re.search(date_pattern, url)
    if match:
        try:
            # Extract the date and convert it to a more readable format
            return datetime.strptime(match.group(1), '%Y/%m/%d').date()
        except ValueError:
            return "Invalid date format"
    return "No date in URL"

def scrape_webpage(url):
    # Extract date from URL to keep it after scraping
    date_from_url = extract_date_from_url(url)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Will raise an HTTPError for bad responses
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find('title').text if soup.find('title') else 'No Title'
        paragraphs = [p.get_text(strip=True) for p in soup.find_all('p')]
        return {'title': title, 'paragraphs': paragraphs, 'date_from_url': date_from_url}
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return {'title': 'Failed to Load', 'paragraphs': [], 'date_from_url': date_from_url}

scraped_data = {}

# Collect scraped data including the date
for item in search_results.get('items', []):
    url = item['link']
    content = scrape_webpage(url)
    scraped_data[url] = content

# Iterate through the scraped data to print results
for url, data in scraped_data.items():
    print(f"URL: {url}")
    print(f"Title: {data['title']}")
    print(f"Date from URL: {data['date_from_url']}")
    print()
    # Ensure paragraphs is not empty before trying to print excerpts
    content_preview = " ".join(data['paragraphs'][:3]) if data['paragraphs'] else "No content available"
    print("Content Preview:", content_preview)
    print()  # Extra line for better separation of entries
