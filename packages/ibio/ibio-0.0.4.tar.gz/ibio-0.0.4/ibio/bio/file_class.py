import os


class File:
    @staticmethod
    def validate_path(filepath):
        """Check if file given by user exists
        """
        if not os.path.exists(filepath):
            raise IOError(f"File {filepath} does not exists")

        return filepath
