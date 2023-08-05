from shelve import Shelf


class LevelDbfilenameShelf(Shelf):
    """Shelf implementation using leveldb as storage backend.

    This is initialized with the filename for the leveldb database.
    """

    def __init__(self, filename, protocol=None, writeback=False):
        from . import leveldb_map
        Shelf.__init__(self, leveldb_map.open(filename) , protocol, writeback)


def open(filename, protocol=None, writeback=False):
    """Open a persistent dictionary for reading and writing.

    The filename parameter is the base filename for the underlying
    database. The optional protocol parameter specifies the
    version of the pickle protocol.
    """

    return LevelDbfilenameShelf(filename, protocol, writeback)