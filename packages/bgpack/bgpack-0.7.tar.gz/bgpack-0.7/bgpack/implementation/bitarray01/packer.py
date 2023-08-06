"""
These packers receive an integer from the mapper
and convert it into a binary data with a predefined
number of bits.
As they work at bit level, they should only return information
when a byte or set of bytes are completed
"""

import math

from bgpack.pack import IPacker


class Packer(IPacker):

    def __init__(self, map_):
        """
        Convert an integer value into a set of bits

        Args:
            map_ (MapWriter): map writer object

        """
        self.data = 0
        self.nbits = 0  # bits used
        self.nbits4value = map_.nbits

    def add_and_get(self, value):
        """

        Args:
            value (int): integer

        Returns:
            bytearray: return bytes if they are full, else None

        """
        self.nbits += self.nbits4value
        self.data = self.data << self.nbits4value
        self.data += value
        return self._save_get()

    def _save_get(self):
        """
        Return the byte array with the bytes
        that are full

        Returns:
            bytearray or None: bytearray with the bytes that are full. None if
              no bytes are full

        """
        if self.nbits % 8 == 0:
            nbytes = self.nbits // 8
            return self._get(nbytes)
        else:
            return None

    def _get(self, nbytes=None):
        """
        Get the stored value as an array of bytes

        Args:
            nbytes (int, optional): number of bytes to return. If the
               value does not fit, the rest is kept as the value

        Returns:
            bytearray: value as an array of bytes

        """
        nbytes_required = math.ceil(self.nbits / 8)
        nbytes = nbytes or nbytes_required
        if nbytes >= nbytes_required:
            value = self.data.to_bytes(nbytes, byteorder='big', signed=False)
            self.data = 0
            self.nbits = 0
        else:
            bytes_ = self.data.to_bytes(nbytes_required, byteorder='big', signed=False)
            self.nbits -= nbytes * 8
            self.data = int.from_bytes(bytes_[nbytes:], byteorder='big', signed=False)
            value = bytes_[:nbytes]
        return value

    def get_rest(self):
        """

        Returns:
            bytearray: fill the missing values to complete the last byte with 0
               and return a byte array

        """
        if self.nbits == 0:
            return None
        else:
            nbytes_required = math.ceil(self.nbits / 8)
            nbits_required = nbytes_required * 8
            nbits_empty = nbits_required - self.nbits
            v = self.data << nbits_empty
            self.data = 0
            self.nbits = 0
            return v.to_bytes(nbytes_required, byteorder='big', signed=False)

    def add(self, value):
        """Generic add method to add a value"""
        self.nbits += self.nbits4value
        self.data = self.data << self.nbits4value
        self.data += value
