import os
import random
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import *
from gtts import gTTS

# Configuración
FLAG_DIR = r"C:\Users\ricar\OneDrive\Documentos\GitHub\Autok\flags"
OUTPUT_VIDEO = r"C:\Users\ricar\OneDrive\Documentos\GitHub\Autok\output.mp4"
FONT_PATH = r"C:/Windows/Fonts/arial.ttf"
SHOW_DURATION = 3  # segundos antes de mostrar el país
VIDEO_SIZE = (1080, 1920)
MUSIC_FILE = r"C:\Users\ricar\OneDrive\Documentos\GitHub\Autok\background.mp3"  # Añade un archivo MP3 de fondo

# Limpieza
for path in os.listdir():
    if path.startswith("temp_") or path.endswith(".mp3"):
        os.remove(path)

# Cargar banderas aleatorias
flag_files = random.sample(os.listdir(FLAG_DIR), 1)
flag_paths = [os.path.join(FLAG_DIR, f) for f in flag_files]
print("Banderas seleccionadas:", flag_paths)
print("Generando video...")
clips = []

for path in flag_paths:
    country = os.path.splitext(os.path.basename(path))[0].capitalize()
    print(f"Procesando {country}...")
    # Imagen sin texto
    img = Image.open(path).convert("RGB")
    img = img.resize(VIDEO_SIZE)
    img_no_text = img.copy()
    print(f"Imagen {country} cargada y redimensionada.")
    # Imagen con texto
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype(FONT_PATH, 100)
    except:
        font = ImageFont.load_default()
    
    print(f"Fuente cargada: {FONT_PATH}.")
    print("Verificando fuente cargada...")
    print(font.getname())  # Esto lanza excepción si no carga bien


    text = country
    bbox = font.getbbox(text)
    text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    position = ((VIDEO_SIZE[0] - text_w) // 2, VIDEO_SIZE[1] - text_h - 100)

    # Dibujar el texto en la imagen
    draw.text(position, text, font=font, fill="white")

    print(f"Texto '{text}' añadido a la imagen {country}.")
    # Guardar frames temporales
    img_no_text_path = f"temp_{country}_no_text.jpg"
    img_text_path = f"temp_{country}_with_text.jpg"
    img_no_text.save(img_no_text_path)
    img.save(img_text_path)
    print(f"Imagenes guardadas como {img_no_text_path} y {img_text_path}.")
    # Clip sin texto
    clip1 = ImageClip(img_no_text_path).set_duration(SHOW_DURATION)

    # Clip con texto
    clip2 = ImageClip(img_text_path).set_duration(2)

    # Voz del país
    tts = gTTS(text=country, lang="en")
    audio_path = f"{country}.mp3"
    tts.save(audio_path)
    audio = AudioFileClip(audio_path).set_duration(clip2.duration)
    clip2 = clip2.set_audio(audio)
    print(f"Audio para {country} generado y añadido al clip.")
    # Concatenar clips
    final_clip = concatenate_videoclips([clip1, clip2])
    clips.append(final_clip)
    print(f"Clip para {country} generado y añadido a la lista.")
# Juntar todo
video = concatenate_videoclips(clips)

# Música de fondo
if os.path.exists(MUSIC_FILE):
    music = AudioFileClip(MUSIC_FILE).volumex(0.1).set_duration(video.duration)
    video = video.set_audio(CompositeAudioClip([video.audio, music]))

video.write_videofile(OUTPUT_VIDEO, fps=24)
print(f"Video generado: {OUTPUT_VIDEO}")
# Limpieza
for path in os.listdir():
    if path.startswith("temp_") or path.endswith(".mp3"):
        os.remove(path)
