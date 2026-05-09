import requests
from bs4 import BeautifulSoup
from datetime import datetime


def get_france24():
    url = "https://www.france24.com/fr/rss"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    r = requests.get(url, headers=headers, timeout=15)
    r.raise_for_status()

    soup = BeautifulSoup(r.content, "xml")

    articles = []
    seen = set()

    items = soup.find_all("item")

    for item in items:
        title_tag = item.find("title")
        link_tag = item.find("link")

        if not title_tag or not link_tag:
            continue

        title = title_tag.get_text(strip=True)
        link = link_tag.get_text(strip=True)

        if not title or len(title) < 20:
            continue

        if link in seen:
            continue

        seen.add(link)

        articles.append({
            "title": title,
            "url": link,
            "source": "france24",
            "scraped_at": datetime.now().isoformat()
        })

        if len(articles) >= 15:
            break

    return articles