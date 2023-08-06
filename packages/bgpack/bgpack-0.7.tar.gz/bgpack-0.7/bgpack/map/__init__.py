"""
The map module contains all the interfaces for the maps.
Maps are in charge of collecting all possible and different items
and translating them into the bytes for storing.

In the maps there are 3 types of items, each with 2 implementations

- Mappers
Mappers are the ones that receive all possible values,
and with them, generate the appropriate Map Writer

- Writers
Map Writers are the ones that receive a set (or sets)
with all distinct values from the Mappers and
associate them with a different key.
Each writer as an associated Mapper

- Readers
Map Reader do the inverse operation to Writer.
From the saved data, they return the original value


Each of those has 2 implementations.
One of them is optimized to work with single values
while the other should work with single and multiple values.
The reason for the existence of both is performance.
"""

from bgpack.globals import BGPackError


class MapError(BGPackError):
    """Base class fo mapper exceptions"""
    pass


class IMapper:
    """
    Interface for mappers.
    Mappers are constructors of maps.
    The can receive values (from a parser) and when done, you can get the map back
    """

    def add(self, *args):
        raise NotImplementedError

    def set_default_value(self, value):
        raise NotImplementedError

    def get(self):
        """
        If the data contains only one value, a :class:`Map` is returned.
        If the data consists of a set of values, a :class`MapManager` is returned
        """
        raise NotImplementedError


class IWriter:
    """
    Interface for MapWriters. Map Writers should return the value associated for each key
    Note that they are closely related to the packer and how it works.
    """

    def __getitem__(self, item):
        return NotImplemented

    def get(self, *args, **kwargs):
        """
        The get method is added to enable passing lists to the Manager.
        Just for convenience
        """
        raise NotImplementedError

    def get_reader(self):
        """Return the associated reader"""
        raise NotImplementedError


class IReader:
    """
    Interface for MapReaders.
    MapReaders should return the original value from each "key"/"index"
    They should have **nbits** and **nbytes** attributes and be able to be indexed by []
    Note that they are closely related to the reader and how it works.
    """

    def __getitem__(self, item):
        return NotImplemented
