# Autok

Autok is a collection of Python scripts for creating short flag guessing videos and uploading them to social media.

## Repository structure

```
/Autok
├── generate_flags.py
├── generate_video.py
├── main.py
├── requirements.txt
└── uploaders/
    ├── upload_instagram.py
    └── upload_youtube.py
```

Each file is executed directly (the project has no package layout). The `uploaders/` directory holds helper functions for publishing videos to different platforms.

## Flag collection and classification

`generate_flags.py` fetches country data from the REST Countries API and downloads flag images. The beginning of the script looks like this:
\n```python
import requests
import os
from transformers import pipeline

def fetch_flags_and_names():
    url = "https://restcountries.com/v3.1/all"
    response = requests.get(url)
    response.raise_for_status()
    countries = response.json()

    flags = []
    for country in countries:
        try:
            flag_url = country['flags']['png']
            name_en = country['name']['common']
            name_es = country['translations']['spa']['common']
            flags.append({
                'flag_url': flag_url,
                'name_en': name_en,
                'name_es': name_es
            })
        except KeyError:
            continue

    return flags
```

Flags are grouped into difficulty categories using a sentence-transformer model:
```python

labels = {
    "easy": ["United States", "Germany", "China", "Brazil"],
    "medium": ["Peru", "Morocco", "Vietnam", "Philippines"],
    "hard": ["Moldova", "Eritrea", "Kazakhstan", "Bhutan"],
    "very difficult": ["Comoros", "Tuvalu", "São Tomé and Príncipe", "Kiribati"]
}

label_embeddings = {label: model.encode(countries) for label, countries in labels.items()}

def classify_country_difficulty(country_name):
    country_emb = model.encode(country_name)
    max_sim = -1
    best_label = None
    for label, embs in label_embeddings.items():
        sims = util.cos_sim(country_emb, embs)
        avg_sim = sims.mean().item()
        if avg_sim > max_sim:
            max_sim = avg_sim
            best_label = label
    print(f"Clasificación para {country_name}: {best_label}")
    print(f"Similitud promedio: {max_sim}")
    return best_label


def save_flags_to_folder_by_category(flags, folder_path):
    # Crear carpetas por dificultad
    for category in ["easy", "medium", "hard", "very difficult"]:
        os.makedirs(os.path.join(folder_path, category), exist_ok=True)

    for flag in flags:
        category = classify_country_difficulty(flag['name_en'])
        # Formato de nombre: nombre_ingles=nombre_espanol.png
        file_name = f"{flag['name_en'].lower()}={flag['name_es'].lower()}.png"
        flag_path = os.path.join(folder_path, category, file_name)
        response = requests.get(flag['flag_url'], stream=True)
        response.raise_for_status()
        with open(flag_path, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
    print(f"Banderas clasificadas y guardadas en {folder_path}")

if __name__ == "__main__":
    folder_path = "flags"
```

The flags are stored under a local `flags/` directory organised by category.

## Video generation

`generate_video.py` composes videos using `moviepy`. It relies on configuration variables defined in `config/paths.py`:
```python
import os
import random
from PIL import Image
from moviepy.editor import *
from gtts import gTTS
from moviepy.config import change_settings
from moviepy.editor import VideoFileClip, concatenate_videoclips
from pydub import AudioSegment
import requests  # Agregar para descargar audio de TikTok TTS
from datetime import datetime
import datetime
import base64
from config.paths import OUTPUT_PATH, FLAG_DIR, MUSIC_FILE

change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"})
```

After assembling the clips, the script writes the result to `OUTPUT_PATH` and adds background music:
```python
    bg_clip = make_looping_background(total_duration, base_bg)

    # Superponer banderas/textos sobre el fondo animado global
    count = 0
    for i in MUSIC_FILE:
        count += 1
        if not os.path.exists(i):
            raise FileNotFoundError(f"Archivo de música no encontrado: {i}")
        # Música de fondo
        video = CompositeVideoClip([bg_clip, video_flags], size=VIDEO_SIZE)
        if os.path.exists(i):
            print(f"Agregando música de fondo: {i}")
            music = AudioFileClip(i).volumex(0.1).set_duration(video.duration)
            video = video.set_audio(CompositeAudioClip([video.audio, music]))
        video_name = os.path.join(OUTPUT_PATH, VIDEO_PLATFORMS[count-1], lang, f"flags_{lang}_{count}_{CREATION_TIME}.mp4")
        video.write_videofile(video_name, fps=24)
        print(f"Video generado: {video_name}")
# Limpieza
for path in os.listdir():
    if path.startswith("temp_") or path.endswith(".mp3"):
        os.remove(path)
```

## Uploading videos

`main.py` shows a basic example of uploading a generated clip to YouTube:
```python
from uploaders.upload_youtube import upload_youtube_video
# from uploaders.upload_instagram import upload_instagram_reel


print("🚀 Subiendo nuevo video")
upload_youtube_video(r"output\Youtube\en\flags_en_1_20250531_115354.mp4", "Guess test!", "You have 5 seconds… AutoGuessIt! #Shorts", ["shorts", "python"])
# upload_instagram_reel("videos_to_upload/video1.mp4", "¡Nuevo video!")
print("✅ Video subido a YouTube")
```

The uploader uses OAuth credentials referenced in `uploaders/upload_youtube.py`:
```python
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
```

There is also an Instagram example with placeholders for your tokens:
```python
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
```

## Dependencies

All Python packages needed for these scripts are listed in `requirements.txt`:
```text
c e r t i f i = = 2 0 2 5 . 4 . 2 6  
 c h a r s e t - n o r m a l i z e r = = 3 . 4 . 2  
 c l i c k = = 8 . 1 . 8  
 c o l o r a m a = = 0 . 4 . 6  
 d e c o r a t o r = = 4 . 4 . 2  
 g T T S = = 2 . 5 . 4  
 i d n a = = 3 . 1 0  
 i m a g e i o = = 2 . 3 7 . 0  
 i m a g e i o - f f m p e g = = 0 . 6 . 0  
 m o v i e p y = = 1 . 0 . 3  
 n u m p y = = 2 . 2 . 5  
 P i l l o w = = 9 . 5 . 0  
 p r o g l o g = = 0 . 1 . 1 2  
 p y t h o n - d o t e n v = = 1 . 1 . 0  
 r e q u e s t s = = 2 . 3 2 . 3  
 t q d m = = 4 . 6 7 . 1  
 u r l l i b 3 = = 2 . 4 . 0  
```

## Workflow

1. Run `generate_flags.py` to create the `flags/` folder with categorised images.
2. Run `generate_video.py` to build clips for each language and platform. The files are written to `OUTPUT_PATH`.
3. Use `main.py` or the scripts in `uploaders/` to publish the final videos.

External resources such as background clips and audio should reside in a `resources/` directory, and the `config/` directory must define variables like `OUTPUT_PATH`, `FLAG_DIR` and `MUSIC_FILE`.

## Next steps

- Explore the `moviepy` library to customise animations or effects.
- Experiment with different models for classification.
- Review the YouTube and Instagram API documentation if you plan to automate uploads.
- Consider reorganising these scripts into a package structure as the project grows.
