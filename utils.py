import requests
from transformers import pipeline
import spacy
import pandas as pd
from gtts import gTTS
import os
from dotenv import load_dotenv
from translate import Translator

load_dotenv()
api_key = os.getenv("NEWS_API_KEY")

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
print("bart-large-cnn loaded")
sentiment_pipeline = pipeline("sentiment-analysis")
print("sentiment-analysis loaded")
nlp = spacy.load("en_core_web_sm")
print("en_core_web_sm loaded")


def fetch_news(company):
    url = f"https://newsapi.org/v2/everything?q={company}&apiKey={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        articles = response.json().get("articles", [])[:10]
        for article in articles:
            if "title" not in article:
                article["title"] = "No Title Available"
            if "content" not in article:
                article["content"] = ""
        return articles
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching news: {e}")
        return []


def summarize_text(text):
    if text:
        summary = summarizer(text, max_length=130, min_length=30, do_sample=False)[0][
            "summary_text"
        ]
        return summary
    return "No content available for summarization."


def analyze_sentiment(text):
    if text:
        result = sentiment_pipeline(text)[0]
        return result["label"]
    return "Neutral"


def extract_topics(text):
    if text:
        doc = nlp(text)
        return list(set([ent.text for ent in doc.ents]))
    return []


def comparative_analysis(articles):
    df = pd.DataFrame(articles)
    sentiment_distribution = df["Sentiment"].value_counts().to_dict()

    coverage_differences = []
    for i in range(len(articles) - 1):
        coverage_differences.append(
            {
                "Comparison": f"Article {i + 1} vs Article {i + 2}",
                "Impact": f"{articles[i]['title']} focuses on {articles[i]['Topics']}, "
                f"while {articles[i + 1]['title']} focuses on {articles[i + 1]['Topics']}.",
            }
        )

    common_topics = set(articles[0]["Topics"]).intersection(set(articles[1]["Topics"]))
    unique_topics_1 = set(articles[0]["Topics"]).difference(set(articles[1]["Topics"]))
    unique_topics_2 = set(articles[1]["Topics"]).difference(set(articles[0]["Topics"]))

    return {
        "Sentiment Distribution": sentiment_distribution,
        "Coverage Differences": coverage_differences,
        "Topic Overlap": {
            "Common Topics": list(common_topics),
            "Unique Topics in Article 1": list(unique_topics_1),
            "Unique Topics in Article 2": list(unique_topics_2),
        },
    }


def split_text(text, max_length=500):
    """Split text into chunks of a maximum length."""
    words = text.split()
    chunks = []
    current_chunk = []

    for word in words:
        if len(" ".join(current_chunk + [word])) <= max_length:
            current_chunk.append(word)
        else:
            chunks.append(" ".join(current_chunk))
            current_chunk = [word]

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


def generate_tts(text):
    translator = Translator(to_lang="hi")
    chunks = split_text(text)
    translated_chunks = [translator.translate(chunk) for chunk in chunks]
    translated_text = " ".join(translated_chunks)
    tts = gTTS(text=translated_text, lang="hi")
    tts.save("output.mp3")
    return "output.mp3"
