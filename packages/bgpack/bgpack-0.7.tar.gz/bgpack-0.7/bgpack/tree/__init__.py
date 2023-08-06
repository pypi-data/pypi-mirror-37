"""
The tree implementation works on top of the bgpack implementation.
Instead of filling missing values with the default value
those positions are skipped and the offset saved in a tree
of intervals.
"""
from .main import pack as write, get_parser, get_unpacker