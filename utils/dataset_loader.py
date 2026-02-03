import os
import requests
import re

DATASETS = {
    "training_data_26000.csv": "https://drive.google.com/uc?export=download&id=1kDX3QBavqA_tY7KNfR4nnjGuZmZCc2Mh",
    "IPO.csv": "https://drive.google.com/uc?export=download&id=1Vv89WmLn9xmRZds92KJoIhtfO9y0Y66u"
}

def _get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith("download_warning"):
            return value
    return None

def _save_response_content(response, destination):
    with open(destination, "wb") as f:
        for chunk in response.iter_content(32768):
            if chunk:
                f.write(chunk)

def download_from_google_drive(url, destination):
    session = requests.Session()

    response = session.get(url, stream=True)
    token = _get_confirm_token(response)

    if token:
        params = {"confirm": token}
        response = session.get(url, params=params, stream=True)

    # 🔴 SAFETY CHECK: stop if HTML is downloaded
    content_type = response.headers.get("Content-Type", "")
    if "text/html" in content_type.lower():
        raise RuntimeError("Google Drive returned HTML instead of CSV. Download blocked.")

    _save_response_content(response, destination)

def ensure_datasets(base_dir):
    data_dir = os.path.join(base_dir, "data")
    os.makedirs(data_dir, exist_ok=True)

    for filename, url in DATASETS.items():
        path = os.path.join(data_dir, filename)

        if os.path.exists(path) and os.path.getsize(path) > 0:
            print(f"✔ {filename} already exists")
            continue

        print(f"⬇️ Downloading {filename} from Google Drive...")
        download_from_google_drive(url, path)
        print(f"✅ {filename} downloaded successfully")
