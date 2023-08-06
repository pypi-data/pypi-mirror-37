import tabix

from bgpack.parse import ParserError


class Tabix:

    def __init__(self, file):
        self.file = file
        self.tb = None

    def __enter__(self):
        self.tb = tabix.open(self.file)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return True

    def get(self, chromosome, start, stop):
        try:
            for row in self.tb.query("{}".format(chromosome), start - 1, stop):
                yield row
        except tabix.TabixError:
            raise ParserError('Tabix error in {}: {}-{}'.format(chromosome, start, stop))
