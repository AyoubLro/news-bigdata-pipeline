import pandas as pd
import glob
import json
import re
import os
from datetime import datetime

from storage.upload import upload_to_minio


# =========================
# CLEAN TEXT FUNCTION
# =========================
def clean_text(text):
    if not text:
        return ""

    text = str(text)

    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text.lower().strip()


# =========================
# LOAD BRONZE DATA
# =========================
def load_bronze_data():
    files = glob.glob("data/bronze/*.json")

    all_data = []

    for file in files:
        with open(file, "r", encoding="utf-8") as f:
            all_data.extend(json.load(f))

    return pd.DataFrame(all_data)


# =========================
# PROCESS → SILVER
# =========================
def process():
    df = load_bronze_data()

    if df.empty:
        print("❌ No data found")
        return

    df.columns = [c.lower() for c in df.columns]

    if "scraped_at" in df.columns and "date" not in df.columns:
        df["date"] = df["scraped_at"]

    df["clean_title"] = df["title"].apply(clean_text)

    df["url"] = df["url"].fillna("unknown")
    df["source"] = df["source"].fillna("unknown")
    df["date"] = df["date"].fillna(pd.Timestamp.now().isoformat())

    df = df.dropna(subset=["title"])
    df = df[df["clean_title"] != ""]
    df = df.drop_duplicates(subset=["title"])

    df = df[["title", "clean_title", "url", "source", "date"]]

    # save local silver
    os.makedirs("data/silver", exist_ok=True)

    output_file = f"data/silver/cleaned_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    df.to_json(output_file, orient="records", force_ascii=False, indent=4)

    # save MinIO silver
    upload_to_minio("silver", df.to_dict(orient="records"))

    print(f"💾 Saved locally: {output_file}")
    print("☁️ Saved to SILVER (MinIO)")
    print(f"✅ Cleaning done: {len(df)} rows")


if __name__ == "__main__":
    process()