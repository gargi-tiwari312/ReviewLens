
import pandas as pd


def analyze_sentiment(review):

    review = str(review).lower()

    positive_words = [
        "good", "great", "excellent", "amazing",
        "love", "happy", "best", "wonderful",
        "soft", "worth", "perfect", "beautiful",
        "comfortable", "satisfied", "awesome"
    ]

    negative_words = [
        "bad", "poor", "worst", "terrible",
        "hate", "wrong", "damage", "defective",
        "disappointed", "problem", "late",
        "broken", "waste", "faded", "missing"
    ]

    positive_count = sum(
        1 for word in positive_words
        if word in review
    )

    negative_count = sum(
        1 for word in negative_words
        if word in review
    )

    if positive_count > negative_count:
        return "Positive"

    elif negative_count > positive_count:
        return "Negative"

    else:
        return "Neutral"


def analyze_reviews(filepath):

    df = pd.read_csv(filepath)

    df["sentiment"] = df["review_text"].apply(
        analyze_sentiment
    )

    output_path = "data/analyzed_reviews.csv"

    df.to_csv(output_path, index=False)

    sentiment_counts = df["sentiment"].value_counts()

    return {
        "total_reviews": len(df),
        "positive": int(sentiment_counts.get("Positive", 0)),
        "negative": int(sentiment_counts.get("Negative", 0)),
        "neutral": int(sentiment_counts.get("Neutral", 0)),
        "output_path": output_path
    }
