import requests
import json

import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="./.env")  # Load environment variables from .env file
API_KEY = os.getenv("API_KEY")
CHANNEL_HANDLE = "MrBeast"

def get_playlist_id():
    try:
        url = f"https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANNEL_HANDLE}&key={API_KEY}"
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        data = response.json()
        playlist_id = data["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
        #print(f"Playlist ID for {CHANNEL_HANDLE}: {playlist_id}")
        print(playlist_id)
        return playlist_id
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    print("get_playlist_id will be called when this script is run directly.")
    get_playlist_id()
else:
    print("get_playlist_id will not be called when this script is imported as a module.")