# Max ID endpoint (thanks to Salman): https://hacker-news.firebaseio.com/v0/maxitem.json

# 1. Use this endpoint to retrieve the latest ID: https://hacker-news.firebaseio.com/v0/maxitem.json
# 2. Retrieve 10 latest comments based on that
# 3. Ignore all stories, just get comments

import requests

def get_latest_comments():
    # Step 1: Retrieve the latest ID
    latest_id_url = "https://hacker-news.firebaseio.com/v0/maxitem.json"
    latest_id = requests.get(latest_id_url).json()

    comments = []
    current_id = latest_id

    # Step 2 & 3: Retrieve 10 latest comments
    while len(comments) < 10:
        item_url = f"https://hacker-news.firebaseio.com/v0/item/{current_id}.json"
        item = requests.get(item_url).json()

        if item and item["type"] == "comment":
            comments.append(item)
        current_id -= 1  # Move to the previous item

    return comments

# Fetch and print the 10 latest comments
latest_comments = get_latest_comments()
for comment in latest_comments:
    print(comment)

def save_ids_to_file(id1, id2, filename="ids.txt"):
    with open(filename, 'w') as file:
        file.write(f"{id1}\n{id2}")

def load_ids_from_file(filename="ids.txt"):
    with open(filename, 'r') as file:
        id1, id2 = file.read().splitlines()
    return int(id1), int(id2)
