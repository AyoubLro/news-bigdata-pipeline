import time
import os

while True:
    print("🔄 Running pipeline...")

    os.system("python scraper/main_scraper.py")
    os.system("python processing/clean.py")
    os.system("python processing/analysis.py")
    os.system("python db/database.py")

    print("⏳ Waiting 10 seconds...")
    time.sleep(10)