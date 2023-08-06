import tempfile
from os import path

import pytest

from bgpack import BGPackError, write, get_unpacker


OPTIONS_MULTIFILE = [True, False]
OPTIONS_IMPLEMENTATION = ['read', 'size']


@pytest.mark.parametrize("multifile", OPTIONS_MULTIFILE)
@pytest.mark.parametrize("implementation", OPTIONS_IMPLEMENTATION)
def test1(multifile, implementation):
    # 2 parsers single value
    def parser():
        for i in range(15):
            yield i, i*3

    parsers = {'1': parser, '2': parser}

    with tempfile.TemporaryDirectory() as tmpdirname:
        name = path.join(tmpdirname, 'test1')
        write(name, parsers, allow_multifile=multifile, optimize_for=implementation)

        reader = get_unpacker(name)

        with reader as r:
            try:
                r.get()
            except TypeError:  # missing key argument
                assert True
            else:
                assert False

        with reader as r:
            for original, result in zip(parser(), r.get('1')):
                assert original == result

            for original, result in zip(parser(), r.get('2')):
                assert original == result

            for _, val in r.get('1', 1, 1):
                assert val == 3

            for _, val in r.get('1', 2, 2):
                assert val == 6

            for _, val in r.get('2', 3, 3):
                assert val == 9

            for _, val in r.get('2', 13, 13):
                assert val == 39

            for _, val in r.get('1', 14, 14):
                assert val == 42


@pytest.mark.parametrize("multifile", OPTIONS_MULTIFILE)
@pytest.mark.parametrize("implementation", OPTIONS_IMPLEMENTATION)
def test2(multifile, implementation):
    # 2 parsers two values
    def parser():
        for i in range(15):
            yield i, i, i*3

    parsers = {'1': parser, '2': parser}

    with tempfile.TemporaryDirectory() as tmpdirname:
        name = path.join(tmpdirname, 'test2')
        write(name, parsers, allow_multifile=multifile, optimize_for=implementation)

        reader = get_unpacker(name)

        with reader as r:
            for original, result in zip(parser(), r.get('1')):
                assert original == result

            for original, result in zip(parser(), r.get('2')):
                assert original == result

            for _, *val in r.get('1', 1, 1):
                assert val == [1, 3]

            for _, *val in r.get('1', 2, 2):
                assert val == [2, 6]

            for _, *val in r.get('2', 3, 3):
                assert val == [3, 9]

            for _, *val in r.get('2', 13, 13):
                assert val == [13, 39]

            for _, *val in r.get('1', 14, 14):
                assert val == [14, 42]


@pytest.mark.parametrize("multifile", OPTIONS_MULTIFILE)
@pytest.mark.parametrize("implementation", OPTIONS_IMPLEMENTATION)
def test3(multifile, implementation):
    # 2 parsers one value, changing limits
    def parser():
        for i in range(3, 6):
            yield i, i

    parsers = {'1': parser, '2': parser}

    with tempfile.TemporaryDirectory() as tmpdirname:
        name = path.join(tmpdirname, 'test3')
        write(name, parsers, init_pos={'1': 0, '2': 1}, end_pos={'1': 7, '2': 10}, allow_multifile=multifile, optimize_for=implementation)

        reader = get_unpacker(name)

        with reader as r:

            try:
                for _, val in r.get('2', 0, 2):
                    assert val is None
            except BGPackError:
                assert True
            else:
                assert False

            for _, val in r.get('1', 0, 2):
                assert val is None

            for _, val in r.get('2', 7, 10):
                assert val is None

            try:
                for _, val in r.get('1', 7, 10):
                    assert val is None
            except BGPackError:
                assert True
            else:
                assert False


@pytest.mark.parametrize("multifile", OPTIONS_MULTIFILE)
@pytest.mark.parametrize("implementation", OPTIONS_IMPLEMENTATION)
def test4(multifile, implementation):
    # 2 different parsers single value
    def parser1():
        for i in range(7):
            yield i, i*3
    def parser2():
        for i in range(15):
            yield i, i*2

    parsers = {'1': parser1, '2': parser2}

    with tempfile.TemporaryDirectory() as tmpdirname:
        name = path.join(tmpdirname, 'test4')
        write(name, parsers, allow_multifile=multifile, optimize_for=implementation)

        reader = get_unpacker(name)

        with reader as r:
            for original, result in zip(parser1(), r.get('1')):
                assert original == result

            for original, result in zip(parser2(), r.get('2')):
                assert original == result

            for _, val in r.get('1', 1, 1):
                assert val == 3

            for _, val in r.get('1', 2, 2):
                assert val == 6

            for _, val in r.get('1', 3, 3):
                assert val == 9

            for _, val in r.get('1', 5, 5):
                assert val == 15

            for _, val in r.get('1', 6, 6):
                assert val == 18

            for _, val in r.get('2', 1, 1):
                assert val == 2

            for _, val in r.get('2', 2, 2):
                assert val == 4

            for _, val in r.get('2', 3, 3):
                assert val == 6

            for _, val in r.get('2', 13, 13):
                assert val == 26

            for _, val in r.get('2', 14, 14):
                assert val == 28


def all_(multifile, implementation):
    test1(multifile, implementation)
    test2(multifile, implementation)
    test3(multifile, implementation)
    test4(multifile, implementation)


if __name__ == '__main__':
    for v in zip(OPTIONS_MULTIFILE, OPTIONS_IMPLEMENTATION):
        all_(*v)
