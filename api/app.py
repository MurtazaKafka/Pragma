from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup
from openai import OpenAI
import os
import dotenv

import re
import datetime

dotenv.load_dotenv()

app = FastAPI()

CSE_ID = os.getenv("CSE_ID")
CSE_API_KEY = os.getenv("CSE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


@app.get("/search")
def query_search(query):
    base_url = "https://www.googleapis.com/customsearch/v1"
    params = {"q": query, "key": CSE_API_KEY, "cx": CSE_ID}
    response = requests.get(base_url, params=params)
    result = response.json()
    return result


@app.get("/extract") 
def scrape_webpage(url):
    # Extract date from URL to keep it after scraping
    date_pattern = r"/(\d{4}/\d{1,2}/\d{1,2})/"
    match = re.search(date_pattern, url)
    if match: 
        try: 
            # Extract the date and convert it to a more readable format
            date_from_url = datetime.strptime(match.group(1), '%Y/%m/%d').date()
        except ValueError:
            date_from_url = "Invalid date format"
    else: 
        date_from_url = "No date in URL"
    
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



@app.get("/answer")
def answer_question(pages_contents, question): 
    client = OpenAI(api_key=OPENAI_API_KEY)
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", 
             "content": "You are a data collector. You will be given 3 websites and their contents. Based on these content, you are prompted to answer the question you are given for data collection purposes."}, 
            {"role": "user", "content": pages_contents + 
             f"Based on this information, give me the answer to this questions: {question}. I want your completion to be concise and definite. Give me colon separated values like, <question>: <retrieved respnonse>."},
        ]
    )

    return completion.choices[0].message.content

os.system('python3 -m uvicorn app:app --reload')