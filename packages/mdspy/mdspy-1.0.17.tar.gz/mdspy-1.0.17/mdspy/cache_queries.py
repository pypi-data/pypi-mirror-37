import hashlib
import json
import logging
import os

from aiotstudio.datasource import search_df
from fastparquet import write, ParquetFile


class q_cacher:

    def __init__(self, cache_directory='parquet'):
        self.parquet_dir = cache_directory + '/'
        if not os.path.exists(self.parquet_dir):
            os.makedirs(self.parquet_dir)

    def _get_hash(self, query):
        hash_object = hashlib.sha1(json.dumps(query).encode('utf-8'))
        hex_dig = hash_object.hexdigest()
        return hex_dig

    def remove_cache_for(self, q, suffix=''):
        filename = self._create_fileName(q, suffix)
        os.remove(filename)

    def _is_query_cacheable(self, q):
        list_forbidden_keyword = ['thisMonth', 'now', 'sevenDaysAgo', 'today', 'yesterday', 'thirtyDaysAgo',
                                  'thisMonth',
                                  'lastMonth', 'thisQuarter', 'lastQuarter', 'thisYear', 'lastYear']
        for k in list_forbidden_keyword:
            if k.lower() in str(q).lower():
                return False
        return True

    def get_data_form_query(self, q, force=False):
        log = logging.getLogger()
        if self._is_data_cached(q) and not force:
            log.info('reading from cache')
            return self._get_data_from_cache(q)
        else:
            log.info('loading from smartobject')
            res = search_df(q)
        assert len(res) < 100000, str(q)
        if self._is_query_cacheable(q):
            self._save_df(res, q)
        return res

    def _create_fileName(self, q, suffix=''):
        if suffix != '':
            return self.parquet_dir + self._get_hash(q) + '_' + suffix + '.parq'
        return self.parquet_dir + self._get_hash(q) + '.parq'

    def _save_df(self, df, q, suffix=''):
        filename = self._create_fileName(q, suffix)
        write(filename, df, compression='SNAPPY')

    def _is_data_cached(self, q, suffix=''):
        filename = self._create_fileName(q, suffix)
        return os.path.isfile(filename)

    def _get_data_from_cache(self, q, suffix=''):
        filename = self._create_fileName(q, suffix)
        return ParquetFile(filename).to_pandas()
