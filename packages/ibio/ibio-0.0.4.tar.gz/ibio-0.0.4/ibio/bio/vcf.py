from .file_class import File
import ibio


class Position:
    """Class that evaluates a position"""
    def __init__(self, chrom, position):

        # Check that chromosome and position are correct
        self.chrom, self.position = self.check_variant_values(chrom, position)

    def __str__(self):
        return self.__class__.__name__ + ' -> ' + self.chrom + ':' + str(self.position)

    def __repr__(self):
        return self.chrom + ':' + str(self.position)

    @staticmethod
    def check_variant_values(chrom, position):
        """Method that checks that chromosome is on the range 1-22,X,Y, if not raises an exception

        Input
        -----
        - chrom(str): Chromosome of the position
        - position(int): Position to evaluate

        Output
        ------
        - chrom(str): Chromosome of the position
        - position(int): Position to evaluate

        """
        chrom_values = [str(c) for c in range(1, 23)] + ['X', 'Y']

        try:
            assert chrom.upper() in chrom_values, f"#[ERR] -> Chromosome should be in {','.join(chrom_values)}"

        except AssertionError as error:
            print(error)
            exit(0)

        except Exception as error:
            print("Exception error")
            exit(0)

        position = int(position)
        return chrom, position

    def get_gene_of_variant_in_exome(self):
        exome_regions = ibio.Regions()
        exome_regions.load_gene_regions()
        return exome_regions.get_info_of_position(self.chrom, self.position)

    def get_id_of_variant_in_roi(self, regions_filepath):
        exome_regions = ibio.Regions()
        exome_regions.from_file(regions_filepath)
        return exome_regions.get_info_of_position(self.chrom, self.position)

    def get_annot_of_variant_in_roi(self, regions):
        exome_regions = ibio.Regions(regions)
        return exome_regions.get_info_of_position(self.chrom, self.position)


class Variant(Position):
    """Class that evaluates a variant"""
    def __init__(self, chrom, position, reference_allele="", alternative_allele=""):
        super().__init__(chrom, position)
        self.reference_allele, self.alternative_allele = reference_allele, alternative_allele

    def __str__(self):
        return self.__class__.__name__ + ' -> ' + self.chrom + ':' + str(self.position)

    def __repr__(self):
        return self.chrom + ':' + str(self.position)


class Vcf(File):
    """Class that evaluates a vcf"""
    def __init__(self):
        pass
