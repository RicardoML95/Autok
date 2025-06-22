# 🌍 Autok

**Autok** es una colección de scripts en Python para generar videos cortos de adivinanza de banderas y subirlos automáticamente a redes sociales como YouTube e Instagram.

---

## 📁 Estructura del repositorio

```
/Autok
├── generate_flags.py           # Descarga y clasifica banderas
├── generate_video.py           # Genera los videos a partir de banderas
├── main.py                     # Ejecuta la subida de videos
├── requirements.txt            # Dependencias
└── uploaders/
    ├── upload_instagram.py     # Subida a Instagram
    └── upload_youtube.py       # Subida a YouTube
```

---

## 🚩 Generación y clasificación de banderas

`generate_flags.py` obtiene datos de países desde la API de REST Countries y descarga las banderas:

```python
import requests
import os
from transformers import pipeline

def fetch_flags_and_names():
    url = "https://restcountries.com/v3.1/all"
    response = requests.get(url)
    response.raise_for_status()
    countries = response.json()
    # ...
```

Las banderas se clasifican por dificultad usando `sentence-transformers`:

```python
labels = {
    "easy": ["United States", "Germany", "China", "Brazil"],
    "medium": ["Peru", "Morocco", "Vietnam", "Philippines"],
    "hard": ["Moldova", "Eritrea", "Kazakhstan", "Bhutan"],
    "very difficult": ["Comoros", "Tuvalu", "São Tomé and Príncipe", "Kiribati"]
}
```

Las banderas se guardan localmente en la carpeta `flags/` organizada por categoría.

---

## 🎬 Generación de video

`generate_video.py` usa `moviepy` y `gTTS` para componer videos con las banderas y música de fondo. Depende de configuraciones definidas en `config/paths.py`:

```python
from config.paths import OUTPUT_PATH, FLAG_DIR, MUSIC_FILE
change_settings({"IMAGEMAGICK_BINARY": r"C:\...path\to\magick.exe"})
```

Ejemplo de ensamblado de clips:

```python
video = CompositeVideoClip([bg_clip, video_flags], size=VIDEO_SIZE)
music = AudioFileClip(i).volumex(0.1).set_duration(video.duration)
video = video.set_audio(CompositeAudioClip([video.audio, music]))
video.write_videofile(output_path, fps=24)
```

---

## 🚀 Subida automática de videos

`main.py` muestra cómo subir un video generado a YouTube:

```python
from uploaders.upload_youtube import upload_youtube_video

upload_youtube_video(
    r"output\Youtube\en\flags_en_1_20250531_115354.mp4",
    "Guess test!",
    "You have 5 seconds… AutoGuessIt! #Shorts",
    ["shorts", "python"]
)
```

### Subida a YouTube (OAuth)

```python
flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    "config/client_secret_googleusercontent.json",
    scopes=["https://www.googleapis.com/auth/youtube.upload"]
)
```

### Subida a Instagram (ejemplo)

```python
ACCESS_TOKEN = "TU_ACCESS_TOKEN"
INSTAGRAM_ACCOUNT_ID = "TU_ID_INSTAGRAM"

from uploaders.upload_instagram import upload_instagram_reel

upload_instagram_reel("videos_to_upload/video1.mp4", "¡Nuevo video!")
```

> ⚠️ Requiere subir el video a un servidor accesible o usar Graph API para archivos locales.

---

## 📦 Dependencias

Incluidas en `requirements.txt`:

```txt
requests
transformers
sentence-transformers
moviepy
pydub
gTTS
google-auth-oauthlib
google-api-python-client
```

---
