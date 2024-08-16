import os
import pandas as pd
from googleapiclient.discovery import build
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variables
API_KEY = os.getenv('YOUTUBE_API_KEY')

# Dictionary to hold channel names and their corresponding environment variable names
channel_dict = {'BuzzFeedVideo': os.getenv('BUZZFEED_VIDEO_CHANNEL_ID'),}

# Create a YouTube service object
youtube = build('youtube', 'v3', developerKey=API_KEY)

# Function to get videos from a channel
def get_channel_videos(channel_id):
    videos = []
    request = youtube.search().list(
        part='snippet',
        channelId=channel_id,
        maxResults=50,
        type='video'
    )
    response = request.execute()

    for item in response['items']:
        video_id = item['id']['videoId']
        videos.append(video_id)

    return videos

# Function to get video details
def get_video_details(video_ids):
    video_details = []
    for video_id in video_ids:
        request = youtube.videos().list(
            part='snippet,contentDetails,statistics,status',
            id=video_id
        )
        response = request.execute()

        for item in response['items']:
            video_info = {
                'Video ID': item['id'],
                'Channel ID': item['snippet']['channelId'],
                'Title': item['snippet']['title'],
                'Tags': ', '.join(item['snippet'].get('tags', [])),
                'Description': item['snippet']['description'],
                'Privacy': item.get('status', {}).get('privacyStatus', 'N/A'),
                'Date Published': item['snippet']['publishedAt'],
                'Category ID': item['snippet']['categoryId'],
                'Thumbnail': item['snippet']['thumbnails']['high']['url'],
                'Watch URL': f"https://www.youtube.com/watch?v={item['id']}",
                'File Name': f"{item['id']}.mp4",
                'Date Backed': '',
                'View Count': item['statistics'].get('viewCount', 0),
                'Comment Count': item['statistics'].get('commentCount', 0),
                'Like Count': item['statistics'].get('likeCount', 0),
                'Dislike Count': item['statistics'].get('dislikeCount', 0),
                'Length (seconds)': item['contentDetails']['duration']
            }
            video_details.append(video_info)
    
    return video_details

# Get videos from channels and their details
all_videos = []
for channel_name, channel_id in channel_dict.items():
    video_ids = get_channel_videos(channel_id)
    video_details = get_video_details(video_ids)
    all_videos.extend(video_details)

# Convert to DataFrame and save to Excel
df = pd.DataFrame(all_videos)
df.to_excel('buzzfeed_youtube_metrics.xlsx', index=False)

print('Data has been saved to buzzfeed_youtube_metrics.xlsx')