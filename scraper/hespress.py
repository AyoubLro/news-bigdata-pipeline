import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urljoin

URL = "https://www.hespress.com"


def get_hespress():
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(URL, headers=headers, timeout=15)
    soup = BeautifulSoup(response.text, "html.parser")

    articles = []
    seen = set()

    # 🔥 استهداف titles ديال الأخبار فقط
    posts = soup.select("h3")

    for post in posts:
        title = post.get_text(strip=True)

        a_tag = post.find_parent("a")

        if not a_tag:
            continue

        href = a_tag.get("href", "")
        full_url = urljoin(URL, href)

        if not title or len(title) < 20:
            continue

        if full_url in seen:
            continue

        seen.add(full_url)

        articles.append({
            "title": title,
            "url": full_url,
            "source": "hespress",
            "scraped_at": datetime.now().isoformat()
        })

        if len(articles) >= 15:
            break

    return articles