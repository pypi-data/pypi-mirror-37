
import mmap

from bgpack.unpack import IUnpacker
from bgpack.globals import BGPackError


class Unpacker(IUnpacker):

    def __init__(self, name, metadata, restrictto=None):
        """
        Base class for reader for multiple indexed files

        Args:
            name (str): name of the pack files
            metadata (dict):
            restrictto (list, optional): list of keys to restrict the data to.
              If None are provided, all are used

        """
        self.fd = None
        self.mm = None
        self.start = None
        self.stop = None
        self.init = None
        self.end = None
        self.offset = 0

        self.file_path = name + '__{}.bgpck'

        if restrictto is None:
            self.positions = metadata['positions']
        else:
            self.positions = {k: v for k, v in metadata['positions'] if k in restrictto}

        self.names = [name for name in self.positions.keys()]
        if not self.names:
            raise BGPackError('No files found')

        self.default_value = metadata['default']
        self.index = metadata['index']

        self.nbits = self.index.nbits
        self.nbytes = self.index.nbytes

    def __enter__(self):
        self.fds = {}
        self.mms = {}
        for name in self.names:
            fd = open(self.file_path.format(name), 'rb')
            self.fds[name] = fd
            self.mms[name] = mmap.mmap(fd.fileno(), 0, access=mmap.ACCESS_READ)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        for name in self.names:
            self.mms[name].close()
            self.fds[name].close()


def get(value_unpacker_class):
    """Returns the right class for the reader"""

    class Unpacker_(value_unpacker_class, Unpacker):

        def get(self, key, start=None, stop=None):

            self.mm = self.mms[key]
            self.start, self.stop, self.init, self.end = self.positions[key]

            return super().get(start, stop)

    return Unpacker_
