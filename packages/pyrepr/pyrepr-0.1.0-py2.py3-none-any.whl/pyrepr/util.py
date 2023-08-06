import json
from markdownify import markdownify


def hyper_markdownify(s):
    while True:
        try:
            s = json.loads(s)
        except (json.decoder.JSONDecodeError, TypeError):
            break

    return markdownify(s)
