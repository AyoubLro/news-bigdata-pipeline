import pandas as pd
import glob
import os
import re
from collections import Counter

from storage.upload import upload_to_minio


def load_latest_silver():
    files = glob.glob("data/silver/*.json")

    if not files:
        print("❌ No silver files found")
        return None

    latest_file = max(files, key=os.path.getctime)
    print(f"📂 Using silver file: {latest_file}")

    return pd.read_json(latest_file)


def get_top_words(df):
    text = " ".join(df["clean_title"].astype(str))
    words = re.findall(r"\w+", text.lower())

    stop_words = {
        "من", "في", "على", "إلى", "عن", "مع", "هذا", "هذه", "ذلك",
        "تلك", "كان", "يكون", "تم", "قد", "ما", "لا", "لم", "لن",

        "de", "la", "le", "les", "des", "du", "un", "une", "et",
        "en", "au", "aux", "par", "pour", "dans", "sur", "avec",

        "the", "and", "for", "with", "from", "that", "this",
        "are", "was", "were", "you", "your", "his", "her",
        "its", "has", "have", "but", "not", "will", "after"
    }

    words = [w for w in words if w not in stop_words and len(w) > 2]

    top_words = Counter(words).most_common(15)

    return pd.DataFrame(top_words, columns=["word", "count"])


def articles_by_source(df):
    return df.groupby("source").size().reset_index(name="count")


def run_gold():
    df = load_latest_silver()

    if df is None or df.empty:
        print("❌ No data to analyze")
        return

    os.makedirs("data/gold", exist_ok=True)

    top_words_df = get_top_words(df)
    source_df = articles_by_source(df)

    top_words_df.to_json(
        "data/gold/top_words.json",
        orient="records",
        force_ascii=False,
        indent=4
    )

    source_df.to_json(
        "data/gold/articles_by_source.json",
        orient="records",
        force_ascii=False,
        indent=4
    )

    gold_data = {
        "top_words": top_words_df.to_dict(orient="records"),
        "articles_by_source": source_df.to_dict(orient="records")
    }

    upload_to_minio("gold", gold_data)

    print("✅ Gold layer generated locally")
    print("☁️ Gold uploaded to MinIO bucket: gold")


if __name__ == "__main__":
    run_gold()