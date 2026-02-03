from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment(articles):
    """
    Estimate sentiment based on article-level sentiment labels.
    Input: list of article dicts (each must have 'Sentiment': positive/neutral/negative)
    Output: sentiment score dict with counts and estimated compound score
    """
    counts = {"positive": 0, "neutral": 0, "negative": 0}
    total = 0

    for article in articles:
        sentiment = article.get('Sentiment', '').lower()
        if sentiment in counts:
            counts[sentiment] += 1
            total += 1

    if total == 0:
        return {"positive": 0.0, "neutral": 1.0, "negative": 0.0, "compound": 0.0}

    # Normalize to percentages
    pos = counts['positive'] / total
    neu = counts['neutral'] / total
    neg = counts['negative'] / total

    # Heuristic compound score: positive - negative
    compound = round(pos - neg, 2)

    return {
        "positive": round(pos, 2),
        "neutral": round(neu, 2),
        "negative": round(neg, 2),
        "compound": compound
    }

