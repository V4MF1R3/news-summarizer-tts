from flask import Flask, request, jsonify
from utils import (
    fetch_news,
    summarize_text,
    analyze_sentiment,
    extract_topics,
    comparative_analysis,
    generate_tts,
)

app = Flask(__name__)


@app.route("/get_news", methods=["GET"])
def get_news():
    company = request.args.get("company")
    articles = fetch_news(company)

    for article in articles:
        content = article.get("content", "")
        article["Summary"] = summarize_text(content)
        article["Sentiment"] = analyze_sentiment(content)
        article["Topics"] = extract_topics(content)

    analysis = comparative_analysis(articles)

    # Create a summary of the sentiment report in English
    sentiment_summary = f"Sentiment analysis for {company}: "
    sentiment_summary += (
        f"Positive: {analysis['Sentiment Distribution'].get('Positive', 0)}, "
    )
    sentiment_summary += (
        f"Negative: {analysis['Sentiment Distribution'].get('Negative', 0)}, "
    )
    sentiment_summary += (
        f"Neutral: {analysis['Sentiment Distribution'].get('Neutral', 0)}. "
    )
    sentiment_summary += "Coverage differences: "
    for difference in analysis["Coverage Differences"]:
        sentiment_summary += f"{difference['Comparison']} - {difference['Impact']}. "
    sentiment_summary += (
        "Common topics: " + ", ".join(analysis["Topic Overlap"]["Common Topics"]) + ". "
    )
    sentiment_summary += (
        "Unique topics in Article 1: "
        + ", ".join(analysis["Topic Overlap"]["Unique Topics in Article 1"])
        + ". "
    )
    sentiment_summary += (
        "Unique topics in Article 2: "
        + ", ".join(analysis["Topic Overlap"]["Unique Topics in Article 2"])
        + ". "
    )

    # Generate TTS in Hindi
    tts_file = generate_tts(sentiment_summary)

    response = {
        "Company": company,
        "Articles": articles,
        "Comparative Analysis": analysis,
        "Audio": tts_file,
    }
    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True)
