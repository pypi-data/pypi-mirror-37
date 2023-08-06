# -*- coding: utf-8 -*-

from zipfile import ZipFile


PROVIDES = {}


def setup(utils):
    class OpenDocumentFormat(utils.BaseIndexer):

        def _get_content(self):
            with ZipFile(self.filename) as zip:
                content = zip.read('content.xml')
            for block in utils.extract_from_xml(content):
                yield block

    ODF = OpenDocumentFormat
    _P = utils.Plugin

    PROVIDES.update({
        '.odt': _P(ODF, 'application/vnd.oasis.opendocument.text'),
        '.ods': _P(ODF, 'application/vnd.oasis.opendocument.spreadsheet'),
        '.odp': _P(ODF, 'application/vnd.oasis.opendocument.presentation'),
        '.odm': _P(ODF, 'application/vnd.oasis.opendocument.text-master'),
        '.ott': _P(ODF, 'application/vnd.oasis.opendocument.text-template'),
        '.ots': _P(ODF, 'application/vnd.oasis.opendocument.spreadsheet-'
                   'template'),
        '.otp': _P(ODF, 'application/vnd.oasis.opendocument.presentation-'
                   'template')
    })
