from wordcloud import WordCloud

def generate_wordcloud(articles, save_path):
    # Extract summaries from article dicts
    texts = [article.get('Summary', '') for article in articles if 'Summary' in article]

    # Join all summaries into one string
    combined_text = " ".join(texts)

    # Generate and save the word cloud
    wc = WordCloud(width=800, height=400, background_color="white").generate(combined_text)
    wc.to_file(save_path)
