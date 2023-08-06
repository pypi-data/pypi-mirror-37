from bgpack.parse import AbstractParserGrouped


def filter_value(value, float_decimals=None):
    """Filter a float value to certain number of decimals"""
    return round(value, float_decimals)


def data_size(parser):
    """Read size of data of a parser (without consuming a line)"""
    if isinstance(parser, AbstractParserGrouped):
        for _, p in parser.get_parsers():
            _, *v = next(iter(p()))
            return len(v)
    elif isinstance(parser, dict):
        p = parser[list(parser.keys())[0]]
        _, *v = next(iter(p()))
        return len(v)
    else:
        _, *v = next(iter(parser()))
        return len(v)


def fmt(value, type):
    """Format a value with a specific format

    - f, float: convert to float
    - fX: convert t float with X decimals
    - i, int: convert to int

    """
    if type in ['f', 'float']:
        return float(value)
    elif type.startswith('f'):
        return filter_value(float(value), int(type[1:]))
    elif type in ['i', 'int']:
        return int(value)
    else:
        return value
