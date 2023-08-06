# -*- coding: utf-8 -*-

from io import StringIO

from pdfminer.high_level import extract_text_to_fp
from pdfminer.layout import LAParams

PROVIDES = {}


def setup(utils):
    class PDF(utils.BaseIndexer):

        def _get_content(self):
            out = StringIO()
            laparams = LAParams()
            with open(self.filename, 'rb') as pdf:
                extract_text_to_fp(pdf, out, laparams=laparams)
            text = out.getvalue()
            out.close()
            text = text.replace('\r', ' ')
            return text.split('\n')

    PROVIDES['.pdf'] = utils.Plugin(PDF, 'application/pdf')
