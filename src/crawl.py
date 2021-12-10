import sys
import logging
import argparse

import requests
from bs4 import BeautifulSoup

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.INFO)
handlers = [stdout_handler]
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s; %(asctime)s; %(module)s:%(funcName)s:%(lineno)d; %(message)s",
    handlers=handlers)

logger = logging.getLogger(__name__)


def get_page():
    payload = {
        'from': '/bbs/Gossiping/index.html',
        'yes': 'yes'
    }
    rs = requests.session()
    res = rs.post('https://www.ptt.cc/ask/over18', data=payload)
    res = rs.get('https://www.ptt.cc/bbs/Gossiping/index.html')

    soup = BeautifulSoup(res.text, "html.parser")
    for entry in soup.select('.r-ent'):
        print(entry.select('.title')[0].text, entry.select('.date')[0].text)


if __name__ == "__main__":
    parser = argparse.ArgumentParser("The argument parser for data crawling")
    parser.add_argument("--topic", type=str, default="Gossip")
    args = parser.parse_args()

    get_page()
