import bitarray

from bgpack.unpack import IUnpacker, UnpackerError


class Unpacker(IUnpacker):

    def get(self, start=None, stop=None):
        """
        Get values for positions between start and stop

        Args:
            start (int, optional): starting position for the query
            stop (int, optional): end position for the query

        Yield:
            tuple: position, value1, value2...

        """
        start = start if start is not None else self.start  # start or self.start is not valid because it will not work with 0
        stop = stop if stop is not None else self.stop  # stop or self.stop is not valid because it will not work with 0
        if start < self.init or stop > self.end:
            raise UnpackerError('Range outside limits {}-{}'.format(self.init, self.end))
        elif stop < self.start or start > self.stop:  # only asking for default values
            i = start
            while i <= stop:
                yield (i,) + self.default_value
                i += 1
        else:
            # TODO further optimizaton of nbytes_group choice
            nbytes_group = 8 * self.nbits  # taking 8*nbits we ensure that within a group we have a number a fixed number of complete elements and no remaining
            nbits_max_group = 8 * nbytes_group

            byte_starting = (start - self.start) * self.nbits // 8
            byte_starting = byte_starting if byte_starting >= 0 else 0
            byte_starting_group = (byte_starting // nbytes_group) * nbytes_group  # starting group

            self.mm.seek(byte_starting_group + self.offset)

            bit_offset = (start - self.start) * self.nbits % 8 + (byte_starting - byte_starting_group) * 8

            bits = bitarray.bitarray(endian='big')
            bits.frombytes(self.mm.read(nbytes_group))

            i = start

            first_limit = stop if stop < self.start-1 else self.start-1
            second_limit = stop if stop <= self.stop else self.stop

            while i <= first_limit:
                yield (i,) + self.default_value
                i += 1

            while i <= second_limit:
                r = bits[bit_offset:bit_offset + self.nbits].to01()
                yield (i,) + self.index[r]
                i += 1
                bit_offset += self.nbits
                if bit_offset >= nbits_max_group:
                    bit_offset = 0
                    bits = bitarray.bitarray(endian='big')
                    bits.frombytes(self.mm.read(nbytes_group))

            while i <= stop:
                yield (i,) + self.default_value
                i += 1


class UnpackerSingleValue(IUnpacker):

    def get(self, start=None, stop=None):
        """
        Get values for positions between start and stop

        Args:
            start (int, optional): starting position for the query
            stop (int, optional): end position for the query

        Yield:
            tuple: position, value (or (v1, v2, ...))

        This is the right reader to return single values.
        This is the faster than unpacking multiple values when the reader comes from multi values
        """
        start = start if start is not None else self.start  # start or self.start is not valid because it will not work with 0
        stop = stop if stop is not None else self.stop  # stop or self.stop is not valid because it will not work with 0
        if start < self.init or stop > self.end:
            raise UnpackerError('Range outside limits {}-{}'.format(self.init, self.end))
        elif stop < self.start or start > self.stop:  # only asking for default values
            i = start
            while i <= stop:
                yield i, self.default_value
                i += 1
        else:
            # TODO further optimizaton of nbytes_group choice
            nbytes_group = 8 * self.nbits  #  taking 8*nbits we ensure that within a group we have a number a fixed number of complete elements and no remaining
            nbits_max_group = 8 * nbytes_group

            byte_starting = (start - self.start) * self.nbits // 8
            byte_starting = byte_starting if byte_starting >= 0 else 0
            byte_starting_group = (byte_starting // nbytes_group) * nbytes_group  # starting group

            self.mm.seek(byte_starting_group + self.offset)

            bit_offset = (start - self.start) * self.nbits % 8 + (byte_starting - byte_starting_group) * 8

            bits = bitarray.bitarray(endian='big')
            bits.frombytes(self.mm.read(nbytes_group))

            i = start

            first_limit = stop if stop < self.start - 1 else self.start - 1
            second_limit = stop if stop <= self.stop else self.stop

            while i <= first_limit:
                yield i, self.default_value
                i += 1

            while i <= second_limit:
                r = bits[bit_offset:bit_offset + self.nbits].to01()
                yield i, self.index[r]
                i += 1
                bit_offset += self.nbits
                if bit_offset >= nbits_max_group:
                    bit_offset = 0
                    bits = bitarray.bitarray(endian='big')
                    bits.frombytes(self.mm.read(nbytes_group))

            while i <= stop:
                yield i, self.default_value
                i += 1
