import pandas as pd
import os
import pickle
from utils.dataset_loader import ensure_datasets

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

IPO_CSV = os.path.join(DATA_DIR, "IPO.csv")
NEWS_CSV = os.path.join(DATA_DIR, "training_data_26000.csv")
CACHE_FILE = os.path.join(DATA_DIR, "precomputed.pkl")

def precompute():
    ensure_datasets(BASE_DIR)

    ipo_df = pd.read_csv(IPO_CSV)
    news_df = pd.read_csv(NEWS_CSV)

    news_df["Content"] = news_df["Content"].astype(str)
    news_df["content_lower"] = news_df["Content"].str.lower()

    articles = []
    ipo_details = {}

    for _, row in ipo_df.iterrows():
        ipo = str(row["IPO_Name"]).strip()
        if not ipo:
            continue

        ipo_lower = ipo.lower()

        ipo_details[ipo] = {
            "Date": row.get("Date", "N/A"),
            "Issue Size (Cr)": row.get("Issue_Size(crores)", "N/A"),
            "QIB": row.get("QIB", "N/A"),
            "HNI": row.get("HNI", "N/A"),
            "Retail": row.get("RII", "N/A"),
        }

        matched = news_df[news_df["content_lower"].str.contains(ipo_lower, na=False)]

        for _, art in matched.iterrows():
            articles.append({
                "IPO": ipo,
                "URL": art["URL"],
                "Content": art["Content"],
                "Summary": art["Summary"],
                "Sentiment": art["Sentiment"]
            })

    with open(CACHE_FILE, "wb") as f:
        pickle.dump((articles, ipo_details), f)

    print("✅ Precomputation finished and cached")

if __name__ == "__main__":
    precompute()
