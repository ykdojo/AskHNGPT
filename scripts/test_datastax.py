from astrapy.db import AstraDB

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

