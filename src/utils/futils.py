import json
import math
from pathlib import Path


def save_to_json(contents, output_dir):
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)

    results_in_file = 1000
    n_files = math.ceil(len(contents) / results_in_file)

    count = 0
    while count < n_files:
        json_dir = output_dir / f"{count}.json"
        with open(json_dir, 'w') as f:
            json.dump(contents[:results_in_file], f,
                      ensure_ascii=False, indent=3)
        contents = contents[results_in_file:]
        count += 1
