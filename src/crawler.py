import re
import sys
import logging
import argparse
import requests

from tqdm import tqdm
from bs4 import BeautifulSoup

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.INFO)
handlers = [stdout_handler]
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s; %(asctime)s; %(module)s:%(funcName)s:%(lineno)d; %(message)s",
    handlers=handlers)

logger = logging.getLogger(__name__)


def get_title(urls, n_pages=None):
    payload = {
        'from': '/bbs/Gossiping/index.html',
        'yes': 'yes'
    }
    rs = requests.session()
    res = rs.post('https://www.ptt.cc/ask/over18', data=payload)
    all_titles = []

    n_pages = len(urls) if n_pages == None else n_pages
    for url in tqdm(urls[:n_pages]):
        res = rs.get(url)
        soup = BeautifulSoup(res.text, "html.parser")
        titles = [entry.select('.title')[
            0].text for entry in soup.select('.r-ent')]
        all_titles.extend(titles)

    return all_titles


def get_all_url(url):
    payload = {
        'from': '/bbs/Gossiping/index.html',
        'yes': 'yes'
    }
    rs = requests.session()
    res = rs.post('https://www.ptt.cc/ask/over18', data=payload)
    res = rs.get(url)

    soup = BeautifulSoup(res.text, "html.parser")
    btns = soup.select(".btn")
    urls = None

    for btn in btns:
        if btn.text != "‹ 上頁":
            continue
        last_page = btn.get("href")
        ptns = [
            "index[0-9][0-9][0-9][0-9][0-9]",
            "index[0-9][0-9][0-9][0-9]",
            "index[0-9][0-9][0-9]",
            "index[0-9][0-9]",
            "index[0-9]"]
        last_idx = re.findall("|".join(ptns), last_page)
        last_idx = last_idx[0].replace("index", "")
        urls = [
            f"https://www.ptt.cc/bbs/Gossiping/index{i}.html" for i in range(1, int(last_idx))]
        break

    return urls


def crawl(n_pages):
    home_url = "https://www.ptt.cc/bbs/Gossiping/index.html"
    urls = get_all_url(home_url) + [home_url]
    titles = get_title(urls, n_pages)
    titles = [title.replace("\n", "") for title in titles]

    return titles


if __name__ == "__main__":
    parser = argparse.ArgumentParser("The argument parser for data crawling")
    parser.add_argument("--topic", type=str, default="Gossip")
    args = parser.parse_args()

    titles = crawl(n_pages=5)
    print(titles)
