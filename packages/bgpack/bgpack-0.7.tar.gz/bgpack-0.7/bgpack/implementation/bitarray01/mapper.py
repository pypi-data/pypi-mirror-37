"""
Bit array using 0s and 1s mappers

Writer is int-based: value -> int

Writer manager is int-based:  value1, value2... -> int
Each value is got from each own map, and then values are added after a swift
value1 -> int1, value2 -> int2 ...  => int1 << x + int2 << y + ... = int

Reader is 01 str based  01010101: --> value

Reader Manager is 01 str based:  0101110101 --> value1, value2, ...
Each 01 str is divided for each value
010101010101 -> 0101 -> value1
             -> 00111 -> value2
             ...
"""

from bgpack.map import IMapper, IReader, IWriter, utils as mapper_utils
from bgpack.map.mapper import AbstractMapper, AbstractMapperSingleValue
from bgpack.utils import required_bits, bytes4bits


class MapWriter(dict, IWriter):
    """
    Map reader where the keys are associated with a binary string 01
    The number of bits is the smallest possible
    """

    def __init__(self, set_):
        self.nbits = required_bits(len(set_))
        self.update({v: i for i, v in enumerate(set_)})

    def get_reader(self):
        return MapReader(self)


class MapReader(dict, IReader):
    """
    Base class for map readers. For a index entered return the associated value
    """
    def __init__(self, writer):
        self.nbits = writer.nbits
        self.nbytes = bytes4bits(self.nbits)
        self.fmt = '{{:0{}b}}'.format(self.nbits)
        self.update({self._pos_to_key(v): k for k,v in writer.items()})

    def _pos_to_key(self, pos):
        return self.fmt.format(pos)


class MapWriterManager(IMapper):
    """
    Manager of a set of maps.
    For a set of values entered, return the associated index
    """

    def __init__(self, maps):
        self.maps = maps

        self.nbits_list = [map_.nbits for map_ in self.maps]
        self.nbits_list.append(0)  # add a final value to the list

        self.nbits = sum(self.nbits_list)

        # Convert to tuples for efficiency
        self.maps = tuple(self.maps)
        self.nbits_list = tuple(self.nbits_list)

    def __getitem__(self, item):
        result = 0
        for i, v in enumerate(item):
            result += self.maps[i][v]
            result = result << self.nbits_list[i+1]
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

        self.nbits_list = [map_.nbits for map_ in self.maps]
        self.nbits = sum(self.nbits_list)
        self.nbytes = bytes4bits(self.nbits)

        self.slices = []
        self._create_slices()

        self.slice_and_map = tuple(zip(self.slices, self.maps))

    def _create_slices(self):
        prev = 0
        for v in self.nbits_list:
            self.slices.append(slice(prev, prev+v))
            prev += v

    def __getitem__(self, item):
        return tuple([map_[item[slice_]] for slice_, map_ in self.slice_and_map])


class Mapper(AbstractMapper):

    def get(self):

        if len(self.sets) == 1:
            return MapWriter(self.sets[0]), self.default_val[0] if self.default_val is not None else None
        else:
            maps = mapper_utils.optimize_sets(self.sets, bits_function=required_bits, map_writer_class=MapWriter)
            return MapWriterManager(maps), self.default_val


class MapperSingleValue(AbstractMapperSingleValue):
    """Optimized version of :class:`Mapper` for single value maps"""
    def get(self):
        return MapWriter(self), self.default_val
