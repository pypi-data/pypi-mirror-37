"""
These packers receive a byte array from the mapper
and return that information when there is a reasonable amount
of data to write to the file.
This way we speak to save some time as the file is not opened
on every call.
"""

from bgpack.pack import IPacker


class Packer(IPacker):

    def __init__(self, map_, min_size=10**3):
        """
        Group arrays of bytes and return them when they have certain size
        """
        self.size = min_size
        self.data = b''

    def add_and_get(self, value):
        """

        Args:
            value (bytearray):

        Returns:
            bytearray: return bytes if they are full, else None

        """
        self.data += value
        return self._save_get()

    def _save_get(self):
        """
        Return the byte array it size ex

        Returns:
            bytearray or None: bytearray with the bytes that are full. None if
              no bytes are full

        """
        if len(self.data) > self.size:
            return self._get()
        else:
            return None

    def _get(self):
        """
        Get the stored value
        """
        value = self.data
        self.data = b''
        return value

    def get_rest(self):
        """"""
        return self._get()

    def add(self, value):
        """Generic add method to add a value"""
        self.data += value
