from bgpack.implementation.bitarray01 import mapper as bitarray01mapper, packer as bitarray01packer, unpacker as bitarray01unpacker
from bgpack.implementation.bytearray import mapper as bytearraymapper, packer as bytearraypacker, unpacker as bytearrayunpacker
from bgpack.globals import BGPackError


class Factory:

    def __init__(self):
        self.mapper = bytearraymapper
        self.packer = bytearraypacker
        self.unpacker = bytearrayunpacker
        self.optimization = 'size'

    def set(self, optimize_for):
        if optimize_for in ['s', 'S', 'size']:
            self.mapper = bitarray01mapper
            self.packer = bitarray01packer
            self.unpacker = bitarray01unpacker
            self.optimization = 'size'
        elif optimize_for is None or optimize_for in ['r', 'R', 'read']:
            self.mapper = bytearraymapper
            self.packer = bytearraypacker
            self.unpacker = bytearrayunpacker
            self.optimization = 'read'
        else:
            raise BGPackError('This option is not valid. Valid options are: "size" and "read"')

    def get(self):
        return self.optimization

    def get_mapper(self, single_value=False):
        if single_value:
            return self.mapper.MapperSingleValue
        else:
            return self.mapper.Mapper

    def get_packer(self):
        return self.packer.Packer

    def get_unpacker(self, single_value=False):
        if single_value:
            return self.unpacker.UnpackerSingleValue
        else:
            return self.unpacker.Unpacker


factory = Factory()
