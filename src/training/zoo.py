import logging

from transformers import BertTokenizerFast, AutoModelForCausalLM

logger = logging.getLogger(__name__)


def gpt2_chinese():
    logger.info("start loading model: gpt2_chinese")
    tokenizer = BertTokenizerFast.from_pretrained('bert-base-chinese')
    model = AutoModelForCausalLM.from_pretrained(
        'ckiplab/gpt2-base-chinese')
    logger.info("end loading model: gpt2_chinese")

    return model, tokenizer
