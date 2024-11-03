import requests
from pymongo import MongoClient
import os
import dotenv

dotenv.load_dotenv()

organizations = ["University of Maryland, College Park"]
questions = ["Do they have an E-sports team?"]
search_queries = [f"{org} {question}" for org in organizations for question in questions]
search_query = search_queries[0] or "University of Maryland, College Park ESPORTS" 

# Execute the search
search_results = requests.get(f"http://127.0.0.1:8000/search?query={search_query}").json()

# Process and print only the first three results
for item in search_results.get('items', []):
    print(item['title'], item['link'])


scraped_data = {}

# Collect scraped data including the date
for item in search_results.get('items', []):
    url = item['link']
    content = requests.get("http://127.0.0.1:8000/extract?url="+url).json()
    scraped_data[url] = content


pages_contents = [f"{content['title']}\n{content['date_from_url']}\n{' '.join(content['paragraphs'])}" for content in scraped_data.values() if content["paragraphs"]]
completion = requests.get("http://127.0.0.1:8000/answer", params={"pages_contents": '\n\n\n'.join(pages_contents), "question":search_query}).json()
print(completion)

# Connect to the MongoDB database
client = MongoClient(os.environ.get("MONGO_URI"))
db = client.get_database("data_collection")
collection = db.get_collection("data")

# Insert the data into the database
collection.insert_one({"question": search_query, "answer": completion})

# Close the connection
client.close()