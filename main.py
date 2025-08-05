from utils.news_fetcher import fetch_tech_news_rss
from models.slm_writer import rewrite_article
from utils.generate_article import generate_markdown
from utils.hugo_publisher import publish_to_hugo
from utils.generate_article import rewrite_article


def main():
    articles = fetch_tech_news_rss()
    for article in articles:
        print(f"Processing: {article['title']}")
        rewritten = rewrite_article(article['summary'], article['title'])
        generate_markdown(article['title'], rewritten, article['published'])

    publish_to_hugo()
    
if __name__ == "__main__":
    main()
