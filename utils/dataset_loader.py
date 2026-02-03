import os
import gdown

DATASETS = {
    "training_data_26000.csv": "1kDX3QBavqA_tY7KNfR4nnjGuZmZCc2Mh",
    "IPO.csv": "1Vv89WmLn9xmRZds92KJoIhtfO9y0Y66u"
}

def ensure_datasets(base_dir):
    data_dir = os.path.join(base_dir, "data")
    os.makedirs(data_dir, exist_ok=True)

    for filename, file_id in DATASETS.items():
        file_path = os.path.join(data_dir, filename)

        # Force re-download if wrong file exists
        if os.path.exists(file_path):
            os.remove(file_path)

        print(f"⬇️ Downloading {filename} from Google Drive using gdown...")
        gdown.download(
            id=file_id,
            output=file_path,
            quiet=False,
            fuzzy=True
        )

        if not os.path.exists(file_path) or os.path.getsize(file_path) < 1000:
            raise RuntimeError(f"Failed to download {filename}")

        print(f"✅ {filename} downloaded successfully")
