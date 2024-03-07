from FlagEmbedding import BGEM3FlagModel

model = BGEM3FlagModel('BAAI/bge-m3',  
                       use_fp16=True) # Setting use_fp16 to True speeds up computation with a slight performance degradation

sentences_1 = ["What is BGE M3?", "Defination of BM25"]
sentences_2 = ["BGE M3 is an embedding model supporting dense retrieval, lexical matching and multi-vector interaction.", 
               "BM25 is a bag-of-words retrieval function that ranks a set of documents based on the query terms appearing in each document"]

question = 'What do you think about OpenAI and Elon Musk'
embeddings_2 = model.encode(question)['dense_vecs']

def compare_sentences(sentence1, sentence2):
    embedding_1 = model.encode(sentence1)['dense_vecs']
    embedding_2 = model.encode(sentence2)['dense_vecs']
    return embedding_1 @ embedding_2

# print(embeddings_2.tolist())

# embeddings_1 = model.encode(sentences_1, 
#                             batch_size=12, 
#                             max_length=8192, # If you don't need such a long length, you can set a smaller value to speed up the encoding process.
#                             )['dense_vecs']
# similarity = embeddings_1 @ embeddings_2.T
# print(similarity)
# [[0.6265, 0.3477], [0.3499, 0.678 ]]

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

# Use vector search with embeddings_2
documents = collection.vector_find(
    embeddings_2,
    limit=100,
)

# > documents[0].keys()
# dict_keys(['_id', 'URL', 'user', 'text', '$vector', '$similarity'])

print(documents)