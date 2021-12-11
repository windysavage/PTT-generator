import json
from pathlib import Path


def save_to_json(contents, output_dir):
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)

    json_dir = output_dir / "result.json"
    with open(json_dir, 'w') as f:
        json.dump(contents, f, ensure_ascii=False, indent=3)
