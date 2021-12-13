import logging

import torch

logger = logging.getLogger(__name__)


def train_epcoh(epoch, data_loader, model, config):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = model.to(device)

    logger.info(f"start training epoch {epoch}")
    for _, batch in enumerate(data_loader):
        batch = batch.to(device)
        preds = model(batch)
        print(preds)
        break


def val_epcoh():
    logger.info("start validating")
