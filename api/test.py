import requests
from pymongo import MongoClient
import os
import dotenv

dotenv.load_dotenv()

# Connect to the MongoDB database
client = MongoClient(os.environ.get("MONGO_URI"))
db = client.get_database("data_collection")
collection = db.get_collection("data")

organizations = ["University of Maryland, College Park", "University of North Carolina, Chapel Hill"]
questions = ["Do they have an E-sports team?", "Did they close school due to Hurricane Helene?"]
search_queries = [f"{org} {question}" for org in organizations for question in questions]
search_query = search_queries[0] or "University of Maryland, College Park ESPORTS" 

data = {} 
for organization in organizations: 
    for question in questions: 
        search_query = f"{organization} {question}"
        search_results = requests.get(f"http://127.0.0.1:8000/search?query={search_query}").json()
        data[search_query] = search_results.get('items', [])[:1]


scraped_data = {}

# Collect scraped data including the date
for organization in organizations: 
    for question in questions:
        search_query = f"{organization} {question}"
        scraped_data[search_query] = ""
        for item in data[search_query]:
            url = item['link']
            content = requests.get("http://127.0.0.1:8000/extract?url="+url).json()
            scraped_data[search_query] += f"{url}\n\n{content['title']}\n{content['date_from_url']}\n{' '.join(content['paragraphs'])}\n\n\n\n"

        pages_contents = scraped_data[search_query]
        print(pages_contents)
        
        completion = requests.get("http://127.0.0.1:8000/answer", params={"pages_contents": '\n\n\n'.join(pages_contents), "question":search_query}).json()
        print(completion)


        # Insert the data into the database
        collection.insert_one({"question": search_query, "answer": completion})

# Print the data from the database
for item in collection.find():
    print(item)
    
# Close the connection
client.close()