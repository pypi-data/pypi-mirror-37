# -*- coding: utf-8 -*-

import string

from collections import namedtuple

import chardet

try:
    import lxml
    from lxml import etree as et
except ImportError:
    lxml = False
    try:
        import xml.etree.cElementTree as et
    except ImportError:
        import xml.etree.ElementTree as et


Plugin = namedtuple('Plugin', 'handler mimetype')


_strip = string.digits + string.punctuation + string.whitespace


def extract_from_xml(xml):
    """Extracts all text content from xml.

    :parameters:
        xml : String
            XML document or fragment.

    :returns: List of all text content.
    :rtype: List
    """
    root = et.fromstring(xml)
    if lxml:
        return root.xpath('//text()')
    text = []
    for el in root.iter():
        if el.text is not None and el.text.strip():
            text.append(el.text.strip())
        if el.tail is not None and el.tail.strip():
            text.append(el.tail.strip())
    return text


class BaseIndexer:
    """Baseclass for the builtin indexer plugins. Third party plugins must
    not use this.

    :parameters:
        filename : String
            Name of the file to index.
    """

    def __init__(self, filename):
        self.filename = filename

    def _decode_string(self, s):
        try:
            res = chardet.detect(s)
            return str(s, res['encoding'])
        except UnicodeDecodeError:
            return ''

    def _get_content(self, encoding):
        """This method is called to get the file content line by line/block.

        :parameters:
            Encoding : String
                Encoding of `self.filename`.

        :returns: One line of `self.filename`.
        :rtype: String or Unicode
        """
        raise NotImplementedError

    def index(self):
        """Walks a line/block of the document and yields the single words
        with none alphanumeric characters stripped out.

        :parameters:
            encoding : String
                Encoding of `self.filename` (default: utf-8).

        :returns: One word.
        :rtype: Unicode
        """
        for line in self._get_content():
            for word in line.split():
                if not isinstance(word, str):
                    word = self._decode_string(word)
                    if not word:
                        continue
                yield word.strip(_strip)

    def get_full_text(self):
        """Returns the full extracted text of `self.filename`.

        :parameters:
            encoding : String
                Encoding of `self.filename` (default: utf-8).

        :returns: Extracted text.
        :rtype: Unicode
        """
        lines = []
        for line in self._get_content():
            if not isinstance(line, str):
                line = self._decode_string(line)
                if not line:
                    continue
            lines.append(line.strip())
        return ' '.join(lines)

    def get_properties(self, encoding='utf-8'):
        raise NotImplementedError
