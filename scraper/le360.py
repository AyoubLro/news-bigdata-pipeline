import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urljoin


def get_le360():
    base_url = "https://www.le360.ma"
    headers = {"User-Agent": "Mozilla/5.0"}

    r = requests.get(base_url, headers=headers, timeout=15)
    soup = BeautifulSoup(r.text, "html.parser")

    articles = []
    seen = set()

    links = soup.select("a[href*='/']")

    for link in links:
        title = link.get_text(strip=True)
        href = link.get("href")

        # 🔥 نحولو الرابط الكامل
        full_url = urljoin(base_url, href)

        if not title or len(title) < 25:
            continue

        if not full_url.startswith("http"):
            continue

        if full_url in seen:
            continue

        seen.add(full_url)

        articles.append({
            "title": title,
            "url": full_url,
            "source": "le360",
            "scraped_at": datetime.now().isoformat()
        })

        if len(articles) >= 15:
            break

    return articles