import pytest
from datetime import datetime, timedelta

from crawler import PttCrawler


def test_get_page():
    until = datetime.now() - timedelta(minutes=30)
    crawler = PttCrawler(topic="Gossiping", until=until)
    contents = crawler.crawl()
    assert isinstance(contents, list)
    assert len(contents) > 0
    assert isinstance(contents[0], dict)
