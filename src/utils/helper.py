import json


def get_content(path):
    with open(path) as f:
        file = json.load(f)
        title = file.get("title", None)
        text = file.get("main_content", None)

    if title is not None:
        title = title.replace("\n", "")

    if text is not None:
        # do something to extract article

        article_start = 0
        article_end = 0
        comment_start = 0

        text_segments = text.split("\n")
        for i, segment in enumerate(text_segments):
            if most_digit(segment) and article_start == 0:
                article_start = i + 1

            if "文章網址" in segment:
                article_end = i - 3
                comment_start = i + 1

    article = "\n".join(text_segments[article_start: article_end + 1])
    comment = "\n".join(text_segments[comment_start:])
    return title, article, comment


def most_digit(s):
    count = 0
    for c in s:
        if c.isdigit():
            count += 1
    return count >= len(s) * 0.5
