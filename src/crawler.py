import re
import sys
import logging
import argparse
import requests

from tqdm import tqdm
from bs4 import BeautifulSoup

from utils import futils

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.INFO)
handlers = [stdout_handler]
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s; %(asctime)s; %(module)s:%(funcName)s:%(lineno)d; %(message)s",
    handlers=handlers)

logger = logging.getLogger(__name__)

output_types = {
    "json": futils.__dict__["save_to_json"]
}


class PttCrawler():
    def __init__(self, topic, n_pages):
        self.topic = topic
        self.n_pages = n_pages

    def crawl(self):
        home_url = f"https://www.ptt.cc/bbs/{self.topic}/index.html"
        urls = self._get_all_url(home_url) + [home_url]
        results = self._get_title(urls, self.n_pages)

        for result in results:
            result["title"] = result["title"].replace("\n", "")

        return results

    def _get_title(self, urls, n_pages=None):
        all_results = []

        n_pages = len(urls) if n_pages == None else n_pages
        for url in tqdm(urls[:n_pages]):  # page
            try:
                res = self.rs.get(url)
                soup = BeautifulSoup(res.text, "html.parser")

                articles = soup.select('.r-ent')
                page_results = []
                for article in articles:  # article
                    title_div = article.select('.title')[0]
                    title = title_div.text
                    article_url = article.select("a")[0].get("href")
                    page_results.append({"url": article_url, "title": title})

                all_results.extend(page_results)

            except Exception as e:
                logger.error(e)

        return all_results

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
    parser.add_argument("--output-dir", type=str, default="./data")
    parser.add_argument("--output-type", type=str,
                        default="json", choices=["json"])
    args = parser.parse_args()

    crawler = PttCrawler(topic=args.topic, n_pages=1)
    results = crawler.crawl()
    output_types[args.output_type](
        contents=results, output_dir=args.output_dir)
    logger.info(f"There are {len(results)} articles.")
