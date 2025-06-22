# upload_to_youtube.py
import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

def upload_youtube_video(file_path, title, description, tags):
    scopes = ["https://www.googleapis.com/auth/youtube.upload"]

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "config\client_secret_googleusercontent.json"

    # Autenticación
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_local_server(port=0)

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    request_body = {
        "snippet": {
            "categoryId": "24",  # Entertainment category
            "title": title,
            "description": description,
            "tags": tags
        },
        "status": {
            "privacyStatus": "private"
        }
    }

    media_file = googleapiclient.http.MediaFileUpload(file_path)

    request = youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=media_file
    )

    response = request.execute()
    print(f"✅ Subido: {response['id']}")
