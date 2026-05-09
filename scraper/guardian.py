import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urljoin


def get_guardian():
    url = "https://www.theguardian.com/international"
    headers = {"User-Agent": "Mozilla/5.0"}

    r = requests.get(url, headers=headers, timeout=15)
    soup = BeautifulSoup(r.text, "html.parser")

    articles = []
    seen = set()

    posts = soup.select("h3, a")

    for post in posts:
        title = post.get_text(" ", strip=True)

        if post.name == "a":
            a_tag = post
        else:
            a_tag = post.find_parent("a")

        if not a_tag:
            continue

        href = a_tag.get("href", "")
        full_url = urljoin(url, href)

        if not title or len(title) < 25:
            continue

        if full_url in seen:
            continue

        seen.add(full_url)

        articles.append({
            "title": title,
            "url": full_url,
            "source": "guardian",
            "scraped_at": datetime.now().isoformat()
        })

        if len(articles) >= 15:
            break

    return articles