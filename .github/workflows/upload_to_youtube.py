import os
import sys
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def upload_video(video_file, title, description):
    # Pobranie poświadczeń OAuth2 z zmiennej środowiskowej
    creds_json = os.environ.get("YOUTUBE_CREDENTIALS")
    if not creds_json:
        print("Error: YOUTUBE_CREDENTIALS secret is not set.")
        sys.exit(1)

    creds_data = json.loads(creds_json)
    credentials = Credentials.from_authorized_user_info(creds_data)

    youtube = build("youtube", "v3", credentials=credentials)

    body = {
        "snippet": {
            "title": title[:100],  # YouTube ogranicza tytuł do 100 znaków
            "description": description,
            "categoryId": "25"  # Kategoria 25 = News & Politics
        },
        "status": {
            "privacyStatus": "public",  # Zmień na 'unlisted' lub 'private' jeśli wolisz testować prywatnie
            "selfDeclaredMadeForKids": False
        }
    }

    media = MediaFileUpload(video_file, chunksize=-1, resumable=True, mimetype="video/mp4")

    print(f"Uploading '{video_file}' to YouTube...")
    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media
    )

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Uploaded {int(status.progress() * 100)}%")

    print(f"Video uploaded successfully! Video ID: {response.get('id')}")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python upload_to_youtube.py <video_file> <title> <description>")
        sys.exit(1)

    video_path = sys.argv[1]
    video_title = sys.argv[2]
    video_desc = sys.argv[3]

    upload_video(video_path, video_title, video_desc)
