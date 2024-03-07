from fastapi import FastAPI, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, PlainTextResponse
from pydantic import BaseModel
import json

app = FastAPI(
    title="Ask HN GPT",
    description="An API that returns the most relevant HN comments asked by the user.",
    version="1.0.0",
    servers=[
        {"url": "https://7e9de4463e2821.lhr.life"},
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

model = BGEM3FlagModel('BAAI/bge-m3',  
                       use_fp16=True)

# Load the manifest content from the ai-plugin.json file
with open('ai-plugin.json', 'r') as manifest_file:
    manifest_content = json.load(manifest_file)

@app.get("/", response_class=PlainTextResponse)
def intro():
    return "Welcome to AskHNGPT"

@app.get("/hn_comments/{question}", response_class=JSONResponse)
def get_hn_comments(question: str):
    embedding = model.encode(question)['dense_vecs']
    return embedding.tolist()

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
