import sys
from .config import get_config
from .. import fulltext
from .. import incremental
from ..ldoce5 import LDOCE5, NotFoundError, FilemapError, ArchiveError
from ..ldoce5.idmreader import is_ldoce5_dir
from ..utils.compat import range
from ..utils.text import (MATCH_OPEN_TAG, MATCH_CLOSE_TAG, ellipsis,
                          normalize_index_key)

# Identifiers for lazy-loaded objects
_LAZY_INCREMENTAL = 'incremental'
_LAZY_FTS_HWDPHR = 'fts_hwdphr'
_LAZY_FTS_DEFEXA = 'fts_defexa'
_LAZY_FTS_HWDPHR_ASYNC = 'fts_hwdphr_async'
_LAZY_SOUNDPLAYER = 'soundplayer'
_LAZY_ADVSEARCH_WINDOW = 'advsearch_window'
_LAZY_PRINTER = 'printer'
_FTS_HWDPHR_LIMIT = 10000
_INCREMENTAL_LIMIT = 500
_MAX_DELAY_UPDATE_INDEX = 100
_INTERVAL_AUTO_PRON = 50
_LOCAL_SCHEMES = frozenset(('dict', 'static', 'search', 'audio'))

_IS_OSX = sys.platform.startswith('darwin')

class MyLDOCE5():
    def __init__(self):
        # results
        self._incr_results = None
        self._fts_results = None
        self._found_items = None

        # status
        self._selection_pending = False
        self._loading_pending = False
        self._auto_fts_phrase = None

        # Lazy-loaded objects
        self._lazy = {}

        self.defexa = self._fts_defexa()
        self.hwdphr = self._fts_hwdphr()
        self.searcher = self._incremental()

        config = get_config()
        self.ldoce5 = LDOCE5("/isomedia/ldoce5.data", config.filemap_path)

    def _fts_defexa(self):
        obj = self._lazy.get(_LAZY_FTS_DEFEXA, None)
        if obj is None:
            config = get_config()
            try:
                obj = self._lazy[_LAZY_FTS_DEFEXA] = \
                        fulltext.Searcher(
                            config.fulltext_defexa_path,
                            config.variations_path)
            except (EnvironmentError, fulltext.IndexError):
                pass
        return obj

    def _fts_hwdphr(self):
        obj = self._lazy.get(_LAZY_FTS_HWDPHR, None)
        if obj is None:
            config = get_config()
            try:
                obj = self._lazy[_LAZY_FTS_HWDPHR] = fulltext.Searcher(
                        config.fulltext_hwdphr_path, config.variations_path)
            except (EnvironmentError, fulltext.IndexError):
                pass

        return obj

    def _incremental(self):
        obj = self._lazy.get(_LAZY_INCREMENTAL, None)
        if obj is None:
            try:
                obj = self._lazy[_LAZY_INCREMENTAL] = incremental.Searcher(
                        get_config().incremental_path)
            except (EnvironmentError, incremental.IndexError):
                pass
        return obj

    def search(self, key):
        return self.searcher.search(key, _INCREMENTAL_LIMIT)

    #filter result from Search()
    def filter_result(self, result, key_words):
        num = len(result)
        if num >3 :
            num = 3
        i = 0
        se = set()
        for item in result:
            if item[3] == 1 or item[3] == 2:
                real_key = item[2]
                diff_len = abs(len(real_key)-len(key_words))
                if diff_len < 4:
                    se.add(item[1])
            i = i + 1
            if i > num:
                break
        return se

    def load_content(self, path):
        error = 0
        try:
            (data, mime) = self.ldoce5.get_content(path)
        except:
            data = ""
            error = 1
        return (error, data)

