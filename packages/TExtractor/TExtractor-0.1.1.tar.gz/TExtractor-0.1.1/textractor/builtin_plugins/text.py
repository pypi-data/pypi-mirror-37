# -*- coding: utf-8 -*-


PROVIDES = {}


def setup(utils):
    class TextFormats(utils.BaseIndexer):

        def _get_content(self):
            with open(self.filename, 'rb') as fp:
                for line in fp:
                    line = self._decode_string(line)
                    if line.strip():
                        yield line.strip()

    PROVIDES.update({
        '.txt': utils.Plugin(TextFormats, 'text/plain'),
        '.rst': utils.Plugin(TextFormats, 'text/x-rst'),
    })
