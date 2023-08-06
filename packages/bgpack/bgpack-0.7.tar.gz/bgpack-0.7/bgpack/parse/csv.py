import functools
import gzip
import logging

from bgpack.parse import IParser, AbstractParserGrouped, ParserError
from bgpack.parse.utils import fmt


class _CSV:

    def __init__(self, file, position=0, columns=None, formats=None, sep='\t'):
        """
        Base class for CSV text parsers

        Args:
            file (str): filepath
            position (int): column of the position. Default is column 0
            columns (list, optional): list of column to keep (default all)
            formats (dict, optional): formats to apply to each column
            sep (str, optinal): separator for the columns
        """
        self.file = file
        self.fd = None

        self.pos = position
        self.sep = sep

        # Columns to be included
        if columns is None:
            self.columns = None
        else:
            self.columns = [self.pos] + columns

        self.formats = {self.pos: 'int'}
        if formats is not None:
            self.formats.update(formats)

        if self.file.endswith('.gz'):
            self.open = functools.partial(gzip.open,  mode='rt')
        else:
            self.open = functools.partial(open, mode='r')

    def _iscomment(self, line):
        return line.startswith('#')


class CSV(_CSV, IParser):

    @staticmethod
    def parse(line, pos_index, sep='\t', columns=None, formats=None):
        """
        Parse text lines

        Args:
            line (str): text line
            pos_index (int): column index of the position
            sep (str, optional): separator to use to split the line. Default is tab
            columns (list, optional): index of columns to keep (by default all)
            formats (dict): apply specific format to certain columns.
              If no format is indicated, is is assumed to be text.
              See :func:`~bgpack.parser.utils.fmt` for more details on formats

        Returns:
            tuple: position and a list of parsed values

        """
        formats = formats or {}
        data = []
        pos = None
        values = line.strip().split(sep)
        for i, v in enumerate(values):
            if columns is None or i in columns:
                if i in formats:
                    v = fmt(v, formats[i])
                if i == pos_index:
                    pos = v
                else:
                    data.append(v)
        return pos, data

    def __init__(self, file, position=0, columns=None, formats=None, sep='\t'):
        """
        Parser for CSV files

        Args:
            file (str): filepath
            position (int): column of the position. Default is column 0
            columns (list, optional): list of column to keep (default all)
            formats (dict, optional): formats to apply to each column
            sep (str, optinal): separator for the columns

        """
        super().__init__(file, position=position, columns=columns, formats=formats, sep=sep)

        self.parse = functools.partial(CSV.parse, pos_index=self.pos, sep=self.sep, columns=self.columns, formats=self.formats)

        logging.getLogger(__name__).debug('Column %d is the position' % self.pos)

    def __iter__(self):
        with self.open(self.file) as fd:
            for line in fd:
                if not self._iscomment(line):
                    pos, data = self.parse(line)
                    yield (pos,) + tuple(data)


class CSVGrouped(_CSV, AbstractParserGrouped):

    @staticmethod
    def parse(line, pos_index, key_index, sep='\t', columns=None, formats=None):
        """
        Parse text lines

        Args:
            line (str): text line
            pos_index (int): column index of the position
            key_index (int): column index of the position
            sep (str, optional): separator to use to split the line. Default is tab
            columns (list, optional): index of columns to keep (by default all)
            formats (dict): apply specific format to certain columns.
              If no format is indicated, is is assumed to be text.
              See :func:`~bgpack.parser.utils.fmt` for more details on formats

        Returns:
            tuple: position, key and a list of parsed values

        """
        formats = formats or {}
        data = []
        pos = None
        key = None
        values = line.strip().split(sep)
        for i, v in enumerate(values):
            if columns is None or i in columns:
                if i in formats:
                    v = fmt(v, formats[i])
                if i == pos_index:
                    pos = v
                elif i == key_index:
                    key = v
                else:
                    data.append(v)
        return pos, key, data

    def __init__(self, file, key_column=0, position=1, columns=None, formats=None, sep='\t'):
        """

        Args:
            file (str): filepath
            key_column (int): column of the key. Default is column 0
            position (int): column of the position. Default is column 1
            columns (list, optional): list of column to keep (default all)
            formats (dict, optional): formats to apply to each column
            sep (str, optinal): separator for the columns

        """

        if key_column == position:
            raise ParserError('Index of key columm and position column cannot be the same')

        super().__init__(file, position=position, columns=columns, formats=formats, sep=sep)

        self.key = key_column
        if self.columns is not None:
            self.columns.append(self.key)

        logging.getLogger(__name__).debug('Column %d is the key, column %d is the position ' %
                                          (self.key, self.pos))

    def get_parsers(self):
        """

        Yield:
            tuple: key and the associated parser for that key

        """
        current_key = None
        first_val = None

        sep = self.sep
        columns = self.columns
        formats = self.formats
        key_pos = self.key
        pos_pos = self.pos

        keep_going = True

        with self.open(self.file) as fd:
            while keep_going:

                # Read first key and first value skipping comments
                if current_key is None:
                    for line in fd:
                        if self._iscomment(line):
                            continue
                        position, current_key, data = CSVGrouped.parse(line, pos_index=pos_pos, key_index=key_pos, sep=sep, columns=columns, formats=formats)
                        first_val = (position,) + tuple(data)
                        break

                # Create a parser
                def parser():
                    nonlocal current_key, first_val, keep_going

                    yield first_val

                    for line in fd:
                        position, this_key, data = CSVGrouped.parse(line, pos_index=pos_pos, key_index=key_pos, sep=sep, columns=columns, formats=formats)
                        if this_key != current_key:
                            current_key = this_key
                            first_val = (position,) + tuple(data)
                            break
                        else:
                            yield (position,) + tuple(data)
                    else:
                        keep_going = False

                logging.getLogger(__name__).debug('Parser for key: %s' % current_key)

                yield current_key, parser
