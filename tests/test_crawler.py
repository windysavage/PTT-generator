import pytest

from crawler import get_page


def test_get_page():
    titles = get_page()
    assert isinstance(titles, list)
    assert len(titles) > 0
