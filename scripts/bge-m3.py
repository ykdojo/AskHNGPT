import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://api-inference.huggingface.co/models/BAAI/bge-m3"
headers = {"Authorization": f"Bearer {os.getenv('HUGGING_FACE_TOKEN')}"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()
	
output = query({
	"inputs": {
		"source_sentence": "That is a happy person",
		"sentences": [
			"That is a happy dog",
			"That is a very happy person",
			"Today is a sunny day"
		]
	},
})

print(output)