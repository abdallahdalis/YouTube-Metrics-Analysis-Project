"""Extract YouTube video metrics for one or more channels via the Data API v3.

Reads channel IDs and an API key from environment variables (.env), pulls every
video for each channel (paginated), fetches details in batches of 50, and saves
the result to an Excel file.

    python yt-analysis.py
"""
import os
import re

import pandas as pd
from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")
if not API_KEY:
    raise SystemExit("YOUTUBE_API_KEY not set — copy .env.example to .env and fill it in.")

# Map a friendly channel name to its channel-ID env var.
channel_dict = {
    "BuzzFeedVideo": os.getenv("BUZZFEED_VIDEO_CHANNEL_ID"),
}

OUTPUT_XLSX = "buzzfeed_youtube_metrics.xlsx"

youtube = build("youtube", "v3", developerKey=API_KEY)


def parse_duration_seconds(iso: str) -> int:
    """Convert an ISO-8601 duration (e.g. 'PT1M45S') to total seconds."""
    m = re.fullmatch(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", iso or "")
    if not m:
        return 0
    h, mn, s = (int(x) if x else 0 for x in m.groups())
    return h * 3600 + mn * 60 + s


def get_channel_videos(channel_id):
    """Return all video IDs for a channel, following pagination."""
    video_ids, page_token = [], None
    while True:
        resp = youtube.search().list(
            part="id", channelId=channel_id, maxResults=50,
            type="video", pageToken=page_token,
        ).execute()
        video_ids += [it["id"]["videoId"] for it in resp.get("items", [])]
        page_token = resp.get("nextPageToken")
        if not page_token:
            return video_ids


def chunks(seq, n):
    for i in range(0, len(seq), n):
        yield seq[i:i + n]


def get_video_details(video_ids):
    """Fetch details for many videos, batching 50 IDs per API call."""
    details = []
    for batch in chunks(video_ids, 50):  # API allows up to 50 ids per request
        resp = youtube.videos().list(
            part="snippet,contentDetails,statistics,status",
            id=",".join(batch),
        ).execute()
        for item in resp.get("items", []):
            sn, st = item["snippet"], item.get("statistics", {})
            details.append({
                "Video ID": item["id"],
                "Channel ID": sn["channelId"],
                "Title": sn["title"],
                "Tags": ", ".join(sn.get("tags", [])),
                "Description": sn["description"],
                "Privacy": item.get("status", {}).get("privacyStatus", "N/A"),
                "Date Published": sn["publishedAt"],
                "Category ID": sn.get("categoryId", ""),
                "Thumbnail": sn["thumbnails"]["high"]["url"],
                "Watch URL": f"https://www.youtube.com/watch?v={item['id']}",
                "View Count": int(st.get("viewCount", 0)),
                "Comment Count": int(st.get("commentCount", 0)),
                "Like Count": int(st.get("likeCount", 0)),
                # Note: YouTube removed public dislike counts in 2021 (omitted).
                "Length (seconds)": parse_duration_seconds(item["contentDetails"]["duration"]),
            })
    return details


def main():
    all_videos = []
    for name, channel_id in channel_dict.items():
        if not channel_id:
            print(f"Skipping {name}: channel ID not set in environment.")
            continue
        ids = get_channel_videos(channel_id)
        print(f"{name}: {len(ids)} videos found")
        all_videos.extend(get_video_details(ids))

    if not all_videos:
        raise SystemExit("No videos retrieved — check channel IDs and API key.")

    df = pd.DataFrame(all_videos)
    df.to_excel(OUTPUT_XLSX, index=False)
    print(f"Saved {len(df)} rows to {OUTPUT_XLSX}")


if __name__ == "__main__":
    main()
