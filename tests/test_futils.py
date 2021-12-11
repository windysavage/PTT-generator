import json
from pathlib import Path

from utils.futils import save_to_json


def test_save_json():
    test_sequences = [
        {
            "url": "/bbs/Gossiping/M.1119222611.A.7A9.html",
            "category": "[問卦]",
            "title": "第一耶！"
        },
        {
            "url": "/bbs/Gossiping/M.1119222660.A.94E.html",
            "category": "[問卦]",
            "title": "Re: (問題)華航空難留言"
        },
        {
            "url": "/bbs/Gossiping/M.1119233779.A.191.html",
            "category": "[問卦]",
            "title": "Re: 有沒有明天會更好的八卦"
        }
    ]

    output_dir = "./"
    save_to_json(contents=test_sequences, output_dir=output_dir)

    output_file = Path(output_dir) / "0.json"
    with open(output_file) as f:
        results = json.load(f)

    assert results == test_sequences

    output_file.unlink()
