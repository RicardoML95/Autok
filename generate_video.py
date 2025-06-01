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

change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"})



def make_looping_background(duration, base_clip):
    base_clip = base_clip.without_audio()
    if base_clip.duration is None:
        raise ValueError("El clip base no tiene duración definida.")
    n_loops = int(duration // base_clip.duration)
    remainder = duration % base_clip.duration
    clips = [base_clip] * n_loops
    if remainder > 0:
        clips.append(base_clip.subclip(0, remainder))
    final = concatenate_videoclips(clips)
    return final.set_duration(duration)


def crear_carpetas_salida(output_path):
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    idiomas = ["es", "en"]
    plataformas = ["Youtube", "Instagram", "Tiktok"]
    for idioma in idiomas:
        for plataforma in plataformas:
            ruta = os.path.join(output_path, plataforma, idioma)
            if not os.path.exists(ruta):
                os.makedirs(ruta)
                print(f"Carpeta creada: {ruta}")



# Configuración
FLAG_DIR = r"C:\Users\ricar\OneDrive\Documentos\GitHub\Autok\flags"
OUTPUT_PATH = r"C:\Users\ricar\OneDrive\Documentos\GitHub\Autok\output"
FONT_NAME = "PoetsenOne"
SHOW_DURATION = 3 
GUESS_DURATION = 2
VIDEO_SIZE = (1080, 1920)
MUSIC_FILE = [r"C:\Users\ricar\OneDrive\Documentos\GitHub\Autok\resources\music_background_1.mp3",
              r"C:\Users\ricar\OneDrive\Documentos\GitHub\Autok\resources\music_background_2.mp3",
              r"C:\Users\ricar\OneDrive\Documentos\GitHub\Autok\resources\music_background_3.mp3"]
BACKGROUND_FILE = "resources/campo_landscape.mp4"
FLAG_LANG = "en"
FLAG_BASE_DIR = os.path.join(FLAG_DIR, FLAG_LANG)
DIFFICULTY_CATEGORIES = ["easy", "medium", "hard", "very difficult"]
DIFFICULTY_COLORS = {"easy": "green", "medium": "yellow", "hard": "red", "very difficult": "purple"}
DIFFICULTY_WEIGHTS = [4, 4, 2, 1]  # easy:2/6, medium:2/6, hard:1/6, very difficult:1/6
NUM_FLAGS = 1
MARGIN_RATIO = 0.1  # 10% de margen
TIKTOK_VOICE = "en_uk_001"  # Voz de TikTok para la introducción
CREATION_TIME = now_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
VIDEO_PLATFORMS = ["Youtube", "Instagram", "Tiktok"]

crear_carpetas_salida(OUTPUT_PATH)

# Limpieza
for path in os.listdir():
    if path.startswith("temp_") or path.endswith(".mp3") or path.endswith(".mp4"):
        os.remove(path)

# Elegir una sola categoría según los pesos
elegida_categoria = random.choices(DIFFICULTY_CATEGORIES, weights=DIFFICULTY_WEIGHTS, k=1)[0]
difficulty_folder = os.path.join(FLAG_DIR, elegida_categoria)
flag_files = os.listdir(difficulty_folder)
# Seleccionar sin repetición
selected_flags = random.sample(flag_files, min(NUM_FLAGS, len(flag_files)))
flag_paths = [os.path.join(difficulty_folder, flag_file) for flag_file in selected_flags]

# Obtener nombres en inglés y español de los archivos seleccionados
def parse_flag_filename(filename):
    base = os.path.splitext(filename)[0]
    if '=' in base:
        name_en, name_es = base.split('=', 1)
        return name_en.strip(), name_es.strip()
    return base, base

selected_flags_info = [
    {
        'path': os.path.join(difficulty_folder, fname),
        'name_en': parse_flag_filename(fname)[0],
        'name_es': parse_flag_filename(fname)[1]
    }
    for fname in selected_flags
]

print(f"Categoría elegida: {elegida_categoria}")
print("Banderas seleccionadas:", [f['path'] for f in selected_flags_info])
print("Generando videos en ambos idiomas...")

for lang, lang_name_key, tts_lang, tiktok_voice in [
    ("en", "name_en", "en", "en_uk_001"),
    ("es", "name_es", "es", "es_mx_002")
]:
    clips = []
    # --- INTRO CLIP ---
    intro_text1 = "GUESS THE FLAGS!" if lang == "en" else "¡ADIVINA LAS BANDERAS!"
    intro_text2 = f"{elegida_categoria.upper()} EDITION" if lang == "en" else f"EDICIÓN {elegida_categoria.upper()}"

    # Texto con borde negro y letras blancas, posiciones personalizadas
    intro_clip1 = TextClip(
        intro_text1,
        fontsize=140,
        color="white",
        font=FONT_NAME,
        stroke_color="black",
        stroke_width=5,
        size=(VIDEO_SIZE[0], None),
        method="caption",
    ).set_position(("center", int(VIDEO_SIZE[1]*0.24))).set_duration(3.5)
    intro_clip2 = TextClip(
        intro_text2,
        fontsize=120,
        color=DIFFICULTY_COLORS[elegida_categoria],
        font=FONT_NAME,
        stroke_color="black",
        stroke_width=6,
        size=(VIDEO_SIZE[0], None),
        method="caption",
    ).set_position(("center", int(VIDEO_SIZE[1]*0.45))).set_duration(3.5)
    intro_clip = CompositeVideoClip([intro_clip1, intro_clip2], size=VIDEO_SIZE).set_duration(5.5)

    # --- VOZ TIKTOK PARA INTRO ---
    intro_tts_url = "https://tiktok-tts.weilnet.workers.dev/api/generation"
    intro_tts_response = requests.post(intro_tts_url, json={"text": intro_text1, "voice": tiktok_voice})
    intro_audio_path = "intro_tiktok.mp3"
    if intro_tts_response.status_code == 200 and intro_tts_response.json().get("data"):
        audio_data = base64.b64decode(intro_tts_response.json()["data"])
        with open(intro_audio_path, "wb") as f:
            f.write(audio_data)
    else:
        tts = gTTS(text=intro_text1, lang=FLAG_LANG)
        tts.save(intro_audio_path)
    intro_audio = AudioFileClip(intro_audio_path)

    # --- VOZ TIKTOK PARA DIFICULTAD ---
    diff_tts_response = requests.post(intro_tts_url, json={"text": intro_text2, "voice": tiktok_voice})
    diff_audio_path = "diff_tiktok.mp3"
    if diff_tts_response.status_code == 200 and diff_tts_response.json().get("data"):
        audio_data = base64.b64decode(diff_tts_response.json()["data"])
        with open(diff_audio_path, "wb") as f:
            f.write(audio_data)
    else:
        tts = gTTS(text=intro_text2, lang=FLAG_LANG)
        tts.save(diff_audio_path)
    diff_audio = AudioFileClip(diff_audio_path)

    # Calcular duración total de la intro (ambos audios uno tras otro)
    intro_total_duration = intro_audio.duration + diff_audio.duration
    # Hacer que la intro visual dure lo mismo que la suma de los audios
    intro_clip = intro_clip.set_duration(intro_total_duration)

    # Unir los audios en secuencia
    from moviepy.audio.AudioClip import concatenate_audioclips
    intro_audio_concat = concatenate_audioclips([intro_audio, diff_audio]).set_duration(intro_total_duration)
    intro_clip = intro_clip.set_audio(intro_audio_concat)

    clips = [intro_clip]

    # Generar clips de banderas/textos SIN fondo para cada segmento
    for f in selected_flags_info:
        path = f['path']
        country = f['name_' + lang]
        print(f"Procesando {country}...")
        img = Image.open(path).convert("RGB")
        img_ratio = img.width / img.height
        # Calcular tamaño máximo de la bandera con margen
        max_width = int(VIDEO_SIZE[0] * (1 - 2 * MARGIN_RATIO))
        max_height = int(VIDEO_SIZE[1] * (1 - 2 * MARGIN_RATIO))
        if img_ratio > (max_width / max_height):
            new_width = max_width
            new_height = int(new_width / img_ratio)
        else:
            new_height = max_height
            new_width = int(new_height * img_ratio)
        img = img.resize((new_width, new_height), Image.ANTIALIAS)
        img_no_text_path = f"temp_{country}_no_text.jpg"
        img.save(img_no_text_path)

        print(f"Imagen {country} cargada, redimensionada y ajustada con fondo negro y margen.")

        # Calcular la posición vertical de la bandera (flag_y)
        flag_y = int(VIDEO_SIZE[1] * 0.35) - (img.height // 2)
        # Ajustar tamaño y posición de la barra de progreso para que sea pequeña y justo debajo de la bandera
        bar_target_width = int(new_width * 0.7)  # 80% del ancho de la bandera
        bar_target_height = int(new_height * 0.7)  # Pequeña altura
        bar_x = int((VIDEO_SIZE[0] - bar_target_width) / 2)
        bar_y = flag_y + img.height + 20  # Justo debajo de la bandera
        bar_clip = VideoFileClip("resources/countdown_green.mp4")\
            .resize((bar_target_width, bar_target_height))\
            .set_position((bar_x, bar_y))\
            .set_duration(SHOW_DURATION)\
            .fx(vfx.mask_color, color=[8, 252, 20], thr=20, s=20)
        bar_clip = bar_clip.set_mask(bar_clip.mask)
        # Añadir sonido de tiempo pasando
        time_passing_audio = AudioFileClip("resources/time_passing.mp3").set_duration(SHOW_DURATION)
        clip1_img = CompositeVideoClip([
            ImageClip(img_no_text_path).set_duration(SHOW_DURATION).set_position(("center", flag_y)),
            bar_clip
        ], size=VIDEO_SIZE).set_audio(time_passing_audio)

        # Clip con texto usando TextClip (nombre de la bandera)
        text_clip = TextClip(
            country,
            fontsize=120,
            color="white",
            font=FONT_NAME,
            stroke_color="black",
            stroke_width=5,
            size=(VIDEO_SIZE[0], None),
            method="caption",
        ).set_position(("center", bar_y)).set_duration(GUESS_DURATION)  # Justo debajo de la barra
        
        clip2_img = ImageClip(img_no_text_path).set_duration(GUESS_DURATION).set_position(("center", flag_y))
        # Aseguramos que el text_clip esté en la capa inferior
        clip2 = CompositeVideoClip([clip2_img, text_clip], size=VIDEO_SIZE)

        # Voz del país usando TikTok TTS API
        tiktok_tts_url = "https://tiktok-tts.weilnet.workers.dev/api/generation"
        tts_response = requests.post(tiktok_tts_url, json={"text": country, "voice": tiktok_voice})
        if tts_response.status_code == 200 and tts_response.json().get("data"):
            import base64
            audio_data = base64.b64decode(tts_response.json()["data"])
            audio_path = f"{country}_tiktok.mp3"
            with open(audio_path, "wb") as f:
                f.write(audio_data)
        else:
            # Fallback a gTTS si falla la API
            from gtts import gTTS
            tts = gTTS(text=f"{country}", lang=FLAG_LANG)
            audio_path = f"{country}.mp3"
            tts.save(audio_path)
        audio = AudioSegment.from_file(audio_path)
        silence = AudioSegment.silent(duration=1000)
        audio_with_silence = audio + silence
        audio_with_silence.export(audio_path, format="mp3")
        audio = AudioFileClip(audio_path).set_duration(clip2.duration)
        # Sonido correcto
        correct_sound = AudioFileClip("resources/correct_beep.mp3").set_duration(clip2.duration)
        # Mezclar voz y sonido correcto
        clip2 = clip2.set_audio(CompositeAudioClip([audio, correct_sound]))
        print(f"Audio para {country} generado y añadido al clip.")
        # Concatenar: primero solo bandera, luego bandera+texto+audio
        final_clip = concatenate_videoclips([clip1_img, clip2])
        clips.append(final_clip)
        print(f"Clip para {country} generado y añadido a la lista.")


    # --- CLIP FINAL: Comment your score! ---
    final_text = "COMMENT YOUR SCORE!"
    final_score_placeholder = f"?/{NUM_FLAGS}"

    # Texto principal leído
    final_text_clip = TextClip(
        final_text,
        fontsize=120,
        color="white",
        font=FONT_NAME,
        stroke_color="black",
        stroke_width=5,
        size=(VIDEO_SIZE[0], None),
        method="caption",
    ).set_position(("center", int(VIDEO_SIZE[1] * 0.25)))

    # Texto visual de puntuación
    score_text_clip = TextClip(
        final_score_placeholder,
        fontsize=130,
        color="yellow",
        font=FONT_NAME,
        stroke_color="black",
        stroke_width=4,
        size=(VIDEO_SIZE[0], None),
        method="caption",
    ).set_position(("center", int(VIDEO_SIZE[1] * 0.45)))

    # Generar audio de TikTok
    score_audio_path = "final_comment.mp3"
    tts_response = requests.post(
        "https://tiktok-tts.weilnet.workers.dev/api/generation",
        json={"text": final_text, "voice": tiktok_voice}
    )

    if tts_response.status_code == 200 and tts_response.json().get("data"):
        audio_data = base64.b64decode(tts_response.json()["data"])
        with open(score_audio_path, "wb") as f:
            f.write(audio_data)
    else:
        tts = gTTS(text=final_text, lang=FLAG_LANG)
        tts.save(score_audio_path)

    # Cargar audio y configurar duración del clip
    final_audio = AudioFileClip(score_audio_path)
    final_duration = 2

    final_comment_clip = CompositeVideoClip(
        [final_text_clip.set_duration(final_duration), score_text_clip.set_duration(final_duration)],
        size=VIDEO_SIZE
    ).set_audio(final_audio)




    # Juntar todos los clips de banderas/textos
    video_flags = concatenate_videoclips(clips + [final_comment_clip])


    # Crear fondo animado global para toda la duración
    total_duration = video_flags.duration
    base_bg = VideoFileClip(BACKGROUND_FILE).without_audio()
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
