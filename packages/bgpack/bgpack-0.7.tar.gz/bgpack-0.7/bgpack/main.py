import gzip
import pickle

from bgpack.implementation import implementation
from bgpack.pack import pack as pack_mod
from bgpack.parse import AbstractParserGrouped, csv as parser_csv
from bgpack.unpack import file as unpack_file, files as unpack_files


def get_parser(file, position, key=None, cols=None, sep='\t'):

    # Get columns an formats
    if cols is None:
        columns = None
        formats = None
    else:
        columns = []
        formats = {}
        for col in cols:
            v = col.split('.')
            c = int(v[0])
            columns.append(c)
            if len(v) == 2:  # columns with format
                formats[c] = v[1]

    if key is None:
        return parser_csv.CSV(file, position=position, columns=columns, formats=formats, sep=sep)
    else:
        return parser_csv.CSVGrouped(file, key_column=key, position=position, columns=columns, formats=formats, sep=sep)


def pack(output_name, parser, default_value=None, init_pos=None, end_pos=None, allow_multifile=True, optimize_for=None):
    """
    Construct packed file and associated metadata file

    Args:
        output_name (str): name of the file used for the data
        parser (iterable or dict): should return sorted pairs of position and value(s)
        default_value (optional): value for missing positions
        init_pos (int, optional): initial position
        end_pos (int, optional): final position
        allow_multifile (bool, optional): whether to force to use a single or multiple files.
          Has only effect when a dict of parsers is used
        optimize_for (str, optional): information used for optimization.
          See :meth:`~bgpack.implementation.implementation.Factory.set`

    Init and end positions are retrieved from the data if not provided.
    """
    implementation.factory.set(optimize_for)
    if isinstance(parser, (dict, AbstractParserGrouped)):
        return pack_mod.multiple(output_name, parser, default_value=default_value, init_pos=init_pos, end_pos=end_pos, ismultifile=allow_multifile)
    else:
        return pack_mod.single(output_name, parser, default_value=default_value, init_pos=init_pos, end_pos=end_pos)


def get_unpacker(name, unpacked=True):
    """
    Loads the right reader for the data

    Args:
        name (str): filename
        unpacked (bool, optional): flag indicating whether to return the values unpacked
          or as a tuple. The second option is faster

    Returns:
        Reader: reader object for the data

    """
    with gzip.open('{}.pkl.gz'.format(name), 'rb') as fd:
        metadata = pickle.load(fd)

    implementation.factory.set(metadata['implementation'])

    issinglevalue = True if metadata['issimple'] or not unpacked else False
    value_unpack_class = implementation.factory.get_unpacker(single_value=issinglevalue)

    if metadata['ismultifile']:
        Unpacker = unpack_files.get(value_unpack_class)
    else:
        hasoffsets = 'offsets' in metadata
        Unpacker = unpack_file.get(value_unpack_class, with_offsets=hasoffsets)

    return Unpacker(name, metadata)
