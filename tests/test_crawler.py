import pytest

from crawler import PttCrawler


def test_get_page():
    n_pages = 0
    crawler = PttCrawler(topic="Gossiping", n_pages=n_pages)
    contents = crawler.crawl()
    assert isinstance(contents, list)
    assert len(contents) > 0
    assert isinstance(contents[0], dict)
