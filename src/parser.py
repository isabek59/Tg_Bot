import json
import requests
from bs4 import BeautifulSoup


def parser(name_file):
    """
    Parse the site https://matchtv.ru/news/football/ and get articles
    - name_file: The name of the file where the information about the article will be recorded
    """
    user_agent = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                      " Chrome/101.0.4951.54 Safari/537.36"
    }

    url = "https://matchtv.ru/news/football/"

    r = requests.get(url=url, headers=user_agent)
    soup = BeautifulSoup(r.text, "html.parser")
    cards = soup.find_all("a", class_="node-news-list__item")
    dict_news = {}
    cards = cards[:10]

    for article in cards:
        article_url = f'https://matchtv.ru{article.get("href")}'
        article_title = article.get("title")

        article_date_time = article.find("li", class_="list__item credits__item").text.strip()

        article_id = article.find("div", class_="node-news-list__title").get("data-node-id")

        dict_news[article_id] = {
            "article_date_timestamp": article_date_time,
            "article_title": article_title,
            "article_url": article_url
        }

        with open(f"{name_file}.json", "w", encoding='utf-8') as file:
            json.dump(dict_news, file, indent=4, ensure_ascii=False)