# Autok

**Flag Challenge Video Generator**

Autok is a small collection of scripts for creating short flag guessing videos. It downloads flag images, builds quick clips with countdowns, and includes helper tools for uploading to social media.

## Repository layout

```text
Autok/
├── generate_flags.py       # download and classify flags
├── generate_video.py       # compose short videos
├── main.py                 # example upload workflow
├── requirements.txt        # Python dependencies
└── uploaders/
    ├── upload_instagram.py
    └── upload_youtube.py
```

## Quick start

1. Install Python 3 and the packages:
   ```bash
   pip install -r requirements.txt
   ```
2. Create a `config/` folder with a `paths.py` file defining:
   ```python
   OUTPUT_PATH = "output"
   FLAG_DIR = "flags"
   MUSIC_FILE = ["resources/music.mp3"]
   ```
3. Run the pipeline:
   ```bash
   python generate_flags.py        # fetch and categorise flags
   python generate_video.py        # build videos under OUTPUT_PATH
   python main.py                  # upload to YouTube
   ```

External assets (background clips, countdowns, etc.) should live in a `resources/` directory that is not tracked by Git.

## Scripts

| Script | Purpose |
|-------|---------|
| `generate_flags.py` | Downloads flags from REST Countries and groups them into difficulty folders using a SentenceTransformer model. |
| `generate_video.py` | Uses `moviepy` and `gTTS` to create short clips. It pulls paths from `config/paths.py`. |
| `uploaders/upload_youtube.py` | Authenticates with the YouTube API and uploads a file. |
| `uploaders/upload_instagram.py` | Shows how to post a reel using the Instagram Graph API (requires your tokens). |

## Dependencies

The exact versions tested for these scripts are listed below:

| Package | Version |
|---------|---------|
| certifi | 2025.4.26 |
| charset-normalizer | 3.4.2 |
| click | 8.1.8 |
| colorama | 0.4.6 |
| decorator | 4.4.2 |
| gTTS | 2.5.4 |
| idna | 3.10 |
| imageio | 2.37.0 |
| imageio-ffmpeg | 0.6.0 |
| moviepy | 1.0.3 |
| numpy | 2.2.5 |
| Pillow | 9.5.0 |
| proglog | 0.1.12 |
| python-dotenv | 1.1.0 |
| requests | 2.32.3 |
| tqdm | 4.67.1 |
| urllib3 | 2.4.0 |

## Example usage

Below is a minimal snippet showing how a video can be uploaded once generated:

```python
from uploaders.upload_youtube import upload_youtube_video

file_to_upload = "output/Youtube/en/flags_en_1_20250531_115354.mp4"
upload_youtube_video(file_to_upload,
                     title="Guess the Flag!",
                     description="You have 5 seconds… AutoGuessIt! #Shorts",
                     tags=["shorts", "python"])
```

This prints the video ID after a successful upload.

## Next steps

- Tweak `generate_video.py` to change effects or add new languages.
- Try different classification models in `generate_flags.py`.
- Combine the scripts into a package if the project grows.

