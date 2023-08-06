"""Testing Int2Bits conversion.
It correspond to the same working principle of the bitarray01 packer implementation"""

import math


class NumberBits:
    def __init__(self):
        self.v = 0
        self.bits_used = 0

    def add(self, value, nbits):
        self.bits_used += nbits
        self.v = self.v << nbits
        self.v += value

    def extract(self, nbytes=None):
        nbytes_required = math.ceil(self.bits_used / 8)
        nbytes = nbytes or nbytes_required
        if nbytes >= nbytes_required:
            value = self.v.to_bytes(nbytes, byteorder='big', signed=False)
            self.v = 0
            self.bits_used = 0
        else:
            bytes_ = self.v.to_bytes(nbytes_required, byteorder='big', signed=False)
            self.bits_used -= nbytes * 8
            self.v = int.from_bytes(bytes_[nbytes:], byteorder='big', signed=False)
            value = bytes_[:nbytes]
        return value

    def save_extract(self):
        if self.bits_used % 8 == 0:
            nbytes = self.bits_used // 8
            return self.extract(nbytes)
        else:
            return None


def test_NumberBits():
    n = NumberBits()
    for i in range(1, 4):
        n.add(i, 4)
    assert n.bits_used == 4*3
    assert b'\x01\x23' == n.extract()
    assert n.bits_used == 0
    assert n.v == 0

    n = NumberBits()
    for i in range(1, 4):
        n.add(i, 4)
    assert b'\x01' == n.extract(1)
    assert int.from_bytes(b'\x23', 'big', signed=False) == n.v


class NumberFixed:

    def __init__(self, bits):
        self.bits_free = bits
        self.v = 0

    def add(self, value, nbits):
        if self.bits_free >= nbits:
            self.v = self.v << nbits
            self.v += value
            self.bits_free -= nbits
            return None
        else:
            self.v = self.v << self.bits_free
            keep = value >> self.bits_free
            self.v += keep
            remain = value - (keep << self.bits_free)
            bits_remaining = nbits - self.bits_free
            self.bits_free = 0
            return remain, bits_remaining


def test_NumberFixed():
    n = NumberFixed(16)
    for i in range(1, 5):
        assert None is n.add(i, 4)
    assert 1, 1 == n.add(1, 1)


if __name__ == '__main__':
    test_NumberBits()
    test_NumberFixed()
