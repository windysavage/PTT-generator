import logging

import tqdm
import torch

logger = logging.getLogger(__name__)


optimizers = {
    "Adam": torch.optim.Adam
}


def train_epcoh(epoch, data_loader, model, config):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = model.to(device)
    optimizer = optimizers[config.get("optimizer")](
        params=model.parameters(), lr=config["lr"])

    logger.info(f"start training epoch {epoch}")
    for _, batch in enumerate(data_loader):
        batch = {k: v.to(device) for k, v in batch.items()}
        preds = model(**batch)
        loss = preds.loss

        loss.backward()
        optimizer.step()
        optimizer.zero_grad()

    # break


def val_epcoh():
    logger.info("start validating")
