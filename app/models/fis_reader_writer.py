"""Read/write from/to a fis inference system file, based on the system provided
with a FISModel class instance.

Classes:

    FISReaderWriter: reader/writer of fis files
"""
import os.path

from .fis_model import FISModel
from .modelsresources.writefis_ext import writeFIS

SUPPORTED_EXTENSIONS: list[str] = [".fis"]
"""File extensions supported by the reader/writer."""


class FISReaderWriter:
    """A class allowing reading/writing of a fis file, to/from a FISModel class
    instance.

    Attributes:

        model (FisModel): model containing the fis system

    Methods:

        __init__(FISModel):
            Initialize a new class instance.
        write_fis(str) -> int:
            Write the fis model to the fis file provided.
    """

    model: FISModel
    """Model containing the fis system."""

    def __init__(self, model: FISModel = None):
        """Initialize a new class instance.

        Parameters:

            model (FISModel): the model to be used, can be None (for reading)
        """
        self.model = model

    def write_fis(self, path: str) -> int:
        """Write the fis model to the fis file provided. If it exists, it will
        be overwritten.

        Parameters:

            path (str): path to save the fis file on, with name appended

        Returns:

            1 - file written successfully

            -1 - chosen file has an unsupported extension

            -2 - no FISModel instance provided

            -3 - problems with writing file, operation aborted
        """
        if not self._check_if_extension_is_supported(path):
            return -1

        if self.model is None:
            return -2

        writeFIS(self.model._fis, path)
        if not os.path.isfile(path):
            return -3

        return 1

    def _check_if_extension_is_supported(self, path: str) -> bool:
        is_supported = False
        for extension in SUPPORTED_EXTENSIONS:
            if path.endswith(extension) is True:
                is_supported = True

        return is_supported
