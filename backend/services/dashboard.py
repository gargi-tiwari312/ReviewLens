
import pandas as pd


def get_dashboard_data(filepath):

    df = pd.read_csv(filepath)

    # Total reviews
    total_reviews = len(df)

    # Sentiment counts
    sentiment_counts = df["sentiment"].value_counts()

    positive = int(sentiment_counts.get("Positive", 0))
    negative = int(sentiment_counts.get("Negative", 0))
    neutral = int(sentiment_counts.get("Neutral", 0))

    # Sentiment percentages
    positive_percent = round((positive / total_reviews) * 100, 2) if total_reviews else 0
    negative_percent = round((negative / total_reviews) * 100, 2) if total_reviews else 0
    neutral_percent = round((neutral / total_reviews) * 100, 2) if total_reviews else 0

    # Product-wise review count
    product_reviews = (
        df.groupby("product")
        .size()
        .to_dict()
    )

    # Average rating by product
    average_ratings = (
        df.groupby("product")["rating"]
        .mean()
        .round(2)
        .to_dict()
    )

    return {
        "total_reviews": total_reviews,
        "positive": positive,
        "negative": negative,
        "neutral": neutral,
        "positive_percent": positive_percent,
        "negative_percent": negative_percent,
        "neutral_percent": neutral_percent,
        "product_reviews": product_reviews,
        "average_ratings": average_ratings
    }
