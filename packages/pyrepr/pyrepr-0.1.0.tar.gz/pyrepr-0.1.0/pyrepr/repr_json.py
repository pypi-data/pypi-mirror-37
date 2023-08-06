import json
from json.encoder import _make_iterencode

from .util import hyper_markdownify


class ReprJSONEncoder(json.JSONEncoder):
    def iterencode(self, o, _one_shot=False):
        if self.check_circular:
            markers = {}
        else:
            markers = None

        _iterencode = _make_iterencode(
            markers, self.default, hyper_markdownify, self.indent, str,
            self.key_separator, self.item_separator, self.sort_keys,
            self.skipkeys, _one_shot)

        return _iterencode(o, 0)
