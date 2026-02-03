import os
import requests

DATASETS = {
    "training_data_26000.csv": "https://drive.google.com/uc?export=download&id=1kDX3QBavqA_tY7KNfR4nnjGuZmZCc2Mh",
    "IPO.csv": "https://drive.google.com/uc?export=download&id=1Vv89WmLn9xmRZds92KJoIhtfO9y0Y66u"
}

def download_file(url, path):
    r = requests.get(url, stream=True)
    r.raise_for_status()
    with open(path, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)

def ensure_datasets(base_dir):
    data_dir = os.path.join(base_dir, "data")
    os.makedirs(data_dir, exist_ok=True)

    for filename, url in DATASETS.items():
        file_path = os.path.join(data_dir, filename)
        if not os.path.exists(file_path):
            print(f"⬇️ Downloading {filename}...")
            download_file(url, file_path)
            print(f"✅ {filename} downloaded")
        else:
            print(f"✔ {filename} already exists")
