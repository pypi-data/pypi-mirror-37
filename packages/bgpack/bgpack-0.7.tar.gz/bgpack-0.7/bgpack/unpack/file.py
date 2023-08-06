
import mmap

from bgpack.unpack import IUnpacker


class Unpacker(IUnpacker):

    def __init__(self, name, metadata):
        """
        Base class for single file reader of indexed files

        Args:
            name (str): name of the pack files

        """
        self.fd = None
        self.mm = None
        self.offset = 0
        self.file_path = name + '.bgpck'

        self.default_value = metadata['default']
        self.index = metadata['index']

        self.nbits = self.index.nbits
        self.nbytes = self.index.nbytes

    def __enter__(self):
        self.fd = open(self.file_path, 'rb')
        self.mm = mmap.mmap(self.fd.fileno(), 0, access=mmap.ACCESS_READ)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.mm.close()
        self.fd.close()


def get(value_unpacker_class, with_offsets=False):
    """Returns the right class for the reader"""

    class Unpacker_(value_unpacker_class, Unpacker):
        """Single file reader"""

        def __init__(self, name, metadata):
            super().__init__(name, metadata)

            self.start = metadata['start']
            self.stop = metadata['stop']
            self.init = metadata['init']
            self.end = metadata['end']

    class UnpackerWithOffsets(value_unpacker_class, Unpacker):
        """File with offsets"""

        def __init__(self, name, metadata):
            super().__init__(name, metadata)

            self.start = None
            self.stop = None
            self.init = None
            self.end = None

            self.offsets = metadata['offsets']
            self.positions = metadata['positions']

        def get(self, key, start=None, stop=None):

            self.offset = self.offsets[key]
            self.start, self.stop, self.init, self.end = self.positions[key]

            return super().get(start, stop)

    return UnpackerWithOffsets if with_offsets else Unpacker_
