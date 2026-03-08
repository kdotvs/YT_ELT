import requests
import json
from datetime import date

import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="./.env")  # Load environment variables from .env file
API_KEY = os.getenv("API_KEY")
CHANNEL_HANDLE = "MrBeast"
maxResults = 50

def get_playlist_id():
    try:
        url = f"https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANNEL_HANDLE}&key={API_KEY}"
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        data = response.json()
        channel_playlist_id = data["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
        #print(f"Playlist ID for {CHANNEL_HANDLE}: {playlist_id}")
        print(channel_playlist_id)
        return channel_playlist_id
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")


def get_video_ids(playlistId):

    video_ids = []
    pageToken = None
    base_url = f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={maxResults}&playlistId={playlistId}&key={API_KEY}"

    try:
        while True:
            url = base_url
            if pageToken:
                url += f"&pageToken={pageToken}"
            response = requests.get(url)
            response.raise_for_status()  # Check if the request was successful
            data = response.json()

            for item in data.get("items", []):
                video_id = item["contentDetails"]["videoId"]
                video_ids.append(video_id)

            pageToken = data.get("nextPageToken")
            if not pageToken:
                break

        #print(video_ids)
        return video_ids

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")


def extract_video_data(video_ids):
    extracted_data = []

    def batch_list(video_id_lst, batch_size=50):
        for i in range(0, len(video_id_lst), batch_size):
            yield video_id_lst[i:i + batch_size]

    try:
        for batch in batch_list(video_ids, maxResults):
            video_id_str = ",".join(batch)
            url = f"https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&part=snippet&part=statistics&id={video_id_str}&key={API_KEY}"
            response = requests.get(url)
            response.raise_for_status()  # Check if the request was successful
            data = response.json()

            for item in data.get("items", []):
                video_data = {
                    "videoId": item["id"],
                    "snippet": item["snippet"],
                    "title": item["snippet"]["title"],
                    "duration": item["contentDetails"]["duration"],
                    "publishedAt": item["snippet"]["publishedAt"],
                    "viewCount": item["statistics"].get("viewCount", None),
                    "likeCount": item["statistics"].get("likeCount", None),
                    "commentCount": item["statistics"].get("commentCount", None)
                }
                extracted_data.append(video_data)
        return extracted_data
    
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

"""
# Example usage: The following code will only execute if this script is run directly, not when imported as a module.
if __name__ == "__main__":
    print("get_playlist_id will be called when this script is run directly.")
    playlistId = get_playlist_id()
    #print(get_video_ids(playlistId))
    video_ids = get_video_ids(playlistId)
    #print(extract_video_data(video_ids))
    extract_video_data(video_ids)

else:
    print("get_playlist_id will not be called when this script is imported as a module.")
"""

def save_data_to_json(extracted_data):
    file_path = f"./data/YT_data_{date.today()}.json"

    with open(file_path, "w", encoding="utf-8") as json_outfile:
        json.dump(extracted_data, json_outfile, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    playlistId = get_playlist_id()
    video_ids = get_video_ids(playlistId)
    video_data = extract_video_data(video_ids)
    save_data_to_json(video_data)
    

