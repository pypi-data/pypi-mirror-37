"""
Package with the logic for the reading the values from the packed file.

In the utils module you can find the Interface for the Unpackers.

The Unpacker Objects are implemented in 2 steps.
While the implementation of the :meth:`get` method is found
in the implementation sub-package, the :mod:`~bgpack.unpack.file`
and :mod:`~bgpack.unpack.files` modules contain the
context manager methods:
- file: when the data is contained in a single file (whether it has offsets or not)
- files: when the data is formed by combining multiple files
"""
from bgpack.globals import BGPackError


class UnpackerError(BGPackError):
    pass


class IUnpacker:
    """
    Interface for readers of indexed files

    Args:
        name (str): name of the pack files
        metadata (dict): all the information saved in the pickle

    """

    def __init__(self):
        raise NotImplementedError

    def __enter__(self):
        raise NotImplementedError

    def __exit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError

    def get(self, start=None, stop=None):
        """
        Get values for positions between start and stop

        Args:
            start (int, optional): starting position for the query
            stop (int, optional): end position for the query

        Yield:
            tuple: position, value(s)

        The actual code depends on the implementation

        """
        raise NotImplementedError
