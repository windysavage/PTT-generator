import json
import math
from pathlib import Path


def save_to_json(content, output_dir, month_dir):
    content_dir = Path(output_dir) / month_dir

    content_dir.mkdir(parents=True, exist_ok=True)
    url = content.get("url", "")

    if url == "":
        return

    idx = url.split("/")[-1].split(".html")[0]
    content_json = content_dir / (idx + ".json")
    with open(content_json, 'w') as f:
        json.dump(content, f, ensure_ascii=False, indent=3)
