from flask import Flask, render_template, request
from urllib.parse import unquote
import os
import re

from utils.ipo_scraper import get_ipo_data, extract_ipo_names, filter_articles_by_ipo
from utils.sentiment_analyzer import analyze_sentiment
from utils.visualizer import generate_wordcloud

app = Flask(__name__)
app.config['WORDCLOUD_FOLDER'] = 'static/wordclouds'

def normalize(text):
    return re.sub(r'[^a-z0-9]', '', text.lower())

@app.route('/')
def index():
    articles, _ = get_ipo_data()
    ipo_names = extract_ipo_names(articles)
    return render_template("index.html", ipo_names=ipo_names)

@app.route('/ipo/<path:ipo_name>')
def ipo_detail(ipo_name):
    ipo_name = unquote(ipo_name)
    articles, ipo_details_dict = get_ipo_data()
    filtered_articles = filter_articles_by_ipo(articles, ipo_name)
    sentiment = analyze_sentiment(filtered_articles)

    os.makedirs(app.config['WORDCLOUD_FOLDER'], exist_ok=True)
    wc_filename = f"{ipo_name.replace(' ', '_')}.png"
    wc_path = os.path.join(app.config['WORDCLOUD_FOLDER'], wc_filename)
    generate_wordcloud(filtered_articles, save_path=wc_path)

    ipo_details = ipo_details_dict.get(ipo_name, {})

    return render_template("ipo_detail.html",
                           ipo_name=ipo_name,
                           ipo_details=ipo_details,
                           wordcloud_filename=wc_filename,
                           sentiment=sentiment)

@app.route('/ipo/<path:ipo_name>/articles')
def ipo_articles(ipo_name):
    ipo_name = unquote(ipo_name)
    articles, _ = get_ipo_data()
    filtered_articles = filter_articles_by_ipo(articles, ipo_name)
    return render_template("ipo_articles.html", ipo_name=ipo_name, articles=filtered_articles)

@app.route('/ipo/<path:ipo_name>/chat', methods=['GET', 'POST'])
def ipo_chatbot(ipo_name):
    ipo_name = unquote(ipo_name)
    _, ipo_details_dict = get_ipo_data()
    ipo_details = ipo_details_dict.get(ipo_name, {})
    chatbot_answer = ""

    if request.method == 'POST':
        query = request.form.get("query", "").lower()

        keyword_map = {
            "Date": ["open date", "date"],
            "Issue Size (Cr)": ["issue size", "total size"],
            "QIB": ["qib", "qualified"],
            "HNI": ["hni", "non-institutional"],
            "Retail": ["retail", "rii"],
            "Total Subscription": ["subscription", "total subscribed"],
            "Issue Price": ["issue price", "price band", "price"],
            "Listing Open": ["listing open", "opening price"],
            "Listing Close": ["listing close", "closing price"],
            "Listing Gain (%)": ["gain", "listing gain", "profit"],
            "CMP": ["cmp", "current market price"],
            "Current Gain (%)": ["current gain", "current return"]
        }

        matched = False
        for field, keywords in keyword_map.items():
            if any(k in query for k in keywords):
                value = ipo_details.get(field)
                if value:
                    chatbot_answer = f"{field}: {value}"
                    matched = True
                    break

        if not matched:
            chatbot_answer = "❌ Sorry, I couldn't find an answer. Try asking about open date, CMP, listing gains, issue price, etc."

    return render_template("ipo_chatbot.html", ipo_name=ipo_name, chatbot_answer=chatbot_answer)

if __name__ == '__main__':
    app.run(debug=True)
