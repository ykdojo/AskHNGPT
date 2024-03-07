from astrapy.db import AstraDB, AstraDBCollection

import os
from dotenv import load_dotenv

load_dotenv()

# Initialize the client
db = AstraDB(
  token=os.getenv('ASTRA_DB_APPLICATION_TOKEN'),
  api_endpoint=os.getenv('ASTRA_DB_API_ENDPOINT')
)

# Create a collection. The default similarity metric is "cosine".
# collection = db.create_collection("hn_comments_main", dimension=1024, metric="cosine")
# print(collection)
# print(f"Connected to Astra DB: {db.get_collections()}")

# Or you can connect to an existing collection directly
collection = AstraDBCollection(
    collection_name="hn_comments_main", astra_db=db
)
print(collection)
print(f"Connected to Astra DB: {db.get_collections()}")

import requests
from FlagEmbedding import BGEM3FlagModel
model = BGEM3FlagModel('BAAI/bge-m3', use_fp16=True)

def save_ids_to_file(id1, id2, filename="ids.txt"):
    with open(filename, 'w') as file:
        file.write(f"{id1}\n{id2}")

def load_ids_from_file(filename="ids.txt"):
    with open(filename, 'r') as file:
        id1, id2 = file.read().splitlines()
    return int(id1), int(id2)

# Load the last ID processed and the starting ID from the file
first_processed_id, last_processed_id = load_ids_from_file()

# Define the starting ID for processing as the next ID after the last processed
start_id = last_processed_id + 1

# Initialize a variable to track the highest ID processed in this run
highest_id_processed = start_id

comments_processed = 0
current_id = start_id

while comments_processed < 10000:
    item_url = f"https://hacker-news.firebaseio.com/v0/item/{current_id}.json"
    item = requests.get(item_url).json()
    
    if not item:
        print(f'No item with ID: {current_id}')
        break
    # Check if the item exists and proceed only if it's a comment
    if item.get('type') == 'comment' and 'text' in item:
        embedding = model.encode(item['text'])['dense_vecs']
        collection.insert_one({
            "_id": item['id'],
            "URL": f"https://news.ycombinator.com/item?id={item['id']}",
            "user": item['by'],
            'text': item['text'],
            "$vector": embedding,
        })
        print(f'Inserted comment with ID: {current_id}')
        highest_id_processed = current_id  # Update the highest ID processed
        save_ids_to_file(first_processed_id, highest_id_processed)
        comments_processed += 1  # Increment the counter for processed comments
    else:
        print(f'Skipped item with ID: {current_id}, not a comment or no text field')

    current_id += 1  # Move to the next ID
