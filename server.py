from fastapi import FastAPI, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, PlainTextResponse
from pydantic import BaseModel
import json
from astrapy.db import AstraDB, AstraDBCollection

app = FastAPI(
    title="Ask HN GPT",
    description="An API that returns the most relevant HN comments asked by the user.",
    version="1.0.0",
    servers=[
        {"url": "https://ffb212d5a44b90.lhr.life"},
    ],
)

# Enable CORS for https://chat.openai.com/
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://chat.openai.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from FlagEmbedding import BGEM3FlagModel
model = BGEM3FlagModel('BAAI/bge-m3', use_fp16=True)

import os
from dotenv import load_dotenv

load_dotenv()

# Initialize the client
db = AstraDB(
  token=os.getenv('ASTRA_DB_APPLICATION_TOKEN'),
  api_endpoint=os.getenv('ASTRA_DB_API_ENDPOINT')
)

# Or you can connect to an existing collection directly
collection = AstraDBCollection(
    collection_name="hn_comments_main", astra_db=db
)
print(collection)
print(f"Connected to Astra DB: {db.get_collections()}")

# Load the manifest content from the ai-plugin.json file
with open('ai-plugin.json', 'r') as manifest_file:
    manifest_content = json.load(manifest_file)

@app.get("/", response_class=PlainTextResponse)
def intro():
    return "Welcome to AskHNGPT"

@app.get("/hn_comments/{question}", response_class=JSONResponse)
def get_hn_comments(question: str):
    print('get_hn_comments')
    embedding = model.encode(question)['dense_vecs']
    print('embedding has been created')
    documents = collection.vector_find(
        embedding,
        limit=100,
    )
    print('documents have been found')

    # > documents[0].keys()
    # dict_keys(['_id', 'URL', 'user', 'text', '$vector', '$similarity'])

    cleaned_documents = []
    total_chars = 0

    for document in documents:
        # Calculate the remaining characters allowed
        remaining_chars = 20000 - total_chars
        
        # If adding this document exceeds the limit, stop adding more documents
        if len(document['text']) > remaining_chars:
            break
        
        # Add characters count of current document to total
        total_chars += len(document['text'])
        
        # Remove $vector and $similarity fields
        document.pop('$vector', None)
        document.pop('$similarity', None)
        
        cleaned_documents.append(document)
    
    print('length of cleaned_documents:', len(cleaned_documents))
    return cleaned_documents

# Serve the manifest file at the /.well-known/ai-plugin.json path
@app.get("/.well-known/ai-plugin.json")
async def serve_manifest():
    return JSONResponse(content=manifest_content)

class TextData(BaseModel):
    text: str

@app.post("/count")
def count_characters_and_words(data: TextData):
    text = data.text
    character_count = len(text)
    word_count = len(text.split())
    return {
        "character_count": character_count,
        "word_count": word_count
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
