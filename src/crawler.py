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
    def __init__(self, topic, until):
        self.topic = topic
        self.until = until

    def crawl(self):
        home_url = f"https://www.ptt.cc/bbs/{self.topic}/index.html"
        page_urls = self._get_page_url(home_url)
        page_urls.reverse()

        articles = self._get_article(page_urls)

        for article in articles:
            article["title"] = article.get("title", "").replace("\n", "")

        return articles

    def _get_content(self, article):
        cont = True

        title_div = article.select('.title')[0]
        title = title_div.text

        # deleted articles didn't have url.
        try:
            article_url = article.select("a")[0].get("href")
        except Exception as e:
            logger.info("This article has been deleted.")
            logger.error(e)
            return {}, cont

        res = self.rs.get("http://www.ptt.cc" + article_url)
        soup = BeautifulSoup(res.text, "html.parser")

        author = ""
        publish_time = ""

        mata_lines = soup.select('.article-metaline')
        for meta_line in mata_lines:
            if meta_line.select('.article-meta-tag')[0].text == "作者":
                author = meta_line.select('.article-meta-value')[0].text
                continue
            if meta_line.select('.article-meta-tag')[0].text == "時間":
                publish_time = meta_line.select('.article-meta-value')[0].text
                continue

        if publish_time != "" and datetime.strptime(publish_time, "%a %b %d %H:%M:%S %Y") < self.until:
            cont = False

        return{
            "url": article_url,
            "author": author,
            "title": title,
            "publish_time": publish_time
        }, cont

    def _get_article(self, urls):
        all_results = []

        for url in tqdm(urls):  # page
            res = self.rs.get(url)
            soup = BeautifulSoup(res.text, "html.parser")

            articles = soup.select('.r-ent')
            page_results = []

            for article in articles:  # article
                content, cont = self._get_content(article)
                page_results.append(content)

                if not cont:
                    all_results.extend(page_results)
                    return all_results

            all_results.extend(page_results)

        return all_results

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


if __name__ == "__main__":
    parser = argparse.ArgumentParser("The argument parser for data crawling")
    parser.add_argument("--topic", type=str, default="Gossiping")
    parser.add_argument("--output-dir", type=str, default="./data")
    parser.add_argument("--output-type", type=str,
                        default="json", choices=["json"])
    parser.add_argument("--until", type=str,
                        default="2021-12-12@11-20-00")
    args = parser.parse_args()

    until = datetime.strptime(args.until, "%Y-%m-%d@%H-%M-%S")

    crawler = PttCrawler(topic=args.topic, until=until)
    results = crawler.crawl()
    output_types[args.output_type](
        contents=results, output_dir=args.output_dir)
    logger.info(f"There are {len(results)} articles.")
