import collections

import plyvel


class _Database(collections.MutableMapping):
    """
    LevelDB map interface
    """
    def __init__(self, db_name):
        self._db_name = db_name
        self._db = self._create()

    def _create(self):
        return plyvel.DB(self._db_name, create_if_missing=True)

    def __getitem__(self, key):
        if isinstance(key, str):
            key = key.encode('utf-8')
        return self._db.get(key)

    def __setitem__(self, key, val):
        if isinstance(key, str):
            key = key.encode('utf-8')
        return self._db.put(key, val)

    def __delitem__(self, key):
        if isinstance(key, str):
            key = key.encode('utf-8')
        self._db.delete(key)

    def keys(self):
        for k, _ in self._db:
            yield k

    def items(self):
        for k, v in self._db:
            yield k, v

    def __contains__(self, key):
        if isinstance(key, str):
            key = key.encode('utf-8')
        for k, _ in self._db:
            if k == key:
                return True
        return False

    def iterkeys(self):
        for k, _ in self._db:
            yield k
    __iter__ = iterkeys

    def __len__(self):
        count = 0
        for k, _ in self._db:
            count += 1
        return count

    def close(self):
        self._db.close()

    __del__ = close

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()


def open(file):
    return _Database(file)
