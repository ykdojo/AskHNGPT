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

# Or you can connect to an existing connection directly
collection = AstraDBCollection(
    collection_name="hn_comments_main", astra_db=db
)
print(collection)
print(f"Connected to Astra DB: {db.get_collections()}")

current_id = 39610860
import requests
item_url = f"https://hacker-news.firebaseio.com/v0/item/{current_id}.json"
item = requests.get(item_url).json()
print(item)
# {'by': 'pm90', 'id': 39610860, 'parent': 39565773, 'text': 'I don’t think so. However Tesla is famous for lowballing SWEs and they have a pretty terrible internal development&#x2F;services platform. I wouldn’t want to work there as an SWE.', 'time': 1709685288, 'type': 'comment'}
# URL: https://news.ycombinator.com/item?id=39610860

from FlagEmbedding import BGEM3FlagModel
model = BGEM3FlagModel('BAAI/bge-m3', use_fp16=True)

embedding = model.encode(item['text'])['dense_vecs']
print(embedding)

collection.insert_one(
    {
        "_id": item['id'],
        "URL": f"https://news.ycombinator.com/item?id={item['id']}",
        "user": item['by'],
        'text': item['text'],
        "$vector": embedding,
    }
)
print('Inserted comment')