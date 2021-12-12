import os
import json
import shutil
from pathlib import Path
from datetime import datetime, timezone, timedelta

from crawler import cli, PttCrawler


def test_crawl():
    test_output_dir = "./test_outputs"
    until = datetime.now(timezone.utc) + \
        timedelta(hours=8) - timedelta(minutes=15)
    until = until.replace(tzinfo=None)
    year = until.year
    month = until.month

    until = datetime.strftime(until, "%Y-%m-%d@%H-%M-%S")
    argv = [
        "--topic", "Gossiping",
        "--output-dir", test_output_dir,
        "--until", until
    ]
    args = cli(argv)
    crawler = PttCrawler(args)
    crawler.crawl()

    json_files = os.listdir(f"{test_output_dir}/{year}-{month}")
    for json_file in json_files:
        with open(f"{test_output_dir}/{year}-{month}/{json_file}") as f:
            result = json.load(f)
        assert isinstance(result, dict)

    shutil.rmtree(test_output_dir)
