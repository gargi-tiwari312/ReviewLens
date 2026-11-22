from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()


def analyze_sentiment(review_text):

    scores = analyzer.polarity_scores(str(review_text))

    compound_score = scores["compound"]

    if compound_score >= 0.05:
        sentiment = "Positive"

    elif compound_score <= -0.05:
        sentiment = "Negative"

    else:
        sentiment = "Neutral"

    return {
        "sentiment": sentiment,
        "compound_score": compound_score
    }