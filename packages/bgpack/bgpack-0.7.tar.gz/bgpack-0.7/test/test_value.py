
import tempfile
from os import path

import pytest

from bgpack import write, get_unpacker


OPTIONS = ['size', 'read']


@pytest.mark.parametrize("implementation", OPTIONS)
def test1(implementation):
    # 4 bits
    def parser():
        # pos 0-14, values pos*3
        for i in range(15):
            yield i, i * 3
    with tempfile.TemporaryDirectory() as tmpdirname:
        name = path.join(tmpdirname, 'test1')
        write(name, parser, optimize_for=implementation)

        reader = get_unpacker(name)

        with reader as r:
            for original, result in zip(parser(), r.get()):
                assert original == result

            for _, val in r.get(1, 1):
                assert val == 3

            for _, val in r.get(2, 2):
                assert val == 6

            for _, val in r.get(3, 3):
                assert val == 9

            for _, val in r.get(13, 13):
                assert val == 39

            for _, val in r.get(14, 14):
                assert val == 42


@pytest.mark.parametrize("implementation", OPTIONS)
def test2(implementation):
    # adding limits
    def parser():
        # pos 5-19, values (pos-5)*3
        for i in range(15):
            yield i + 5, i * 3
    with tempfile.TemporaryDirectory() as tmpdirname:
        name = path.join(tmpdirname, 'test2')
        write(name, parser, init_pos=3, end_pos=21, optimize_for=implementation)

        reader = get_unpacker(name)

        with reader as r:
            for i, t in enumerate(r.get(3, 4)):
                assert t == (3+i, None)
            for original, result in zip(parser(), r.get()):
                assert original == result
            for i, t in enumerate(r.get(20, 21)):
                assert t == (20 + i, None)


@pytest.mark.parametrize("implementation", OPTIONS)
def test3(implementation):
    # changing default value
    def parser():
        # 4 bits to encode values
        # pos 0-4 10-14 20-24, values = pos
        for i in range(5):
            yield i, i
        for i in range(10, 15):
            yield i, i
        for i in range(20, 25):
            yield i, i
    with tempfile.TemporaryDirectory() as tmpdirname:
        name = path.join(tmpdirname, 'test3')
        write(name, parser, default_value=137, optimize_for=implementation)

        reader = get_unpacker(name)

        with reader as r:
            for index, value in r.get(0, 24):
                if index in list(range(5)) + list(range(10, 15)) + list(range(20,25)):
                    assert value == index
                else:
                    assert value == 137


@pytest.mark.parametrize("implementation", OPTIONS)
def test4(implementation):
    # 3 bits
    def parser():
        # pos 0-14, values pos*3
        for i in range(8):
            yield i, i + 6
    with tempfile.TemporaryDirectory() as tmpdirname:
        name = path.join(tmpdirname, 'test4')
        write(name, parser, optimize_for=implementation)

        reader = get_unpacker(name)

        with reader as r:
            for original, result in zip(parser(), r.get()):
                assert original == result

            for _, val in r.get(1, 1):
                assert val == 7

            for _, val in r.get(2, 2):
                assert val == 8

            for _, val in r.get(3, 3):
                assert val == 9

            for _, val in r.get(6, 6):
                assert val == 12

            for _, val in r.get(7, 7):
                assert val == 13


@pytest.mark.parametrize("implementation", OPTIONS)
def test5(implementation):
    # 9 bits
    def parser():
        # pos 0-510, values pos*3
        for i in range(511):
            yield i, i
    with tempfile.TemporaryDirectory() as tmpdirname:
        name = path.join(tmpdirname, 'test5')
        write(name, parser, optimize_for=implementation)

        reader = get_unpacker(name)

        with reader as r:
            for original, result in zip(parser(), r.get()):
                assert original == result

            for _, val in r.get(1, 1):
                assert val == 1

            for _, val in r.get(2, 2):
                assert val == 2

            for _, val in r.get(3, 3):
                assert val == 3

            for _, val in r.get(509, 509):
                assert val == 509

            for _, val in r.get(510, 510):
                assert val == 510


@pytest.mark.parametrize("implementation", OPTIONS)
def test6(implementation):
    # 4 bits
    def parser():
        # pos -11-4, values pos*3
        for i in range(-11, 4, 1):
            yield i, i * 3
    with tempfile.TemporaryDirectory() as tmpdirname:
        name = path.join(tmpdirname, 'test6')
        write(name, parser, optimize_for=implementation)

        reader = get_unpacker(name)

        with reader as r:
            for original, result in zip(parser(), r.get()):
                assert original == result

            for _, val in r.get(1, 1):
                assert val == 3

            for _, val in r.get(2, 2):
                assert val == 6

            for _, val in r.get(0, 0):
                assert val == 0

            for _, val in r.get(-1, -1):
                assert val == -3

            for _, val in r.get(-2, -2):
                assert val == -6

            for _, val in r.get(-10, -10):
                assert val == -30

            for _, val in r.get(-11, -11):
                assert val == -33


@pytest.mark.parametrize("implementation", OPTIONS)
def test7(implementation):
    # Tuple, 4 bits
    def parser():
        # pos -11-4, values pos*3
        for i in range(-11, 4, 1):
            yield i, (i * 3, i*4)
    with tempfile.TemporaryDirectory() as tmpdirname:
        name = path.join(tmpdirname, 'test7')
        write(name, parser, optimize_for=implementation)

        reader = get_unpacker(name)

        with reader as r:
            for original, result in zip(parser(), r.get()):
                assert original == result

            for _, val in r.get(1, 1):
                assert val == (3, 4)

            for _, val in r.get(2, 2):
                assert val == (2*3, 2*4)

            for _, val in r.get(0, 0):
                assert val == (0, 0)

            for _, val in r.get(-1, -1):
                assert val == (-3, -4)

            for _, val in r.get(-2, -2):
                assert val == (-6, -8)

            for _, val in r.get(-10, -10):
                assert val == (-30, -40)

            for _, val in r.get(-11, -11):
                assert val == (-33, -44)


def all_(implementation):
    test1(implementation)
    test2(implementation)
    test3(implementation)
    test4(implementation)
    test5(implementation)
    test6(implementation)
    test7(implementation)


if __name__ == '__main__':
    for v in OPTIONS:
        all_(v)
