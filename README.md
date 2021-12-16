# PTT-generator / PTT生成器

This repo aims to implement a PTT (a well-knowned BBS in Taiwan) generator via natural language generation techniques. The generated contents might be titles, replies...etc.

To achieve this goal, there are some tasks which need to be done first...

## Dataset preparation
In order to prepare the datasets for language generation, this repo offered a tool to crawl PTT articles.

- To crawl titles of a given topic

```bash
python src/crawler.py --topic Gossiping --output-dir ./data --output-type json --until 2021/01/01
```

## Finetune a languane model
- You can utilize the data collected in the last step to finetune a language model.
```bash
python src/run.py train
```
