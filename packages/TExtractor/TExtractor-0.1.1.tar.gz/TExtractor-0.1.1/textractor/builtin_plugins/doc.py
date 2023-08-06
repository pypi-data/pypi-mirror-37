# -*- coding: utf-8 -*-

import re


PROVIDES = {}

preserve_re = re.compile(r'[^a-zA-Z0-9\s\,\.\-\n\r\t@\/\_\(\)]')
whitespace_re = re.compile(r'\s+')


def setup(utils):
    class BinaryMSWord(utils.BaseIndexer):

        def _get_content(self):
            with open(self.filename, 'rb') as doc:
                data = doc.read()
            for line in data.split(b'\x0D'):
                if line.find(b'\x00') == -1 and line.strip():
                    s = str(line.strip(), 'cp1252', errors='replace')
                    s = preserve_re.sub('', s)
                    s = whitespace_re.sub(' ', s)
                    yield s

    PROVIDES['.doc'] = utils.Plugin(BinaryMSWord, 'application/msword')
