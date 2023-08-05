import unittest
import ibio


class TestVariants(unittest.TestCase):

    def test_retrieve_variant_gene_1(self):
        variant = ibio.Variant("1", "14365", "G", "A")
        gene = variant.get_gene_of_variant_in_exome()
        assert (gene == "DDX11L1,WASH7P"), f"Gene {gene} does not match with expected"

    def test_retrieve_variant_gene_2(self):
        variant = ibio.Position("1", "14365")
        gene = variant.get_gene_of_variant_in_exome()
        assert (gene == "DDX11L1,WASH7P"), f"Gene {gene} does not match with expected"

    def test_retrieve_position_gene(self):
        variant = ibio.Position("1", "14365")
        gene = variant.get_id_of_variant_in_roi("/DATA/biodata/exome/007_exome_RefSeq/imegen.roi.25pb.full.merged.sort.bed")
        assert (gene == "DDX11L1,WASH7P"), f"Gene {gene} does not match with expected"


def main():
    tests = TestVariants()
    tests.test_retrieve_variant_gene_1()


if __name__ == "__main__":
    main()
