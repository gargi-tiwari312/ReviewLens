
from collections import Counter
import re


def generate_insights(df):

    if df.empty:
        return {
            "common_complaints": [],
            "appreciated_features": [],
            "improvement_suggestions": [],
            "summary": "No reviews available."
        }

    # ==========================================
    # 1. SEPARATE POSITIVE AND NEGATIVE REVIEWS
    # ==========================================

    positive_reviews = df[
        df["sentiment"] == "Positive"
    ]["review_text"].dropna().astype(str).tolist()

    negative_reviews = df[
        df["sentiment"] == "Negative"
    ]["review_text"].dropna().astype(str).tolist()

    neutral_count = len(df[
        df["sentiment"] == "Neutral"
    ])

    # ==========================================
    # 2. STOP WORDS
    # ==========================================

    stop_words = {
        "the", "is", "and", "a", "an", "to", "of",
        "it", "this", "that", "was", "for", "with",
        "but", "very", "not", "my", "i", "in",
        "on", "after", "have", "has", "are", "be",
        "its", "they", "you", "we", "so", "too",
        "as", "at", "from", "did", "do", "me",
        "them", "all", "days", "never", "also",
        "been", "being", "were", "will", "would",
        "could", "should", "can", "cannot", "dont",
        "does", "doesnt", "didnt", "had", "having",
        "their", "there", "then", "than", "when",
        "where", "what", "which", "who", "why",
        "how", "if", "or", "by", "about", "into",
        "out", "up", "down", "over", "under",
        "just", "only", "some", "any", "much",
        "many", "more", "most", "such", "own",
        "same", "other", "each", "every", "both",
        "few", "again", "once", "here", "while",
        "during", "before", "because", "although",
        "though", "however", "still", "even",
        "really", "quite", "well", "got", "get",
        "make", "made", "one", "two", "three",
        "product", "products", "item", "items",
        "customer", "review", "reviews",
        "instructions", "thing", "things",
        "ordered", "order", "bought", "buy"
    }

    # Generic sentiment words are not useful as product features
    generic_words = {
        "good", "great", "bad", "best", "worst",
        "nice", "awesome", "excellent", "amazing",
        "perfect", "poor", "okay", "ok", "love",
        "loved", "like", "liked", "disappointed"
    }

    # ==========================================
    # 3. KEYWORD EXTRACTION
    # ==========================================

    def extract_keywords(reviews):

        words = []

        for review in reviews:

            tokens = re.findall(
                r"\b[a-zA-Z]{3,}\b",
                review.lower()
            )

            for word in tokens:

                if (
                    word not in stop_words
                    and word not in generic_words
                ):
                    words.append(word)

        return Counter(words).most_common(5)

    complaints = extract_keywords(negative_reviews)

    appreciated = extract_keywords(positive_reviews)

    # ==========================================
    # 4. IMPROVEMENT SUGGESTIONS
    # ==========================================

    suggestions = []

    # Extract all words from negative reviews
    negative_text = " ".join(negative_reviews).lower()

    complaint_words = set(
        re.findall(r"\b[a-zA-Z]+\b", negative_text)
    )

    # Product Quality
    quality_words = {
        "quality", "damaged", "broken", "defect",
        "defective", "durability", "fabric",
        "material", "poor"
    }

    if complaint_words.intersection(quality_words):
        suggestions.append(
            "Improve product quality, material and durability."
        )

    # Delivery
    delivery_words = {
        "delivery", "delivered", "shipping",
        "shipment", "arrived", "arrival",
        "late", "delay", "delayed", "courier"
    }

    if complaint_words.intersection(delivery_words):
        suggestions.append(
            "Improve delivery speed and shipping services."
        )

    # Product Size
    size_words = {
        "size", "small", "large", "fit",
        "fitting", "tight", "loose", "wrong"
    }

    if complaint_words.intersection(size_words):
        suggestions.append(
            "Provide accurate product size information and sizing options."
        )

    # Pricing
    price_words = {
        "price", "expensive", "cost",
        "costly", "overpriced", "pricing"
    }

    if complaint_words.intersection(price_words):
        suggestions.append(
            "Review product pricing and value for money."
        )

    # Product Performance
    performance_words = {
        "battery", "sound", "connection",
        "connectivity", "charging", "charge",
        "performance", "functionality"
    }

    if complaint_words.intersection(performance_words):
        suggestions.append(
            "Improve product performance and functionality."
        )

    # Default Suggestions
    if not suggestions and negative_reviews:
        suggestions.append(
            "Review negative customer feedback to identify product improvements."
        )

    if not negative_reviews:
        suggestions.append(
            "Maintain current product quality and customer satisfaction."
        )

    # ==========================================
    # 5. OVERALL SUMMARY
    # ==========================================

    total = len(df)

    positive_count = len(positive_reviews)
    negative_count = len(negative_reviews)

    if positive_count > negative_count:

        summary = (
            f"Overall customer feedback is mostly positive. "
            f"Out of {total} reviews, {positive_count} are positive, "
            f"{negative_count} are negative and "
            f"{neutral_count} are neutral."
        )

    elif negative_count > positive_count:

        summary = (
            f"Customer feedback indicates areas that need improvement. "
            f"Out of {total} reviews, {positive_count} are positive, "
            f"{negative_count} are negative and "
            f"{neutral_count} are neutral."
        )

    else:

        summary = (
            f"Customer feedback is mixed or balanced. "
            f"Out of {total} reviews, {positive_count} are positive, "
            f"{negative_count} are negative and "
            f"{neutral_count} are neutral."
        )

    # ==========================================
    # 6. RETURN INSIGHTS
    # ==========================================

    return {
        "common_complaints": complaints,
        "appreciated_features": appreciated,
        "improvement_suggestions": suggestions,
        "summary": summary
    }
