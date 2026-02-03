import os
import sys
import pickle

# -------------------------------------------------
# FIX PYTHON PATH (CRITICAL FOR RENDER RUNTIME)
# -------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

CACHE_FILE = os.path.join(BASE_DIR, "data", "precomputed.pkl")


def get_ipo_data():
    if not os.path.exists(CACHE_FILE):
        raise RuntimeError("❌ Precomputed cache not found. Build step may have failed.")

    with open(CACHE_FILE, "rb") as f:
        return pickle.load(f)


def extract_ipo_names(articles):
    return sorted({a["IPO"] for a in articles})


def filter_articles_by_ipo(articles, ipo_name):
    ipo_name = ipo_name.lower()
    return [a for a in articles if a["IPO"].lower() == ipo_name]
