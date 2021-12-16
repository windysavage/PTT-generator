import json


def get_title(path):
    with open(path) as f:
        title = json.load(f).get("title", None)
    if title is not None:
        return title.replace("\n", "")
