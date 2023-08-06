# -*- coding: utf-8 -*-

from setuptools import setup


classifiers = [
    'Development Status :: 4 - Beta',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3',
    'Topic :: Software Development :: Libraries :: Python Modules',
]


setup(
    name='TExtractor',
    version='0.1.1',
    packages=['textractor'],
    install_requires=['pdfminer.six', 'pluginbase', 'chardet'],
    url='http://bitbucket.org/whitie/textractor-py3/',
    license='MIT',
    author='Thorsten Weimann',
    author_email='weimann.th@yahoo.com',
    description='Extract text content from many filetypes.',
    long_description=open('README').read(),
    long_description_content_type='text/x-rst',
    classifiers=classifiers,
    keywords='text extract pdf docx',
)
