import unittest
from ibio.dbs.ucsc_db import UCSC


class ucsc_db(unittest.TestCase):

    ucsc = UCSC()

    def test_ucsc_db_version(self):
        self.assertEqual(self.ucsc.db, 'hg19')

    # def test_ucsc_sequence(self):
    #
    #     rs = 'rs1815739'
    #     data = self.ucsc.queryRs(rs, 'snp150')
    #
    #     # Define header
    #     header = ['bin', 'chrom', 'chromStart', 'chromEnd', 'name', 'score', 'strand', 'refNCBI',
    #               'refUCSC', 'observed', 'molType', 'class', 'valid', 'avHet', 'avHetSE', 'func',
    #               'locType', 'weight', 'exceptions', 'submitterCount', 'submitters', 'alleleFreqCount',
    #               'alleles', 'alleleNs', 'alleleFreqs', 'bitfields']
    #
    #     # Assert that header has not change
    #     self.assertEqual(header, data['header'])
    #
    #     # Assert that the recovered RS matches the queried
    #     self.assertEqual(data['data'][0][4], rs)
    #
    #     self.ucsc.close_conn()

    # def test_ucsc_nm_regions(self):
    #
    #     nm_list = ['NM_005450']
    #     regions = self.ucsc.queryStructureByNm(nm_list, True)
    #
    #     self.assertEqual(regions, [['17', '54671584', '54672283', 'NOG', 'NM_005450']])
