import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup

URL = 'https://golem.de'
NUM_ARTICLES = 5

s = requests.Session()
s.cookies['golem_consent20'] = 'cmp|220101'


def get(golemplus_filter=None):
    r = s.get(URL)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, 'html.parser')

    article_lists = soup.find_all('ol', class_='list-articles')
    articles = [
        article
        for article_list in article_lists
        for article in article_list.find_all('li', recursive=False)
        # NOTE: Some <li> tags are not articles, but e.g. "Verlagsangebot[e]"
        if 'data-article-id' in article.attrs
    ]
    print(f"Found {len(articles)} articles in total")

    article_urls = [
        article.find('header').find('a')['href']
        for article in articles
        if (
            golemplus_filter is None  # default: no filter
            or
            golemplus_filter == ('golemplus' in article.get('class', []))
        )
    ]

    data = [
        get_single(url) for url in article_urls[:NUM_ARTICLES]
    ]

    return [
        {
            'uid': hex(hash(article['title']))[2:8+1],
            'titleText': article['title'],
            'mainText': f"{article['title']}: {article['content']}",
            'updateDate': article['datetime'],
            'redirectionUrl': article['url'],
        }
        for article in data
    ]


def get_single(url):
    r = s.get(url)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, 'html.parser')
    article = soup.find('article')

    # NOTE: There might be an empty <p> tag before the actual header content.
    # Example: https://www.golem.de/news/steamer-gamescom-reagiert-auf-tumulte-um-montana-black-2209-168032.html
    content = (article.find('header').find_all('p')[-1].text.strip()
               .replace("Hinweis: Um sich diesen Artikel vorlesen zu lassen, klicken Sie auf den Player im Artikel.", "")
               .strip()
               )
    assert content

    return {
        'url': url,
        'datetime': article.find('time')['datetime'],
        'title': article.find('header').find('h1').find('span', class_='head5').text,
        'content': content,
        'is_golemplus': 'golemplus' in article.get('class', []),
    }


if __name__ == '__main__':
    print(get())
