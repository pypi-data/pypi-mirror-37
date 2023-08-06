"""Subpackage with parser utilites"""
from bgpack.globals import BGPackError


class ParserError(BGPackError):
    """Base class for parser errors"""
    pass


class IParser:
    """Parsers should be callable object that we can iterate through"""

    def __call__(self, *args, **kwargs):
        return self

    def __iter__(self):
        raise NotImplementedError


class AbstractParserGrouped:
    """Grouped parsers should yield pairs of key and parsers"""

    def get_parsers(self):
        raise NotImplementedError

    def items(self):
        """Just for compatibility with a dict of parsers"""
        return self.get_parsers()
