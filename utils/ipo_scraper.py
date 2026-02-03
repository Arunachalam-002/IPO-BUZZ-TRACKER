import pandas as pd
import os
from utils.dataset_loader import ensure_datasets

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
ensure_datasets(BASE_DIR)

IPO_CSV_PATH = os.path.join(BASE_DIR, "data", "IPO.csv")
NEWS_CSV_PATH = os.path.join(BASE_DIR, "data", "training_data_26000.csv")

# 🔥 GLOBAL CACHE
_CACHED_RESULT = None


def get_ipo_data():
    global _CACHED_RESULT
    if _CACHED_RESULT is not None:
        return _CACHED_RESULT

    # ---- Load data ONCE ----
    ipo_df = pd.read_csv(IPO_CSV_PATH)
    ipo_df.columns = [c.strip() for c in ipo_df.columns]

    news_df = pd.read_csv(NEWS_CSV_PATH)
    news_df.columns = [c.strip() for c in news_df.columns]

    # Preprocess ONCE
    news_df["Content"] = news_df["Content"].astype(str)
    news_df["Content_lower"] = news_df["Content"].str.lower()

    articles = []
    ipo_details_dict = {}

    for _, row in ipo_df.iterrows():
        ipo_name = str(row.get("IPO_Name", "")).strip()
        if not ipo_name:
            continue

        ipo_name_lower = ipo_name.lower()

        ipo_details_dict[ipo_name] = {
            "Date": row.get("Date", "N/A"),
            "Issue Size (Cr)": row.get("Issue_Size(crores)", "N/A"),
            "QIB": row.get("QIB", "N/A"),
            "HNI": row.get("HNI", "N/A"),
            "Retail": row.get("RII", "N/A"),
            "Total Subscription": "N/A",
            "Issue Price": row.get("Issue_price", "N/A"),
            "Listing Open": row.get("Listing_Open", "N/A"),
            "Listing Close": row.get("Listing_Close", "N/A"),
            "Listing Gain (%)": row.get("Listing_Gains(%)", "N/A"),
            "CMP": row.get("CMP", "N/A"),
            "Current Gain (%)": row.get("Current_gains", "N/A")
        }

        matched = news_df[
            news_df["Content_lower"].str.contains(ipo_name_lower, na=False)
        ]

        for _, art in matched.iterrows():
            articles.append({
                "IPO": ipo_name,
                "URL": art["URL"],
                "Content": art["Content"],
                "Summary": art["Summary"],
                "Sentiment": str(art["Sentiment"]).lower()
            })

    # 💾 Cache result
    _CACHED_RESULT = (articles, ipo_details_dict)
    return _CACHED_RESULT


def extract_ipo_names(articles):
    return sorted({a["IPO"] for a in articles})


def filter_articles_by_ipo(articles, ipo_name):
    ipo_name = ipo_name.lower()
    return [a for a in articles if a["IPO"].lower() == ipo_name]
