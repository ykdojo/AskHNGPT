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
        {"url": "https://weather.example.com"},
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

# Load the manifest content from the ai-plugin.json file
with open('ai-plugin.json', 'r') as manifest_file:
    manifest_content = json.load(manifest_file)

@app.get("/", response_class=PlainTextResponse)
def intro():
    return "Welcome to AskHNGPT"

@app.get("/hn_comments/{question}", response_class=JSONResponse)
def get_hn_comments(question: str):
    comments = [
        {
            "username": "devUser1",
            "date": "2024-03-01",
            "comment_body": "I think React is great for building fast and scalable front-end applications. It's component-based architecture makes it easy to reuse code.",
            "link": "https://news.ycombinator.com/item?id=12345678"
        },
        {
            "username": "webMaster23",
            "date": "2024-02-28",
            "comment_body": "React has a bit of a learning curve, but once you get the hang of it, it's incredibly powerful.",
            "link": "https://news.ycombinator.com/item?id=87654321"
        },
        {
            "username": "jsGuru",
            "date": "2024-02-27",
            "comment_body": "I've been using React for several years now and it's my go-to library for UI development. The ecosystem is rich and the community is very supportive.",
            "link": "https://news.ycombinator.com/item?id=23456789"
        }
    ]

    return comments

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
