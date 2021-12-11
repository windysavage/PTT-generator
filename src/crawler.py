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


class PttCrawler():
    def __init__(self, topic, n_pages):
        self.topic = topic
        self.n_pages = n_pages

    def crawl(self):
        home_url = f"https://www.ptt.cc/bbs/{self.topic}/index.html"
        urls = self._get_all_url(home_url) + [home_url]
        titles = self._get_title(urls, self.n_pages)
        titles = [title.replace("\n", "") for title in titles]

        return titles

    def _get_title(self, urls, n_pages=None):
        all_titles = []

        n_pages = len(urls) if n_pages == None else n_pages
        for url in tqdm(urls[:n_pages]):
            res = self.rs.get(url)
            soup = BeautifulSoup(res.text, "html.parser")
            titles = [entry.select('.title')[
                0].text for entry in soup.select('.r-ent')]
            all_titles.extend(titles)

        return all_titles

    def _get_all_url(self, url):
        payload = {
            'from': f'/bbs/{self.topic}/index.html',
            'yes': 'yes'
        }
        self.rs = requests.session()
        res = self.rs.post('https://www.ptt.cc/ask/over18', data=payload)
        res = self.rs.get(url)

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


if __name__ == "__main__":
    parser = argparse.ArgumentParser("The argument parser for data crawling")
    parser.add_argument("--topic", type=str, default="Gossiping")
    args = parser.parse_args()

    crawler = PttCrawler(topic=args.topic, n_pages=3)
    titles = crawler.crawl()
    logger.info(titles)
