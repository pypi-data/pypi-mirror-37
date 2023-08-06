from intervaltree import IntervalTree

from bgpack.parse import IParser, AbstractParserGrouped, ParserError


class Wrapper(IParser):

    def __init__(self, parser):
        self.parser = parser
        self.tree = None

    def __iter__(self):
        self.tree = IntervalTree()
        it = iter(self.parser())
        first = next(it)  # get first value
        pos_prev = first[0]
        yield first
        offset = 0
        interval_start = pos_prev
        for pos, *values in it:
            if pos == pos_prev + 1:  # continuous case
                yield (pos - offset,) + tuple(values)
            elif pos < pos_prev - 1:
                raise ParserError('Positions are not sorted')
            else:  # there is a gap with missing values
                self.tree.addi(interval_start, pos_prev + 1, offset)
                offset += pos - pos_prev - 1
                interval_start = pos
                yield (pos - offset,) + tuple(values)

            pos_prev = pos

        # Add last interval (only if needed)
        if not self.tree[pos]:
            self.tree.addi(interval_start, pos + 1, offset)


class WrapperGrouped(AbstractParserGrouped):

    def __init__(self, parser):
        self.parser = parser
        self.tree = {}

    def get_parsers(self):
        for name, parser in self.parser.get_parsers():
            p = Wrapper(parser)
            yield name, p
            self.tree[name] = p.tree
