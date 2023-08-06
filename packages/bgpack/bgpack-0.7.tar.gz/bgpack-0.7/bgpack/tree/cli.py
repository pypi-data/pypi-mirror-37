"""
Mimic the :mod:`bgpack.cli` package with the tree implementation on top
"""

import sys
from os import path

import bglogs
import click

from bgpack.tree import main
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
