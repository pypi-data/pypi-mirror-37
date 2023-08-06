
import gzip
import pickle

from bgpack.implementation import implementation
from bgpack.pack import utils
from bgpack.parse import utils as parser_utilities


def _get_functions(data_size):
    """Choose the right functions"""
    if data_size == 1:
        issimple = True
        build_map = utils.build_map_single_value
        generate_data = utils.generate_data_single_value
    else:
        issimple = False
        build_map = utils.build_map
        generate_data = utils.generate_data
    return issimple, build_map, generate_data


def _write_data(filename, iterator):
    with open(filename, 'wb', 16 * 1024 * 1024) as fd_out:
        for values in iterator:
            fd_out.write(values)


def _save_metadata(filename, metadata):
    with gzip.open(filename, 'wb') as fd:
        pickle.dump(metadata, fd)


def single(output_name, parser, default_value=None, init_pos=None, end_pos=None):
    """
    Construct packed file and associated metadata file

    Args:
        output_name (str): name of the file used for the data
        parser (iterable): should return sorted pairs of position and value
        default_value (optional): value for missing positions
        init_pos (int, optional): initial position
        end_pos (int, optional): final position

    Init and end positions are retrieved from the data if not provided.
    """

    size = parser_utilities.data_size(parser)
    # Choose between single or multiple values
    issimple, build_map, generate_data = _get_functions(size)

    mapper, start, stop = build_map(parser)
    mapper.set_default_value(default_value)
    map_, def_val = mapper.get()

    metadata = {'start': start, 'stop': stop, 'init': init_pos or start, 'end': end_pos or stop,
                'default': def_val, 'index': map_.get_reader(), 'issimple': issimple, 'ismultifile': False,
                'implementation': implementation.factory.get()}

    _write_data('{}.bgpck'.format(output_name), generate_data(parser, map_, def_val))

    _save_metadata('{}.pkl.gz'.format(output_name), metadata)


def multiple(output_name, parsers, default_value=None, init_pos=None, end_pos=None, ismultifile=True):

    size = parser_utilities.data_size(parsers)
    # Choose between single or multiple values
    issimple, build_map, generate_data = _get_functions(size)

    positions = {}  # for each file to be created add a tuple (filename, start, stop, init, end)
    mapper = None
    for name, parser in parsers.items():
        mapper, start, stop = build_map(parser, mapper)

        ip = init_pos.get(name, None) if isinstance(init_pos, dict) else init_pos
        ep = end_pos.get(name, None) if isinstance(end_pos, dict) else end_pos

        initial_pos = start if ip is None else ip  # ip or start wont work for 0 values
        final_pos = stop if ep is None else ep

        positions[name] = (start, stop, initial_pos, final_pos)

    mapper.set_default_value(default_value)
    map_, def_val = mapper.get()

    metadata = {'positions': positions, 'default': def_val, 'index': map_.get_reader(), 'issimple': issimple,
                'ismultifile': ismultifile, 'implementation': implementation.factory.get()}

    if ismultifile:
        for name, parser in parsers.items():
            _write_data('{}__{}.bgpck'.format(output_name, name), generate_data(parser, map_, def_val))
    else:
        filename = '{}.bgpck'.format(output_name)
        offsets = {}
        byteswritten = 0
        with open(filename, 'wb', 16 * 1024 * 1024) as fd_out:
            for name, parser in parsers.items():
                offsets[name] = byteswritten
                for values in generate_data(parser, map_, def_val):
                    byteswritten += len(values)
                    fd_out.write(values)
        metadata['offsets'] = offsets

    _save_metadata('{}.pkl.gz'.format(output_name), metadata)
