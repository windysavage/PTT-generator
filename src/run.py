import sys
import json
import random
import logging
import argparse
from pathlib import Path

from tqdm import tqdm
from torch.utils.data import DataLoader
import pandas as pd

from training.dataset import PttDataset
from training.trainer import train_epcoh, val_epcoh
from training import zoo

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.INFO)
handlers = [stdout_handler]
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s; %(asctime)s; %(module)s:%(funcName)s:%(lineno)d; %(message)s",
    handlers=handlers)

logger = logging.getLogger(__name__)


class PttCli():
    def __init__(self, argv):
        parser = argparse.ArgumentParser(
            description='CLI for model traning and inferance.',
            usage='''run.py <command> [<args>]

        The most commonly used on_slogan commands are:
           train                Train NLG model
           infer                Infer contents based on context
        ''')

        parser.add_argument('command', help='Subcommand to run')
        args = parser.parse_args(argv[1:2])
        if not hasattr(self, args.command):
            print('Unrecognized command')
            parser.print_help()
            exit(1)

        # use dispatch pattern to invoke method with same name
        getattr(self, args.command)(argv)

    def train(self, argv):
        parser = argparse.ArgumentParser(
            description='Train NLG model')
        parser.add_argument("--root-dir", type=str, default="./data")
        parser.add_argument("--train-split", type=float, default=0.8)
        parser.add_argument("--model", type=str, default="gpt2_chinese")
        parser.add_argument("--random-seed", type=int, default=111)
        args = parser.parse_args(argv[2:])

        with open(f"src/configs/{args.model}.json") as f:
            model_config = json.load(f)

        random.seed(args.random_seed)
        docs = pd.read_csv(Path(args.root_dir) / "data.csv")
        docs = docs.sample(frac=1, random_state=args.random_seed)

        train_size = round(len(docs) * args.train_split)
        train_docs = docs[:train_size]
        val_docs = docs[train_size:]

        model, tokenizer = zoo.__dict__[args.model]()

        train_ds = PttDataset(docs=train_docs,
                              doc_type="title",
                              tokenizer=tokenizer)

        val_ds = PttDataset(docs=val_docs, doc_type="title",
                            tokenizer=tokenizer)

        train_loader = DataLoader(
            train_ds, batch_size=model_config["batch_size"], shuffle=False)
        val_loader = DataLoader(
            val_ds, batch_size=model_config["batch_size"], shuffle=False)

        for epoch in range(model_config["epoch"]):
            train_loss = train_epcoh(
                epoch=epoch,
                data_loader=train_loader,
                model=model,
                config=model_config
            )
            train_ds._reset()

            val_loss = val_epcoh(
                epoch=epoch,
                data_loader=val_loader,
                model=model
            )

            logger.info(
                f"Epoch: {epoch}, Train_loss: {train_loss}, Val_loss: {val_loss}")


if __name__ == "__main__":
    PttCli(sys.argv)
