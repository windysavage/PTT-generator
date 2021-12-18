import json
import random

import torch
from torch.utils.data import Dataset


class PttDataset(Dataset):
    def __init__(self, docs, doc_type, tokenizer):
        self.docs = docs.reset_index()
        self.doc_type = doc_type
        self.tokenizer = tokenizer

    def __getitem__(self, index):
        title = self.docs.at[index, self.doc_type]
        inputs = self.tokenizer(
            text=title,
            padding="max_length",
            truncation=True,
            max_length=64,
            return_token_type_ids=True
        )

        inputs = {k: torch.tensor(v, dtype=torch.int32)
                  for k, v in inputs.items()}
        inputs["labels"] = torch.tensor(
            self._get_labels(inputs["input_ids"]), dtype=torch.int64)

        return inputs

    def _reset(self):
        random.shuffle(self.docs)

    def __len__(self):
        return len(self.docs)

    def _get_labels(self, input_ids):
        return [input_id if input_id not in [0, 101, 102] else -100 for input_id in input_ids]
