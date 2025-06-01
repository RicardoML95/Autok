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

from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

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
    flags = fetch_flags_and_names()
    save_flags_to_folder_by_category(flags, folder_path)