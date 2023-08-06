import gzip
import logging
import os
import pickle
import shutil
import tempfile
import uuid
from os import path

from bgpack.globals import BGPackError
from bgpack.parse import utils as parse_utils, AbstractParserGrouped
from bgpack.utils import required_bits, required_bytes, combine_groups


class GroupSet:

    def __init__(self, n, file):
        self.sets = [set() for _ in range(n)]
        self.file = file

    def add(self, *args):
        for i, arg in enumerate(args):
            self.sets[i].add(arg)

    def __len__(self):
        return sum([len(s) for s in self.sets])

    def save(self):
        with gzip.open(self.file, 'wb') as fd:
            pickle.dump(self.sets, fd)
        n = len(self.sets)
        self.sets = [set() for _ in range(n)]

    def update(self):
        if path.exists(self.file):
            with gzip.open(self.file, 'rb') as fd:
                loaded_sets = pickle.load(fd)

            for this_set, loaded_set in zip(self.sets, loaded_sets):
                this_set.update(loaded_set)

    def empty(self):
        os.remove(self.file)
        self.file = None
        self.sets = []
        self.save = lambda *args: None
        self.update = lambda *args: None


def optimize(parser, max_size=10**8, max_distinct=5*10**7):
    """Optimize a parser"""
    logger = logging.getLogger(__name__)
    length = parse_utils.data_size(parser)

    logger.info('Data has size %d', length)

    tmp = tempfile.mkdtemp()

    groups = []
    for g in combine_groups(list(range(length)), []):
        grouped, ungrouped = g
        size = len(grouped) + len(ungrouped)
        groups.append((g, GroupSet(size, path.join(tmp, str(uuid.uuid4()) + '.pkl.gz'))))

    if not isinstance(parser, (AbstractParserGrouped, dict)):
        parser = {'_': parser}

    rows = 0

    for _, p in parser.items():
        for _, *v in p():
            rows += 1
            for group, set_ in groups:
                grouped, ungrouped = group
                l = []
                for index in ungrouped:
                    l.append(v[index])
                for subgroup in grouped:
                    sub_l = []
                    for index in subgroup:
                        sub_l.append(v[index])
                    l.append(tuple(sub_l))
                set_.add(*tuple(l))

                if rows % 10**6 == 0:  # check if any of the original columns has so much variability that the index will be huge
                    set_.update()
                    if len(grouped) == 0:  # all ungrouped
                        if any([len(s) > max_distinct for s in set_.sets]):
                            for i, l in enumerate(map(len, set_.sets)):
                                logger.info('%d values in column %d', l, i)
                            logger.error('Due to high variability in the data, your index cannot be optimized')
                            shutil.rmtree(tmp)
                            raise BGPackError('Optimization not possible')
                    else:
                        if len(set_) > max_size:  # if any set is getting too big, discard it
                            logger.debug('Discarding set for %s', group)
                            set_.empty()

            if rows % 10 ** 6 == 0:
                logger.debug('%d million rows read', rows//(10**6))

    default = None
    bitarray01 = None
    bytearray_ = None
    for index, (group, set_) in enumerate(groups):
        if set_.file is None:  # empty set
            continue
        grouped, ungrouped = group
        set_.update()
        nbits = sum([required_bits(len(x)) for x in set_.sets])
        nbytes = sum([required_bytes(len(x)) for x in set_.sets])
        if len(grouped) == 0:  # all separated
            default = (index, nbits, nbytes)
        if bitarray01 is None or nbits < bitarray01[1]:
            bitarray01 = (index, nbits)
        if bytearray_ is None or nbytes < bytearray_[1]:
            bytearray_ = (index, nbytes)
        set_.save()

    indexes_to_keep = []
    if default is None and bitarray01 is None and bytearray_ is None:
        raise BGPackError('All set exceded the limits')
    if default is None:
        logger.info('Default index not found')
        logger.info('The bitarray01 implementation requires %d bits.', bitarray01[1])
        logger.info('The bytearray implementation requires %d bytes.', bytearray_[1])
    else:
        logger.info('Your default parser requieres %d bits and %d bytes.', default[1], default[2])
        indexes_to_keep.append(default[0])
        if bitarray01[1] >= default[1]:
            logger.info('No optimizations found for bitarray implementation.')
            bitarray01 = None
        else:
            logger.info('Using the bitarray01 you reduce the number of bits to %d.', bitarray01[1])
            indexes_to_keep.append(bitarray01[0])
        if bytearray_[1] >= default[2]:
            logger.info('No optimizations found for bytearray implementation.')
            bytearray_ = None
        else:
            logger.info('Using the bytearray you reduce the number of bytes to %d.', bytearray_[1])
            indexes_to_keep.append(bytearray_[0])

    for i, (g, s) in enumerate(groups):
        if i not in indexes_to_keep:
            s.empty()

    default = None if default is None else groups[default[0]]
    bitarray01 = None if bitarray01 is None else groups[bitarray01[0]]
    bytearray_ = None if bytearray_ is None else groups[bytearray_[0]]

    return rows, tmp, default, bitarray01, bytearray_


def print_optimization(optimization_result):
    rows, tmp, default, bitarray01, bytearray_ = optimization_result

    print('{} rows read'.format(rows))
    print('Result in directory {}'.format(tmp))

    if default is not None:
        group, set_ = default
        set_.update()
        nbits = sum([required_bits(len(x)) for x in set_.sets])
        nbytes = sum([required_bytes(len(x)) for x in set_.sets])
        print(
            'Your parser will require {} bits when using the bitarray01 implementation and {} bits when using the bytearray implementation'.format(
                nbits, nbytes * 8))
        for i, s in enumerate(set_.sets):
            print('Column {} has {} distinct values'.format(i, len(s)))

    if bitarray01 is not None:
        group, set_ = bitarray01
        set_.update()
        nbits = sum([required_bits(len(x)) for x in set_.sets])
        print('The bitarray01 implementation will require {} bits if you group the following columns'.format(nbits), end='')
        grouped, ungrouped = group
        for g in grouped:
            print('{}'.format(g), end=', ')
        print('')  # for the end of line

    if bytearray_ is not None:
        group, set_ = bytearray_
        set_.update()
        nbits = sum([required_bytes(len(x)) for x in set_.sets]) * 8
        print('The bytearray implementation will require {} bits if you group the following columns'.format(nbits), end='')
        grouped, ungrouped = group
        for g in grouped:
            print('{}'.format(g), end=', ')
        print('')  # for the end of line

    shutil.rmtree(tmp)
