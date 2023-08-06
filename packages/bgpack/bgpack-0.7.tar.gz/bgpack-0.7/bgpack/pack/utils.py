"""
This module contains function used when the reader returns a set of values
"""

import logging

from bgpack.implementation.implementation import factory
from bgpack.globals import BGPackError


def build_map(parser, mapper=None):
    """
    Compute index and start and stop position

    Args:
        parser (iterable, or dict): should return sorted pairs of position and value
        mapper (optional): mapper to fill. If not provided a new mapper is created

    Returns:
        tuple: mapper, start and stop

    """
    logging.getLogger(__name__).debug('Generating map')
    mapper = mapper or factory.get_mapper(single_value=False)()

    it = iter(parser())
    start, *first_value = next(it)  # get first value
    prev_pos = start
    mapper.add(*first_value)
    for pos, *value in it:
        if pos <= prev_pos:
            raise BGPackError('Positions are not sorted')
        mapper.add(*value)
        prev_pos = pos
    end = pos

    return mapper, start, end


def generate_data(parser, map_, default_value):
    """
    Generator for packed binary data

    Args:
        parser (iterable): should return sorted pairs of position and value
        map_ (dict):
        default_value: value to be used for missing positions

    Yields:
        bytearray: values to be saved

    """
    data = factory.get_packer()(map_)
    it = iter(parser())
    prev_pos, *value = next(it)  # get first value
    data.add(map_.get(*value))
    for pos, *value in it:  # add all values
        if pos > prev_pos + 1:
            for i in range(prev_pos+1, pos):  # add missing positions
                r = data.add_and_get(map_[default_value])
                if r is not None:
                    yield r
        r = data.add_and_get(map_.get(*value))
        if r is not None:
            yield r
        prev_pos = pos
    else:
        rest = data.get_rest()
        if rest is not None:
            yield rest


def build_map_single_value(parser, mapper=None):
    """
    Optimized version of :func:`build_map`
    for parsers that return single values
    """
    logging.getLogger(__name__).debug('Generating map for 1 value')
    mapper = mapper or factory.get_mapper(single_value=True)()

    it = iter(parser())
    start, first_value = next(it)  # get first value
    prev_pos = start
    mapper.add(first_value)
    for pos, value in it:
        if pos <= prev_pos:
            raise BGPackError('Positions are not sorted')
        mapper.add(value)
        prev_pos = pos
    end = pos

    return mapper, start, end


def generate_data_single_value(parser, map_, default_value):
    """
    Optimized version of :func:`generate_data`
    used to for single value maps
    """
    data = factory.get_packer()(map_)
    it = iter(parser())
    prev_pos, value = next(it)  # get first value
    data.add(map_[value])
    for pos, value in it:  # add all values
        if pos > prev_pos + 1:
            for i in range(prev_pos+1, pos):  # add missing positions
                r = data.add_and_get(map_[default_value])
                if r is not None:
                    yield r
        r = data.add_and_get(map_[value])
        if r is not None:
            yield r
        prev_pos = pos
    else:
        rest = data.get_rest()
        if rest is not None:
            yield rest
