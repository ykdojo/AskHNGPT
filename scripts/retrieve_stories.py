# Max ID endpoint (thanks to Salman): https://hacker-news.firebaseio.com/v0/maxitem.json?print=pretty

import requests

def get_recent_stories(limit=3):
    # Fetch the latest stories' IDs
    response = requests.get("https://hacker-news.firebaseio.com/v0/newstories.json")
    story_ids = response.json()[:limit]  # Get the first 'limit' number of story IDs
    
    stories = []
    for id in story_ids:
        # Fetch each story's details by its ID
        story_response = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{id}.json")
        story = story_response.json()
        stories.append(story)
    
    return stories

# Fetch the 3 most recent stories
recent_stories = get_recent_stories(3)

# Print the titles and URLs of the stories
for story in recent_stories:
    print(f"Title: {story['title']}\nURL: {story.get('url', 'No URL')}\n")
