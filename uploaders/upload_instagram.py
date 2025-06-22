# upload_to_instagram.py
import requests
import time

ACCESS_TOKEN = "TU_ACCESS_TOKEN"
INSTAGRAM_ACCOUNT_ID = "TU_ID_INSTAGRAM"
VIDEO_PATH = "videos_to_upload/video1.mp4"

def upload_instagram_reel(video_path, caption=""):
    """Sube un video local como Reel a Instagram usando la Graph API."""
    print("🔄 Subiendo Reel...")
    url = f"https://graph.facebook.com/v19.0/{INSTAGRAM_ACCOUNT_ID}/media"
    params = {
        "caption": caption,
        "media_type": "REEL",
        "access_token": ACCESS_TOKEN,
    }
    with open(video_path, "rb") as video:
        files = {"video_file": video}
        res = requests.post(url, data=params, files=files)
    res.raise_for_status()
    creation_id = res.json().get("id")

    # 2. Publicar Reel
    publish_url = (
        f"https://graph.facebook.com/v19.0/{INSTAGRAM_ACCOUNT_ID}/media_publish"
    )
    publish_params = {
        "creation_id": creation_id,
        "access_token": ACCESS_TOKEN,
    }
    time.sleep(5)

    pub_res = requests.post(publish_url, data=publish_params)
    pub_res.raise_for_status()
    print("✅ Reel publicado")


if __name__ == "__main__":
    upload_instagram_reel(VIDEO_PATH, "Descripción de prueba")
