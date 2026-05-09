import os
import json
from datetime import datetime

from scraper.hespress import get_hespress
from scraper.le360 import get_le360
from scraper.france24 import get_france24
from scraper.guardian import get_guardian

from streaming.producer import send_article
from storage.upload import upload_to_minio


def safe_scrape(source_name, scraper_function):
    try:
        print(f"🔄 Scraping {source_name}...")

        articles = scraper_function()

        if articles is None:
            articles = []

        print(f"✅ {source_name}: {len(articles)} articles")
        return articles

    except Exception as e:
        print(f"❌ {source_name} error: {e}")
        return []


def run_all():
    all_articles = []

    all_articles += safe_scrape("Hespress", get_hespress)
    all_articles += safe_scrape("Le360", get_le360)
    all_articles += safe_scrape("France24", get_france24)
    all_articles += safe_scrape("Guardian", get_guardian)

    return all_articles


def save_data(data):
    os.makedirs("data/bronze", exist_ok=True)

    filename = f"data/bronze/articles_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    # Save local bronze
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"💾 Saved locally: {filename}")

    # Save to MinIO bronze
    upload_to_minio("bronze", data)

    # Send to Kafka
    sent = 0

    for article in data:
        try:
            send_article(article)
            sent += 1
        except Exception as e:
            print(f"⚠️ Kafka send error: {e}")

    print(f"✅ Total scraped: {len(data)} articles")
    print("☁️ Uploaded to MinIO bucket: bronze")
    print(f"📡 Articles sent to Kafka topic news_topic: {sent}")


if __name__ == "__main__":
    data = run_all()
    save_data(data)