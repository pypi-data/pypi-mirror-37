# -*- coding: utf-8 -*-

"""TExtractor

Designed to extract text content out of the most filetypes in pure Python
and return the result as single words (e.g. for indexing).

Basic usage::

    >>> from textractor import TExtractor
    >>> indexer = TExtractor()
    >>> indexer.index('/path/to/test.pdf')
    ['Hello', 'World', 'test']
    >>> indexer.index('/path/to/test.pdf', drop=['test'])
    ['Hello', 'World']
    >>> indexer.index('/path/to/test.pdf', min_chars=5)
    ['Hello', 'World']

.. note::

   The test.pdf file in the example above only consists of
   "Hello World! test".
"""

import os

from pluginbase import PluginBase
from . import utils


PATH = os.path.dirname(os.path.abspath(__file__))
BUILTIN_PLUGIN_DIR = os.path.join(PATH, 'builtin_plugins')
FILLWORDS_DIR = os.path.join(PATH, 'fillwords')

plugin_base = PluginBase(package='textractor.plugins',
                         searchpath=[BUILTIN_PLUGIN_DIR])


def get_fillword_catalog(lang):
    filename = os.path.join(FILLWORDS_DIR, '{}.txt'.format(lang))
    drop = set()
    if os.path.isfile(filename):
        with open(filename) as fp:
            for line in fp:
                if line.strip():
                    drop.add(line.strip())
    return drop


def _make_name(name):
    """Helper function to make a filepath absolute and convert the filename
    extension to lowercase.

    :parameters:
        name : str
            Filename

    :returns: Absolute path to filename and extension lowered.
    :rtype: Tuple
    """
    ext = os.path.splitext(name)[1]
    return os.path.abspath(name), ext.lower()


class UnknownExtensionError(Exception):
    """Raised if a filename extension is not supported for indexing."""

    def __init__(self, ext):
        self.ext = ext

    def __str__(self):
        return 'Extension {} not registered.'.format(self.ext)


class TExtractor:
    """Object which manages the plugins and provides an equal API to all
    plugins.

    :parameters:
        plugin_dirs : list or str
            One or more dir(s) to search for plugins.
    """

    def __init__(self, plugin_dirs=None):
        if plugin_dirs is None:
            plugin_dirs = []
        elif isinstance(plugin_dirs, str):
            plugin_dirs = [plugin_dirs]
        self.plugins = []
        self.source = plugin_base.make_plugin_source(
            searchpath=plugin_dirs
        )
        self.indexer = {}
        self.load_plugins()
        self.build_map()

    @property
    def extensions(self):
        return dict((x, y.mimetype) for x, y in self.indexer.items())

    def load_plugins(self):
        """Imports all plugins."""
        for plugin_name in self.source.list_plugins():
            plugin = self.source.load_plugin(plugin_name)
            plugin.setup(utils)
            self.plugins.append(plugin)

    def build_map(self):
        """Builds the `self.indexer` dict (d[filename extension] = plugin)."""
        for plugin in self.plugins:
            for ext, plug in plugin.PROVIDES.items():
                self.indexer[ext] = plug

    def get(self, ext, filename):
        """Returns the matching indexer for `ext` or raises
        an error if `ext` is not found.

        :parameters:
            ext : str
                The filename extension (lowercase) to search.
            filename : str
                The full filename of the current file to index.

        :returns: The matching indexer for `ext`.
        :rtype: object
        :raises: UnknownExtensionError if `ext` is not known.
        """
        idx = self.indexer.get(ext)
        if idx is None:
            raise UnknownExtensionError(ext)
        return idx.handler(filename)

    def get_mimetype(self, filename):
        """Returns the mimetype of `filename`.

        :parameters:
            filename : str
                Full filename.

        :returns: The mimetype of the given file.
        :rtype: str
        :raises: UnknownExtensionError if the extentension is not known.
        """
        _, ext = _make_name(filename)
        if ext not in self.indexer:
            raise UnknownExtensionError(ext)
        return self.indexer[ext].mimetype

    def index(self, filename, min_chars=4, drop_fillwords=True, reverse=True,
              lang='en'):
        """Index the given file.

        :parameters:
            filename : str
                The name of the file to index.
            min_chars : int
                Minimum length of the words in the result list.
            drop_fillwords : bool
                Drop commonly known fillwords from the result.
            reverse : bool
                Return the result with longest first (default: True).
            lang : str
                Language to use for the fillwords (en, de).

        :returns: Words of the given `filename` matching the `min_chars`
                  and `drop` criteria sorted by word length
                  (default: longest first).
        :rtype: list
        """
        filename, ext = _make_name(filename)
        if drop_fillwords:
            drop = get_fillword_catalog(lang)
        else:
            drop = set()
        indexer = self.get(ext, filename)
        words = set()
        for word in indexer.index():
            if len(word) >= min_chars and word not in drop:
                words.add(word)
        words = list(words)
        words.sort(key=len, reverse=reverse)
        return words

    def get_properties(self, filename):
        """Extract meta information from `filename`.

        .. note:: Currently not implemented.

        """
        filename, ext = _make_name(filename)
        indexer = self.get(ext, filename)
        props = indexer.get_properties()
        return props

    def get_full_text(self, filename):
        """Get the full text of `filename`.

        :parameters:
            filename : str
                Filename to extract text from.

        :returns: The extracted text.
        :rtype: str
        """
        filename, ext = _make_name(filename)
        indexer = self.get(ext, filename)
        text = indexer.get_full_text()
        return text
