import toml
import json
import re
from io import StringIO

from .repr_json import ReprJSONEncoder
from .util import hyper_markdownify


class Repr:
    OUT_FORMAT = '''
{header}
{markdown}

'''[1:]

    def __init__(self, obj, format_='toml'):
        self.format_ = format_

        self.stream = StringIO()
        toml.dump(obj, self.stream)

    def to_io(self, f_out, format_=None):
        if format_ is None:
            format_ = self.format_

        self.stream.seek(0)

        if format_ == 'json':
            return json.dump(toml.load(self.stream), f_out, cls=ReprJSONEncoder, indent=2)

        header = ''
        for row in self.stream:
            match_obj = re.fullmatch(r'(.*) = (.*)\n', row)
            if match_obj is not None:
                k, v = match_obj.groups()
                f_out.write(self.OUT_FORMAT.format(**{
                    'header': self.key_to_header(header, k, format_=format_),
                    'markdown': hyper_markdownify(v)
                }))
            else:
                header = self.header_to_header(row, format_=format_)
                if header is None:
                    header = row

                f_out.write(header)

    def to_str(self, format_=None):
        f_out = StringIO()
        self.to_io(f_out, format_)

        return f_out.getvalue()

    def __str__(self):
        return self.to_str()

    def __repr__(self):
        return str(self)

    def _repr_markdown_(self):
        return self.to_str(format_='markdown')

    def key_to_header(self, main_key, key, format_):
        if format_ == 'markdown':
            return self._key_to_header_markdown(main_key, key)
        else:
            return self._key_to_header_toml(main_key, key)

    def _key_to_header_markdown(self, main_key, key):
        return '{heading} {key}'.format(**{
            'heading': '#' * (self._get_depth(main_key, '#') + 1),
            'key': key
        })

    def _key_to_header_toml(self, main_key, key):
        depth = self._get_depth(main_key, '[') + 1
        return '{front}{center}{back}'.format(**{
            'front': '[' * depth,
            'center': key,
            'back': ']' * depth
        })

    @staticmethod
    def _get_depth(main_key, compare):
        i = 0
        for i, c in enumerate(main_key):
            if c != compare:
                break

        return i

    def header_to_header(self, header, format_):
        if format_ == 'markdown':
            return self._header_to_header_markdown(header)

        return header

    @staticmethod
    def _header_to_header_markdown(s):
        match_obj = re.fullmatch(r'(\[+)(.+)(\]+)\n', s)
        if match_obj:
            front, center, back = match_obj.groups()
            if len(front) == len(back):
                return '#' * len(front) + ' ' + center + '\n'
