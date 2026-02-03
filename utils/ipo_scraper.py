import pickle
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CACHE_FILE = os.path.join(BASE_DIR, "data", "precomputed.pkl")

def get_ipo_data():
    if not os.path.exists(CACHE_FILE):
        raise RuntimeError("Precomputed data not found")

    with open(CACHE_FILE, "rb") as f:
        return pickle.load(f)

def extract_ipo_names(articles):
    return sorted({a["IPO"] for a in articles})

def filter_articles_by_ipo(articles, ipo_name):
    ipo_name = ipo_name.lower()
    return [a for a in articles if a["IPO"].lower() == ipo_name]
