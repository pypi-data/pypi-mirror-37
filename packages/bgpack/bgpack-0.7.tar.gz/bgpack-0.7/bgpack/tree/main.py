"""
Mimic the :mod:`bgpack.main` package with the tree implementation on top
"""


import gzip
import pickle

from bgpack.parse import AbstractParserGrouped
from bgpack import main as bgpack_main
from bgpack.tree import parser as tree_parser, unpacker as tree_unpacker


def _save_tree(name, tree):
    with gzip.open('{}.tree.pkl.gz'.format(name), 'wb') as fd:
        pickle.dump(tree, fd)


def _load_tree(name):
    with gzip.open('{}.tree.pkl.gz'.format(name), 'rb') as fd:
        return pickle.load(fd)


def get_parser(*args, **kwargs):
    parser = bgpack_main.get_parser(*args, **kwargs)

    if isinstance(parser, AbstractParserGrouped):
        return tree_parser.WrapperGrouped(parser)
    else:
        return tree_parser.Wrapper(parser)


def pack(output_name, parser, *args, **kwargs):

    if isinstance(parser, AbstractParserGrouped):
        parser_ = tree_parser.WrapperGrouped(parser)
    elif isinstance(parser, dict):
        parser_ = {k: tree_parser.Wrapper(v) for k, v in parser.items()}
    else:
        parser_ = tree_parser.Wrapper(parser)

    bgpack_main.pack(output_name, parser_, *args, **kwargs)

    if isinstance(parser, AbstractParserGrouped):
        tree = parser_.tree
    elif isinstance(parser, dict):
        tree = {k: v.tree for k, v in parser_.items()}
    else:
        tree = parser_.tree

    _save_tree(output_name, tree)


def get_unpacker(name, *args, **kwargs):
    tree = _load_tree(name)

    unpacker = bgpack_main.get_unpacker(name, *args, **kwargs)

    with gzip.open('{}.pkl.gz'.format(name), 'rb') as fd:
        metadata = pickle.load(fd)

    if 'positions' in metadata:
        return tree_unpacker.UnpackerKeyed(tree, unpacker)
    else:
        return tree_unpacker.Unpacker(tree, unpacker)
