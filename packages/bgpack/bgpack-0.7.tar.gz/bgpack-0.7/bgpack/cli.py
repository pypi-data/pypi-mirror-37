import sys
from os import path

import bglogs
import click

from bgpack import main
from bgpack.globals import BGPackError


def exception_formatter(exception_type, exception, traceback, others_hook=sys.excepthook):
    """
    Reduce verbosity of error messages associated with BgQmapErrors

    Args:
        exception_type:
        exception:
        traceback:
        others_hook: hook for exceptions of a different class. Default is the system hook

    """
    if exception_type == BGPackError:
        print("%s: %s" % (exception_type.__name__, exception), file=sys.stderr)
    else:
        others_hook(exception_type, exception, traceback)


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option('--debug', is_flag=True, help='Enable debugging')
@click.version_option()
def cli(debug):
    if debug:
        bglogs.configure(debug=True)
        bglogs.debug('Debug mode enabled')
    else:
        bglogs.configure(debug=False)
        # Reduce the verbosity of the error messages
        sys.excepthook = exception_formatter


@cli.command(short_help='Create a packed file from a csv file')
@click.argument('file', metavar='<FILE>', type=click.Path(exists=True))
@click.option('--name', '-n', help='Name (without extension) for the packed file')
@click.option('--position', '-p', type=int, default=0, help='Column with the positions (zero-based index). Default to 0')
@click.option('--key', '-k', type=int, help='Column with the key. Default to None')
@click.option('--sep', default='\t', help='Column separator')
@click.option('--column', '-c', 'columns', multiple=True, metavar='COLUMN[.FORMAT]', help='Data column and format')
@click.option('--multi', '-m', 'multifile', is_flag=True, default=False, help='Create multiple files for each key')
def create(file, name, position, key, sep, columns, multifile):
    """
    Create a packed file from a csv file (<FILE>)

    The "--columns" options should be indicated once for each column.
    It can contain the column index and optionally a dot ('.') and a format
    see :func:`~bgpack.parser.utils.fmt` for more details.
    The key column can be added here to indicate a specific format.

    The key column is optional, if provided, for each key a new parser with the information is used.
    The file must be sorted by key and then by position

    When the file has a key column
    he "--multi" flag allows to create a separate file for each key.
    If not, all the data is set in the same file.

    \b
    E.g.:
    pack myfile.csv.gz --position 0 --sep , -c 1 -c 2.i -c 3.f2
    pack myfile2.tsv.gz --key 0 --position 1 --sep $'\\t' -c 2.i -c 3.f2
    """
    if name is None:
        name = path.basename(file).split('.')[0]

    if len(columns) == 0:
        columns = None

    parser_ = main.get_parser(file, position=position, key=key, cols=columns, sep=sep)

    main.pack(name, parser_, allow_multifile=multifile)


@cli.command(short_help='Read a packed file')
@click.argument('file', metavar='<FILE>', type=click.Path())
@click.option('--from', '-f', 'start', type=int, help='Start position')
@click.option('--to', '-t', 'stop', type=int, help='End position')
@click.option('--key', '-k', help='Key. Only required for packs with key')
@click.option('--sep', default='\t', help='Column separator')
def read(file, start, stop, key, sep):
    """Read a packed file"""
    file = file.replace('.bgpck', '')  # in case the user passes the file with extension
    unpacker = main.get_unpacker(file)

    kw = {}
    if start is not None:
        kw['start'] = start
    if stop is not None:
        kw['stop'] = stop
    if key is not None:
        kw['key'] = key

    with unpacker as r:
        for line in r.get(**kw):
            print(sep.join(map(str, line)))


if __name__ == "__main__":
    cli()
