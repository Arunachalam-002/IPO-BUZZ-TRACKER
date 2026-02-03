import pandas as pd
import os
from utils.dataset_loader import ensure_datasets

# ------------------ PATH SETUP ------------------
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
ensure_datasets(BASE_DIR)

IPO_CSV_PATH = os.path.join(BASE_DIR, "data", "IPO.csv")
NEWS_CSV_PATH = os.path.join(BASE_DIR, "data", "training_data_26000.csv")


# ------------------ CORE LOGIC ------------------
def get_ipo_data():
    # ---- Load IPO data ----
    if not os.path.exists(IPO_CSV_PATH):
        raise FileNotFoundError("IPO.csv not found after download")

    ipo_df = pd.read_csv(IPO_CSV_PATH)
    ipo_df.columns = [col.strip() for col in ipo_df.columns]

    # ---- Load News data ----
    if not os.path.exists(NEWS_CSV_PATH):
        raise FileNotFoundError("training_data_26000.csv not found after download")

    news_df = pd.read_csv(NEWS_CSV_PATH)
    news_df.columns = [col.strip() for col in news_df.columns]

    # ---- Validate required columns ----
    required_cols = {"Content", "URL", "Summary", "Sentiment"}
    if not required_cols.issubset(set(news_df.columns)):
        raise ValueError(
            f"Expected columns {required_cols}, but found {news_df.columns.tolist()}"
        )

    # ---- Filter IPO-related news ----
    news_df = news_df[
        news_df["Content"].str.contains("IPO", case=False, na=False)
    ]

    articles = []
    ipo_details_dict = {}

    # ---- Process IPOs ----
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

        # ---- Match articles for this IPO ----
        matching_articles = news_df[
            news_df["Content"].str.lower().str.contains(ipo_name_lower, na=False)
        ]

        for _, art in matching_articles.iterrows():
            articles.append({
                "IPO": ipo_name,
                "URL": art["URL"],
                "Content": art["Content"],
                "Summary": art["Summary"],
                "Sentiment": str(art["Sentiment"]).lower()
            })

    return articles, ipo_details_dict


# ------------------ HELPERS ------------------
def extract_ipo_names(articles):
    return sorted({a["IPO"] for a in articles if "IPO" in a})


def filter_articles_by_ipo(articles, ipo_name):
    return [
        a for a in articles
        if a.get("IPO", "").lower() == ipo_name.lower()
    ]
