# Reels & Shorts Downloader

A web application to download Instagram Reels, YouTube Shorts, and other short videos by pasting the link.

## Features

- Paste a video link
- Preview the video
- Download the video in MP4 format

## Installation

1. Install Python 3.8+
2. Clone or download this repository
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Running the Application

1. Start the server:
   ```
   uvicorn app.main:app --reload
   ```

2. Open your browser and go to `http://127.0.0.1:8000`

3. Paste a reel/shorts link and click Download.

## Supported Sites

Thanks to yt-dlp, supports many sites including:
- Instagram Reels
- YouTube Shorts
- TikTok
- And many more