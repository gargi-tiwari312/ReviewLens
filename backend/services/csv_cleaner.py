
import pandas as pd
import os


def clean_reviews(filepath):

    # Read CSV file
    df = pd.read_csv(filepath)

    original_count = len(df)

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Remove missing review text
    df = df.dropna(subset=["review_text"])

    # Remove empty reviews
    df["review_text"] = df["review_text"].astype(str).str.strip()
    df = df[df["review_text"] != ""]

    # Remove extra spaces
    df["review_text"] = df["review_text"].str.replace(
        r"\s+", " ", regex=True
    )

    cleaned_count = len(df)

    removed_count = original_count - cleaned_count

    # Save cleaned CSV
    output_path = "data/cleaned_reviews.csv"
    df.to_csv(output_path, index=False)

    return {
        "original_count": original_count,
        "cleaned_count": cleaned_count,
        "removed_count": removed_count,
        "output_path": output_path
    }
