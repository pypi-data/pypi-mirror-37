"""
Byte array mappers

Writer is bytes-based: value -> byte arr

Writer is bytes-based:  value1, value2... -> byte array
Each value contributes with a part to the byte array
value1 -> bytearr1, value2 -> bytearr2, ... => bytearr1 '+' bytearr2 ... = bytarr

Reader is bytes-based:  byte array --> value

Reader Manager is bytes-based:  byte array --> value1, value2, ...
Each byte array is divided for each value
byte array -> bytearr1 -> value1
           -> bytearr2 -> value2
"""

from bgpack.map import IWriter, IReader, IMapper, utils as mapper_utils
from bgpack.map.mapper import AbstractMapper, AbstractMapperSingleValue
from bgpack.utils import required_bytes


class MapWriter(dict, IWriter):
    """
    Map reader where keys are integer
    The number of bits is the smallest for a struct
    """

    def __init__(self, set_):
        self.nbytes = required_bytes(len(set_))
        self.update({v: i.to_bytes(self.nbytes, byteorder='big', signed=False) for i, v in enumerate(set_)})

    def get_reader(self):
        return MapReader(self)


class MapReader(dict, IReader):
    """
    Base class for map readers. For a index entered return the associated value
    """
    def __init__(self, writer):
        self.nbytes = writer.nbytes
        self.nbits = self.nbytes * 8
        self.update({v: k for k, v in writer.items()})


class MapWriterManager(IMapper):
    """
    Manager of a set of maps.
    For a set of values entered, return the associated index
    """

    def __init__(self, maps):

        # Convert to tuples for efficiency
        self.maps = tuple(maps)

    def __getitem__(self, item):
        result = b''
        for map_, v in zip(self.maps, item):
            result += map_[v]
        return result

    def get(self, *args):
        return self.__getitem__(args)

    def get_reader(self):
        if len(self.maps) == 1:
            return self.maps[0].get_reader()
        else:
            return MapReaderManager([map_.get_reader() for map_ in self.maps])


class MapReaderManager(IReader):
    """
    Manager of a set of maps.
    For an index entered returns a set of values associated
    """

    def __init__(self, list_of_maps):

        self.maps = list_of_maps

        nbytes_list = [map_.nbytes for map_ in self.maps]
        self.nbytes = sum(nbytes_list)
        self.nbits = self.nbytes * 8

        self.slices = []
        self._create_slices(nbytes_list)

        self.slice_and_map = tuple(zip(self.slices, self.maps))

    def _create_slices(self, nbytes_list):
        prev = 0
        for v in nbytes_list:
            self.slices.append(slice(prev, prev + v))
            prev += v

    def __getitem__(self, item):
        return tuple([map_[item[slice_]] for slice_, map_ in self.slice_and_map])


class MapperSingleValue(AbstractMapperSingleValue):

    def get(self):
        return MapWriter(self), self.default_val


class Mapper(AbstractMapper):

    def get(self):

        if len(self.sets) == 1:
            return MapWriter(self.sets[0]), self.default_val[0] if self.default_val is not None else None
        else:
            maps = mapper_utils.optimize_sets(self.sets, bits_function=required_bytes, map_writer_class=MapWriter)
            return MapWriterManager(maps), self.default_val
