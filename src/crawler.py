import re
import sys
import logging
import argparse
import requests
from datetime import datetime

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
    def __init__(self, args):
        self.topic = args.topic
        self.output_dir = args.output_dir
        self.output_type = args.output_type
        self.until = datetime.strptime(args.until, "%Y-%m-%d@%H-%M-%S")

    def crawl(self):
        home_url = f"https://www.ptt.cc/bbs/{self.topic}/index.html"
        page_urls = self._get_page_url(home_url)
        page_urls.reverse()

        self._get_article(page_urls)

    def _get_content(self, article):
        cont = True

        title_div = article.select('.title')[0]
        title = title_div.text

        # deleted articles didn't have url.
        article_url = article.select("a")[0].get("href")

        res = self.rs.get("http://www.ptt.cc" + article_url, timeout=60)
        soup = BeautifulSoup(res.text, "html.parser")

        author = ""
        publish_time = ""
        main_content = ""

        content_area = soup.find(id="main-content")
        main_content = content_area.text

        mata_lines = soup.select('.article-metaline')
        for meta_line in mata_lines:
            if meta_line.select('.article-meta-tag')[0].text == "作者":
                author = meta_line.select('.article-meta-value')[0].text
                continue
            if meta_line.select('.article-meta-tag')[0].text == "時間":
                publish_time = meta_line.select('.article-meta-value')[0].text
                continue

        publish_time_dt = datetime.strptime(
            publish_time, "%a %b %d %H:%M:%S %Y")
        pub_year = publish_time_dt.year
        pub_month = publish_time_dt.month

        if publish_time != "" and publish_time_dt < self.until:
            cont = False

        output_types[self.output_type](
            content={"url": article_url,
                     "author": author,
                     "title": title,
                     "main_content": main_content,
                     "publish_time": publish_time},
            output_dir=self.output_dir,
            month_dir=f"{pub_year}-{pub_month}"
        )

        return cont

    def _get_article(self, urls):
        for url in tqdm(urls):  # page
            try:
                res = self.rs.get(url, timeout=60)
            except Exception as e:
                logger.error(e)

            soup = BeautifulSoup(res.text, "html.parser")
            articles = soup.select('.r-ent')

            for article in articles:  # article
                try:
                    cont = self._get_content(article)
                except Exception as e:
                    logger.error(e)
                    continue

                if not cont:
                    return

    def _get_page_url(self, url):
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
                f"https://www.ptt.cc/bbs/Gossiping/index{i}.html" for i in range(1, int(last_idx) + 1)]
            break

        return urls


def cli(args):
    parser = argparse.ArgumentParser("The argument parser for data crawling")
    parser.add_argument("--topic", type=str, default="Gossiping")
    parser.add_argument("--output-dir", type=str, default="./data")
    parser.add_argument("--output-type", type=str,
                        default="json", choices=["json"])
    parser.add_argument("--until", type=str,
                        default="2021-01-01@11-20-00")
    return parser.parse_args(args)


if __name__ == "__main__":
    args = cli(sys.argv[1:])

    crawler = PttCrawler(args)
    crawler.crawl()
