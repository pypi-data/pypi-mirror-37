import xmltodict
import requests


class Sequence:
    """Sequence class"""
    def __init__(self, seq=""):
        self.sequence = seq

    def __str__(self):
        return self.sequence

    def set_sequence(self, sequence):
        """Set the sequence to a given string"""
        self.sequence = sequence

    def get_ucsc_sequence(self, chrom, start, end, version='hg19'):
        """Fetch from UCSC the sequence of a given region"""

        url = f'http://genome.ucsc.edu/cgi-bin/das/{version}/dna?segment=chr{chrom}:{start},{end}'

        r = requests.get(url)
        doc = xmltodict.parse(r.text)

        self.set_sequence(doc['DASDNA']['SEQUENCE']['DNA']['#text'].upper().replace('\n', ''))

        return self.sequence

    def modify_sequence(self, rev=False, compl=False):
        """Method to get reverse or complementary chain of the sequence"""
        result_sequence = ""

        if compl is True:
            for i in self.sequence:
                if i == 'A':
                    result_sequence += "T"
                if i == 'T':
                    result_sequence += "A"
                if i == 'G':
                    result_sequence += "C"
                if i == 'C':
                    result_sequence += "G"

        if rev is True and compl is True:
            result_sequence = result_sequence[::-1]
        elif rev is True:
            result_sequence = self.sequence[::-1]

        return result_sequence
