import pysam
import ibio


class Bam:
    """BED file"""

    def __init__(self, filepath):

        self.filepath = ibio.File.validate_path(filepath=filepath)
        print("Bam validated")

    def __repr__(self):
        return self.filepath

    def __str__(self):
        return self.filepath

    def coverage_at_position(self):
        samfile = pysam.AlignmentFile(self.filepath, 'rb')
        data = samfile.pileup("1", 100, 120)
        print(data)
        samfile.close()
