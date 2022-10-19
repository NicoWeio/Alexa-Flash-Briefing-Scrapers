import time

from providers import golem

start = time.time()
data = golem.get()
end = time.time()
print(f"Retrieved {len(data)} articles in {(end - start):.1f} seconds")


def test_has_articles():
    assert len(data) > 0


def test_has_keys():
    KEYS = ['mainText', 'redirectionUrl', 'titleText', 'uid', 'updateDate']
    for article in data:
        for key in KEYS:
            assert key in article


def test_specials():
    """
    Special-titles such as "Gamescom 22" should not be included.
    """

    article = golem.get_single(
        "https://www.golem.de/news/steamer-gamescom-reagiert-auf-tumulte-um-montana-black-2209-168032.html")
    assert "Gamescom 22" not in article['content']
