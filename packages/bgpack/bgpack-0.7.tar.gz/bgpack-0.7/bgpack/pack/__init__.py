"""
The packer package contains the utilities to create the
packed file and the corresponding metadata information file
"""


class IPacker:
    """Interface for packer objects.
    Packer objects receive a MapWriter on creation to get any information they may need from them
    in advance (for e.g. the number of bits).
    Then the packer should have a method to receive a value from the mapper and return
    (when available) new data to be saved to the file
    """

    def __init__(self, map_):
        raise NotImplementedError

    def add_and_get(self, value):
        """
        Add a value and return a byte array to store, if available
        The availability conditions might differ
        """
        raise NotImplementedError

    def get_rest(self):
        """
        Return remaining data as a byte array to save it
        """
        raise NotImplemented

    def add(self, value):
        """Add a value"""
