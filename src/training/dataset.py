import json
import random

import torch
from torch.utils.data import Dataset


class PttDataset(Dataset):
    def __init__(self, docs_path, tokenizer):
        self.docs_path = docs_path
        self.tokenizer = tokenizer

    def __getitem__(self, index):
        doc_path = self.docs_path[index]
        with open(doc_path) as f:
            doc = json.load(f)

        title = doc["title"]
        inputs = self.tokenizer(
            text=title,
            padding="max_length",
            truncation=True,
            max_length=64,
            return_token_type_ids=True
        )

        input_ids = torch.tensor(
            data=inputs["input_ids"],
            dtype=torch.int32
        )

        return input_ids

    def _reset(self):
        random.shuffle(self.docs_path)

    def __len__(self):
        return len(self.docs_path)
