import logging

from tqdm import tqdm
import torch
from torch.utils.tensorboard import SummaryWriter

logger = logging.getLogger(__name__)


optimizers = {
    "Adam": torch.optim.Adam
}

writer = SummaryWriter()


def train_epcoh(epoch, data_loader, model, config):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.train()
    model = model.to(device)
    optimizer = optimizers[config.get("optimizer")](
        params=model.parameters(), lr=config["lr"])

    losses = []

    logger.info(f"start training epoch {epoch}")
    for batch in tqdm(data_loader):
        batch = {k: v.to(device) for k, v in batch.items()}
        preds = model(**batch)
        loss = preds.loss
        losses.append(loss.item())

        loss.backward()
        optimizer.step()
        optimizer.zero_grad()

    writer.add_scalar('Loss/train', sum(losses)/len(losses), epoch)
    return sum(losses)/len(losses)


def val_epcoh(epoch, data_loader, model):
    model.eval()

    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = model.to(device)

    losses = []

    with torch.no_grad():
        for batch in tqdm(data_loader):
            batch = {k: v.to(device) for k, v in batch.items()}
            preds = model(**batch)
            loss = preds.loss
            losses.append(loss.item())

    writer.add_scalar('Loss/val', sum(losses)/len(losses), epoch)
    return sum(losses)/len(losses)
