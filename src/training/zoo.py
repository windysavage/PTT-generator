import logging

from transformers import BertTokenizerFast, AutoModel

logger = logging.getLogger(__name__)


class gpt2_chinese():
    def __init__(self):
        logger.info(f"start loading model: {type(self)}")
        self.tokenizer = BertTokenizerFast.from_pretrained('bert-base-chinese')
        self.model = AutoModel.from_pretrained('ckiplab/gpt2-base-chinese')
        logger.info(f"end loading model: {type(self)}")

    def __call__(self, inputs):
        outputs = self.model(inputs)
        return outputs

    def to(self, device):
        self.model.to(device)
        return self
