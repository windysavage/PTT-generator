import sys
import logging
import argparse
from pathlib import Path

import pandas as pd

from utils.helper import get_content

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.INFO)
handlers = [stdout_handler]
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s; %(asctime)s; %(module)s:%(funcName)s:%(lineno)d; %(message)s",
    handlers=handlers)

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--root-dir', default="./data",
                        help='the root directory of data.')
    args = parser.parse_args()

    if not Path(args.root_dir).exists():
        raise FileNotFoundError(
            "Please provide a correct path to data directory.")

    root_dir = Path(args.root_dir)
    files = [file for file in root_dir.glob("**/*.json")]

    df = pd.DataFrame(files, columns=["file_path"])
    logger.info(f"Reading {len(df)} json files.")

    titles = []
    articles = []
    comments = []
    for _, row in df.iterrows():
        path = row["file_path"]
        title, article, comment = get_content(path)
        titles.append(title)
        articles.append(article)
        comments.append(comment)

    df["title"] = titles
    df["article"] = articles
    df["comments"] = comment

    logger.info(f"There are {len(df)} json files.")

    df.to_csv(root_dir / "data.csv", index=False)
