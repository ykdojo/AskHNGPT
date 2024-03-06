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

for current_id in range(39610861, 39610871):  # From 39610861 to 39610870
    item_url = f"https://hacker-news.firebaseio.com/v0/item/{current_id}.json"
    item = requests.get(item_url).json()
    
    # Proceed only if item is a comment
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
    else:
        print(f'Skipped item with ID: {current_id}, not a comment or no text field')
