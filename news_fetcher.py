import feedparser

RSS_FEEDS = [
    "https://techcrunch.com/feed/",
    "https://www.theverge.com/rss/index.xml",
    "https://www.wired.com/feed/rss",
    "http://feeds.arstechnica.com/arstechnica/index",
    "http://feeds.bbci.co.uk/news/technology/rss.xml",
    "https://news.google.com/rss/search?q=technology&hl=en-IN&gl=IN&ceid=IN:en"
]

def fetch_tech_news_rss(max_articles=10):
    articles = []

    for feed_url in RSS_FEEDS:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries[:max_articles]:
            title = entry.get("title", "")
            summary = entry.get("summary", "")
            published = entry.get("published", "")
            link = entry.get("link", "")

            # Optional: avoid duplicates
            if not any(a['title'] == title for a in articles):
                articles.append({
                    "title": title,
                    "summary": summary,
                    "published": published,
                    "link": link
                })

    return articles[:max_articles]
