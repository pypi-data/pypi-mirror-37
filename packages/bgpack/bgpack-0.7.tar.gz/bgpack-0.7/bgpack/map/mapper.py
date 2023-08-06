"""
Mappers are object used to create map writers.

Mappers hold (in sets) all the distinct values returned by the parser.
In addition they have a method to add a default value
and they should return the appropriate MapWriter

Here you can find 2 different implementations
one for parsers that return a single value
and another that returns more than one.
"""


from bgpack.map import MapError, IMapper


class AbstractMapper(IMapper):
    """
    Factory for mappers.
    It should work with parsers that return 1 or multiple values.
    However, when using 1 value, it might not be the most efficient way to do things.
    For that, you can use the :class:`MapperSingleValue`
    """

    def __init__(self):
        self.sets = None
        self.default_val = None

    def add(self, *args):
        if self.sets is None:  # no sets added
            self.sets = [{arg} for arg in args]
        else:
            for i, arg in enumerate(args):
                self.sets[i].add(arg)

    def set_default_value(self, value):
        if self.sets is None:
            raise MapError('Default value(s) cannot be set before values have been added')
        if not isinstance(value, (list, tuple)) or len(value) != len(self.sets):
            value = [value]*len(self.sets)
        for s, v in zip(self.sets, value):
            s.add(v)
        self.default_val = tuple(value)

    def get(self):
        raise NotImplementedError


class AbstractMapperSingleValue(set, IMapper):
    """Optimized version of :class:`AbstractMapper` to be used
    with parsers that send a single value"""

    def __init__(self):
        super().__init__()  # initialize the set
        self.default_val = None

    def set_default_value(self, value):
        self.add(value)
        self.default_val = value

    def get(self):
        raise NotImplementedError
