"""
This package contains the different implementations for this package

Each implementation consist of some utilities (functions...) in utils modules
and the implementation of the different classes for mapper, packer and reader.

- mapper contains implementations of mappers, map writers and map readers.
  See :mod:`~bgpack.mapper` for further details

- packer contains classes needed to get the data from the parser, pass them to
  the map and return the binary data to save.
  Find more details in :mod:`~bgpack.packer`

- reader contains classes to read the data from the file
  (using a memory map). More details in :mod:`~bgpack.reader`
"""