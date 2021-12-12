import pytest
from datetime import datetime, timezone, timedelta

from crawler import PttCrawler


def test_get_page():
    until = datetime.now(timezone.utc) + \
        timedelta(hours=8) - timedelta(minutes=15)
    until = until.replace(tzinfo=None)
    crawler = PttCrawler(topic="Gossiping", until=until)
    contents = crawler.crawl()
    assert isinstance(contents, list)
    assert len(contents) > 0
    assert isinstance(contents[0], dict)
