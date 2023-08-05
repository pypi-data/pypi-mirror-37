import sys
import subprocess
from .file_class import File


class Bed(File):
    """BED file"""

    def __init__(self, filepath):
        self.filepath = filepath

        self.validate_path()

    def sort(self):

        cmd = "grep '^#' " + self.filepath + "; "\
              "grep -v '#' " + self.filepath + "| sort -k1,1V -k2,2n -k3,3n"

        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        while True:
            nextline = process.stdout.readline().decode().strip('\n')
            if nextline == '':
                break

            print(nextline)
