# -*- coding: utf-8 -*-

import re

from zipfile import ZipFile


PROVIDES = {}


def setup(utils):
    class OpenXMLBase(utils.BaseIndexer):

        def __init__(self, filename, pattern):
            utils.BaseIndexer.__init__(self, filename)
            self.pattern = pattern
            self.file_re = re.compile(pattern, re.I | re.U)

        def _open(self):
            content = []
            with ZipFile(self.filename) as zip:
                for name in zip.namelist():
                    if self.file_re.match(name) is not None:
                        content.append(zip.read(name))
            return content

        def _get_content(self):
            for stream in self._open():
                for block in utils.extract_from_xml(stream):
                    yield block

    class OpenXMLText(OpenXMLBase):

        def __init__(self, filename):
            OpenXMLBase.__init__(self, filename, r'word/document\.xml')

    class OpenXMLSpreadsheet(OpenXMLBase):

        def __init__(self, filename):
            OpenXMLBase.__init__(self, filename, r'xl/sharedStrings\.xml')

    class OpenXMLPresentation(OpenXMLBase):

        def __init__(self, filename):
            OpenXMLBase.__init__(self, filename, r'ppt/slides/slide\d+\.xml')

    PROVIDES.update({
        '.docx': utils.Plugin(
            OpenXMLText,
            'application/vnd.openxmlformats-'
            'officedocument.wordprocessingml.document'
        ),
        '.dotx': utils.Plugin(
            OpenXMLText,
            'application/vnd.openxmlformats-'
            'officedocument.wordprocessingml.template'
        ),
        '.docm': utils.Plugin(
            OpenXMLText,
            'application/vnd.ms-word.document.macroEnabled.12'
        ),
        '.dotm': utils.Plugin(
            OpenXMLText,
            'application/vnd.ms-word.template.macroEnabled.12'
        ),
        '.xlsx': utils.Plugin(
            OpenXMLSpreadsheet,
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        ),
        '.xltx': utils.Plugin(
            OpenXMLSpreadsheet,
            'application/vnd.openxmlformats-'
            'officedocument.spreadsheetml.template'
        ),
        '.xlsm': utils.Plugin(
            OpenXMLSpreadsheet,
            'application/vnd.ms-excel.sheet.macroEnabled.12'
        ),
        '.xltm': utils.Plugin(
            OpenXMLSpreadsheet,
            'application/vnd.ms-excel.template.macroEnabled.12'
        ),
        '.pptx': utils.Plugin(
            OpenXMLPresentation,
            'application/vnd.openxmlformats-'
            'officedocument.presentationml.presentation'
        ),
        '.potx': utils.Plugin(
            OpenXMLPresentation,
            'application/vnd.openxmlformats-'
            'officedocument.presentationml.template'
        ),
        '.ppsx': utils.Plugin(
            OpenXMLPresentation,
            'application/vnd.openxmlformats-'
            'officedocument.presentationml.slideshow'
        ),
        '.pptm': utils.Plugin(
            OpenXMLPresentation,
            'application/vnd.ms-powerpoint.presentation.macroEnabled.12'
        ),
        '.ppsm': utils.Plugin(
            OpenXMLPresentation,
            'application/vnd.ms-powerpoint.slideshow.macroEnabled.12'
        ),
    })
