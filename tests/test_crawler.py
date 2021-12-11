import pytest

from crawler import crawl


def test_get_page():
    n_pages = 3
    titles = crawl(n_pages)
    assert isinstance(titles, list)
    assert len(titles) > 0
