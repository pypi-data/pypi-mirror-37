"""
Bitarray01 is an efficient implementation to save disk size
because it compresses to bit level.

Each value is mapped to an integer
that is stored as bits with the minimum bits possible.
Then the reader reads those bits as a 01 string
and from that string the original values are returned.
"""