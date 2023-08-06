import csv
import gzip
import logging

from bgpack.parse import AbstractParserGrouped, ParserError


class CADD(AbstractParserGrouped):

    SCORE_ALT = {'T': 'ACG', 'A': 'CGT', 'C': 'AGT', 'G': 'ACT'}

    @staticmethod
    def parse(line):
        pos = int(line['Pos'])
        chrom = line.get('Chrom', line['#Chrom'])
        ref = line['Ref']
        alt = line['Alt']
        score = float(line['PHRED'])
        return chrom, pos, ref, alt, score

    @staticmethod
    def read(reader, check=False):
        v1 = CADD.parse(next(reader))
        # Skip M and R labeled nucleotides
        while v1[2] in ['M', 'R']:
            v1 = CADD.parse(next(reader))
        v2 = CADD.parse(next(reader))
        v3 = CADD.parse(next(reader))

        if check and not (v1[0] == v2[0] == v3[0] and v1[1] == v2[1] == v3[1] and v1[2] == v2[2] == v3[2]):
            raise ParserError('These lines are not consistent {}, {}, {}'.format(v1, v2, v3))
        position = v1[1]
        chromosome = v1[0]
        ref = v1[2]

        alts = CADD.SCORE_ALT[ref]
        scores = [None] * 3
        for i, a in enumerate(alts):
            for v in [v1, v2, v3]:
                if v[3] == a:
                    scores[i] = v[4]
                    break

        return chromosome, (position, ref) + tuple(scores)

    def __init__(self, file):

        logging.getLogger(__name__).debug('Reading CADD scores from %s' % file)

        self.file = file

    def get_parsers(self):
        """

        Yield:
            tuple: key and the associated parser for that key

        """
        current_key = None
        first_val = None

        keep_going = True

        with gzip.open(self.file, 'rt') as fd:
            fd.readline()
            reader = iter(csv.DictReader(fd, delimiter='\t'))

            while keep_going:

                # Read first key and first value skipping comments
                if current_key is None:
                    current_key, first_val = CADD.read(reader)

                # Create a parser
                def parser(check=True):
                    nonlocal current_key, first_val, keep_going

                    yield first_val

                    while True:
                        try:
                            this_key, data = CADD.read(reader, check)
                        except StopIteration:
                            keep_going = False
                            break
                        except KeyError:
                            logging.debug('Skipping {}-{}'.format(this_key, data))
                            continue  # skip lines with unkown ref
                        if this_key != current_key:
                            current_key = this_key
                            first_val = data
                            break
                        else:
                            yield data

                logging.getLogger(__name__).debug('Parser for key: %s' % current_key)

                yield current_key, parser
