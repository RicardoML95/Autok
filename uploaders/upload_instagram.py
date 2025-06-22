# upload_to_instagram.py
import requests
import time

ACCESS_TOKEN = "TU_ACCESS_TOKEN"
INSTAGRAM_ACCOUNT_ID = "TU_ID_INSTAGRAM"
VIDEO_PATH = "videos_to_upload/video1.mp4"

def upload_instagram_reel(video_path, caption=""):
    print("🔄 Subiendo Reel...")
    video = open(video_path, "rb")

    # 1. Subir video en background
    url = f"https://graph.facebook.com/v19.0/{INSTAGRAM_ACCOUNT_ID}/media"
    params = {
        "video_url": "https://tuvideoserver.com/video1.mp4",  # O necesitas subirlo a un host primero
        "caption": caption,
        "media_type": "REEL",
        "access_token": ACCESS_TOKEN
    }
    res = requests.post(url, params=params)
    creation_id = res.json().get("id")

    # 2. Publicar Reel
    publish_url = f"https://graph.facebook.com/v19.0/{INSTAGRAM_ACCOUNT_ID}/media_publish"
    publish_params = {
        "creation_id": creation_id,
        "access_token": ACCESS_TOKEN
    }
    time.sleep(5)  # esperar unos segundos

    pub_res = requests.post(publish_url, params=publish_params)
    print("✅ Reel publicado")

upload_instagram_reel(VIDEO_PATH, "Descripción de prueba")
