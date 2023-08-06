# -*- coding: utf-8 -*-

from setuptools import setup


__name__ = 'TExtractor'
__author__ = 'Thorsten Weimann'
__author_email__ = 'weimann.th@yahoo.com'
__version__ = '0.1'
__release__ = __version__
__url__ = 'http://bitbucket.org/whitie/textractor2/'
__license__ = 'MIT'
__description__ = 'Extract text content from many filetypes.'
__classifiers__ = [
    'Development Status :: 4 - Beta',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3',
    'Topic :: Software Development :: Libraries :: Python Modules',
]


setup(
    name=__name__,
    version=__release__,
    packages=['textractor'],
    install_requires=['pdfminer.six', 'pluginbase', 'chardet'],
    url=__url__,
    license=__license__,
    author=__author__,
    author_email=__author_email__,
    description=__description__,
    long_description=open('README').read(),
    long_description_content_type='text/x-rst',
    classifiers=__classifiers__,
    keywords='text extract pdf docx',
)
