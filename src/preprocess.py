import sys
import logging
import argparse
from pathlib import Path

import pandas as pd

from utils.helper import get_title

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
    parser.add_argument('--root-dir', help='the root directory of data.')
    args = parser.parse_args()

    if not Path(args.root_dir).exists():
        raise FileNotFoundError(
            "Please provide a correct path to data directory.")

    root_dir = Path(args.root_dir)
    files = [file for file in root_dir.glob("**/*.json")]

    df = pd.DataFrame(files, columns=["file_path"])
    logger.info(f"Reading {len(df)} json files.")
    df["title"] = df["file_path"].apply(lambda x: get_title(x))
    df["title"] = df["title"].apply(lambda x: x.replace("Re: ", ""))
    df = df.drop_duplicates(subset=["title"])
    logger.info(f"There are {len(df)} json files after dedup.")

    df.to_csv(root_dir / "data.csv", index=False)
