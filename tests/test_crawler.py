import pytest

from crawler import PttCrawler


def test_get_page():
    n_pages = 3
    crawler = PttCrawler(topic="Gossiping", n_pages=n_pages)
    titles = crawler.crawl()
    assert isinstance(titles, list)
    assert len(titles) > 0
    assert isinstance(titles[0], dict)
