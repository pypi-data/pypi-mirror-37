from contextlib import ExitStack

from bgpack.unpack import IUnpacker


class Unpacker(ExitStack, IUnpacker):

    def __init__(self, tree, unpacker):
        super().__init__()
        self.tree = tree
        self.unpacker = unpacker
        self.pck = None

    def __enter__(self):
        super().__enter__()
        self.pck = self.enter_context(self.unpacker)
        return self

    def get(self, start=None, stop=None):

        if start is None:
            start = self.tree.begin()
        if stop is None:
            stop = self.tree.stop()

        start = max(start, self.tree.begin())
        end = min(stop, self.tree.end())

        for interval in sorted(self.tree.search(start, end)):
            interval_start, interval_stop, interval_offset = interval.begin, interval.end, interval.data
            b = max(start, interval_start)
            e = min(interval_stop-1, end)
            for pos, *v in self.unpacker.get(b-interval_offset, e-interval_offset):
                yield (pos + interval_offset,) + tuple(v)


class UnpackerKeyed(Unpacker):

    def get(self, key, start=None, stop=None):

        tree = self.tree[key]

        if start is None:
            start = tree.begin()
        if stop is None:
            stop = tree.end()

        start = max(start, tree.begin())
        end = min(stop, tree.end())

        for interval in sorted(tree.search(start, end)):
            interval_start, interval_stop, interval_offset = interval.begin, interval.end, interval.data
            b = max(start, interval_start)
            e = min(interval_stop-1, end)
            for pos, *v in self.unpacker.get(key, b-interval_offset, e-interval_offset):
                yield (pos + interval_offset,) + tuple(v)
