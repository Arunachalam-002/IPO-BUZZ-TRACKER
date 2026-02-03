import os
import sys
import pandas as pd
import pickle

# -------------------------------------------------
# FIX PYTHON PATH (CRITICAL FOR RENDER BUILD)
# -------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from utils.dataset_loader import ensure_datasets

# -------------------------------------------------
# PATHS
# -------------------------------------------------
DATA_DIR = os.path.join(BASE_DIR, "data")
IPO_CSV = os.path.join(DATA_DIR, "IPO.csv")
NEWS_CSV = os.path.join(DATA_DIR, "training_data_26000.csv")
CACHE_FILE = os.path.join(DATA_DIR, "precomputed.pkl")


def precompute():
    print("🔧 Ensuring datasets...")
    ensure_datasets(BASE_DIR)

    print("📖 Reading IPO.csv...")
    ipo_df = pd.read_csv(IPO_CSV)
    ipo_df.columns = [c.strip() for c in ipo_df.columns]

    print("📖 Reading training_data_26000.csv...")
    news_df = pd.read_csv(NEWS_CSV)
    news_df.columns = [c.strip() for c in news_df.columns]

    # Preprocess once
    news_df["Content"] = news_df["Content"].astype(str)
    news_df["content_lower"] = news_df["Content"].str.lower()

    articles = []
    ipo_details = {}

    print("⚙️ Precomputing IPO-news mapping...")

    for _, row in ipo_df.iterrows():
        ipo_name = str(row.get("IPO_Name", "")).strip()
        if not ipo_name:
            continue

        ipo_lower = ipo_name.lower()

        ipo_details[ipo_name] = {
            "Date": row.get("Date", "N/A"),
            "Issue Size (Cr)": row.get("Issue_Size(crores)", "N/A"),
            "QIB": row.get("QIB", "N/A"),
            "HNI": row.get("HNI", "N/A"),
            "Retail": row.get("RII", "N/A"),
            "Issue Price": row.get("Issue_price", "N/A"),
            "Listing Gain (%)": row.get("Listing_Gains(%)", "N/A"),
        }

        matched = news_df[
            news_df["content_lower"].str.contains(ipo_lower, na=False)
        ]

        for _, art in matched.iterrows():
            articles.append({
                "IPO": ipo_name,
                "URL": art.get("URL", ""),
                "Content": art.get("Content", ""),
                "Summary": art.get("Summary", ""),
                "Sentiment": str(art.get("Sentiment", "neutral")).lower()
            })

    print("💾 Saving precomputed cache...")
    with open(CACHE_FILE, "wb") as f:
        pickle.dump((articles, ipo_details), f)

    print("✅ Precomputation finished successfully!")


if __name__ == "__main__":
    precompute()
