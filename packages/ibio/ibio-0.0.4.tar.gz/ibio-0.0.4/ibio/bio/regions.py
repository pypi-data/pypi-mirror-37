"""
This will contain the class for regions
"""
import ibio


class Regions:
    """
    class Regions
    """

    def __init__(self, regions=None):

        if regions is None:
            self.regions = dict()

        self.set_regions(regions)

    def __str__(self):
        """
        Represent files
        """
        if self.regions == dict():
            return "Empty regions"

        return str(self.regions)

    def __repr__(self):
        """
        Represent files
        """
        if self.regions == dict():
            return "Empty regions"

        return str(self.regions.keys())

    def from_file(self, filepath):
        ibio.File.validate_path(filepath)
        regions = dict()

        with open(filepath, "r") as f:
            for line in f:
                line = line.strip("\n").split("\t")
                if line[0] not in regions.keys():
                    regions[line[0]] = []

                regions[line[0]].append([int(line[1]), int(line[2]), line[3]])

        self.set_regions(regions)
        return regions

    def set_regions(self, regions):
        self.regions = regions

    def load_gene_regions(self):
        refseq_exome_roi_path = "/DATA/biodata/exome/007_exome_RefSeq/dump_gene_regions_20180906.bed"
        self.from_file(refseq_exome_roi_path)

    def get_info_of_position(self, chrom, position):
        matches = []

        if chrom in self.regions.keys():
            for i in self.regions[chrom]:
                if i[0] < position < i[1]:
                    matches.append(i[2])

        return ','.join(sorted(matches))

    def save_regions(self, filepath):
        with open(filepath, 'w') as fh:
            for chrom in sorted(self.regions.keys()):
                for region in self.regions[chrom]:
                    fh.write('\t'.join([chrom, str(region[0]), str(region[1]), region[2]]) + '\n')

    def get_info_of_region(self, region):
        chrom = list(region.keys())[0]
        start = region[chrom][0]
        end = region[chrom][1]

        genes = []
        if chrom in self.regions.keys():
            for i in self.regions[chrom]:
                if start < i[0] < end or start < i[1] < end:
                    genes.append(i[2])

        return genes

    def is_position_in_regions(self, chrom, position):
        matches = []

        if chrom in self.regions.keys():
            for i in self.regions[chrom]:
                if i[0] < position < i[1]:
                    matches.append(i[2])
        if len(matches) > 0:
            return True
        else:
            return False

    @staticmethod
    def __process_path(filepath):
        """
        This will retrieve data from the file
        """
        in_file = open(filepath, 'r')
        regions = []
        for line in in_file:
            if line.startswith('#'):
                continue
            line = line.strip('\n').split('\t')
            regions.append(line)

        return regions
