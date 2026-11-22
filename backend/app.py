
from flask import Flask, request, jsonify, render_template, redirect
from flask_cors import CORS
from backend.services.sentiment import analyze_sentiment
from backend.services.insights import generate_insights

import os
import pandas as pd


# ==========================================
# PROJECT PATHS
# ==========================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TEMPLATE_DIR = os.path.join(BASE_DIR, "frontend", "templates")
STATIC_DIR = os.path.join(BASE_DIR, "frontend", "static")
DATA_DIR = os.path.join(BASE_DIR, "data")

os.makedirs(DATA_DIR, exist_ok=True)


# ==========================================
# FLASK APPLICATION
# ==========================================

app = Flask(
    __name__,
    template_folder=TEMPLATE_DIR,
    static_folder=STATIC_DIR
)

CORS(app)


# ==========================================
# HOME ROUTE
# ==========================================

@app.route("/")
def home():
    return redirect("/dashboard")


# ==========================================
# GRAPHICAL DASHBOARD
# ==========================================

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


# ==========================================
# CSV UPLOAD + SENTIMENT ANALYSIS
# ==========================================

@app.route("/analyze", methods=["POST"])
def analyze():

    try:

        if "file" not in request.files:
            return jsonify({
                "error": "No CSV file uploaded"
            }), 400

        file = request.files["file"]

        if file.filename == "":
            return jsonify({
                "error": "No file selected"
            }), 400

        if not file.filename.lower().endswith(".csv"):
            return jsonify({
                "error": "Please upload a CSV file"
            }), 400

        df = pd.read_csv(file)

        required_columns = [
            "review_id",
            "product",
            "rating",
            "date",
            "review_text"
        ]

        for column in required_columns:

            if column not in df.columns:
                return jsonify({
                    "error": f"Missing column: {column}"
                }), 400

        # Clean ratings
        df["rating"] = pd.to_numeric(
            df["rating"],
            errors="coerce"
        )

        df = df.dropna(subset=["rating"])

        df = df[
            df["rating"].between(1, 5)
        ].copy()

        # Handle missing review text
        df["review_text"] = (
            df["review_text"]
            .fillna("")
            .astype(str)
        )

        # Apply sentiment analysis
        sentiment_results = df["review_text"].apply(
            analyze_sentiment
        )

        df["sentiment"] = sentiment_results.apply(
            lambda result: result["sentiment"]
        )

        df["compound_score"] = sentiment_results.apply(
            lambda result: result["compound_score"]
        )

        # Save analyzed CSV
        filepath = os.path.join(
            DATA_DIR,
            "analyzed_reviews.csv"
        )

        df.to_csv(filepath, index=False)

        # Sentiment counts
        sentiment_counts = {
            "Positive": int(
                (df["sentiment"] == "Positive").sum()
            ),

            "Negative": int(
                (df["sentiment"] == "Negative").sum()
            ),

            "Neutral": int(
                (df["sentiment"] == "Neutral").sum()
            )
        }

        return jsonify({
            "message": "CSV uploaded and sentiment analysis completed",
            "total_reviews": len(df),
            "sentiment_counts": sentiment_counts,
            "status": "success"
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# ==========================================
# DASHBOARD DATA API
# ==========================================

@app.route("/api/dashboard", methods=["GET"])
def dashboard_data():

    try:

        filepath = os.path.join(
            DATA_DIR,
            "analyzed_reviews.csv"
        )

        if not os.path.exists(filepath):
            return jsonify({
                "error": "No review data found. Please upload CSV first."
            }), 404

        df = pd.read_csv(filepath)

        df["rating"] = pd.to_numeric(
            df["rating"],
            errors="coerce"
        )

        df = df.dropna(subset=["rating"])

        df = df[
            df["rating"].between(1, 5)
        ].copy()

        if df.empty:
            return jsonify({
                "error": "No valid review data found"
            }), 400

        # Overall statistics
        total_reviews = len(df)

        average_rating = round(
            float(df["rating"].mean()),
            2
        )

        # Rating-based counts
        positive_reviews = int(
            (df["rating"] >= 4).sum()
        )

        negative_reviews = int(
            (df["rating"] <= 2).sum()
        )

        neutral_reviews = int(
            (df["rating"] == 3).sum()
        )

        # Rating distribution
        rating_distribution = {
            str(int(key)): int(value)
            for key, value in
            df["rating"].value_counts().sort_index().items()
        }

        # Product summary
        product_summary = (
            df.groupby("product")
            .agg(
                total_reviews=("rating", "count"),
                average_rating=("rating", "mean")
            )
            .round(2)
            .reset_index()
            .to_dict(orient="records")
        )

        # Text-based sentiment counts
        if "sentiment" not in df.columns:

            sentiment_results = (
                df["review_text"]
                .fillna("")
                .apply(analyze_sentiment)
            )

            df["sentiment"] = sentiment_results.apply(
                lambda result: result["sentiment"]
            )

            df["compound_score"] = sentiment_results.apply(
                lambda result: result["compound_score"]
            )

        sentiment_counts = {
            "Positive": int(
                (df["sentiment"] == "Positive").sum()
            ),

            "Negative": int(
                (df["sentiment"] == "Negative").sum()
            ),

            "Neutral": int(
                (df["sentiment"] == "Neutral").sum()
            )
        }

        return jsonify({

            "total_reviews": total_reviews,

            "average_rating": average_rating,

            "positive_reviews": positive_reviews,

            "negative_reviews": negative_reviews,

            "neutral_reviews": neutral_reviews,

            "rating_distribution": rating_distribution,

            "product_summary": product_summary,

            "sentiment_counts": sentiment_counts

        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# ==========================================
# AI REVIEW INSIGHTS API
# ==========================================

@app.route("/api/insights", methods=["GET"])
def review_insights():

    try:

        filepath = os.path.join(
            DATA_DIR,
            "analyzed_reviews.csv"
        )

        if not os.path.exists(filepath):
            return jsonify({
                "error": "Please upload a CSV file first."
            }), 404

        df = pd.read_csv(filepath)

        if df.empty:
            return jsonify({
                "error": "No reviews available."
            }), 400

        # Generate insights
        insights = generate_insights(df)

        return jsonify({

            "status": "success",

            "insights": insights

        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# ==========================================
# RUN APPLICATION
# ==========================================

if __name__ == "__main__":

    app.run(
        debug=True,
        port=5000
    )
