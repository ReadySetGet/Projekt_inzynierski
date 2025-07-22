"""Read/write from/to a fis inference system file, based on the system provided
with a FISModel class instance.

Classes:

    FISReaderWriter: reader/writer of fis files
"""
import os.path

from .fis_model import FISModel
from .modelsresources.readfis_ext import readfis

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
        read_fis(str) -> int:
            Read the fis model from the fis file provided.
    """

    model: FISModel
    """Model containing the fis system."""

    def __init__(self, model: FISModel = None):
        """Initialize a new class instance.

        Parameters:

            model (FISModel): the model to be used, can be None (for reading)
        """
        self.model = model

    def read_fis(self, path: str) -> int:
        """Read the fis model from the fis file provided, and save it in the
            "model" attribute.

        Parameters:

            path (str): path to the fis file, with name appended

        Returns:

            1 - file read successfully

            -1 - chosen file has an unsupported extension

            -2 - file on the given path does not exist

            -3 - problems with reading file, operation aborted


        """
        if not self._check_if_extension_is_supported(path):
            return -1

        if not os.path.isfile(path):
            return -2

        try:
            new_fis = readfis(path)
        except ValueError:
            return -3

        self.model = FISModel(fis=new_fis)
        return 1

    def _check_if_extension_is_supported(self, path: str) -> bool:
        is_supported = False
        for extension in SUPPORTED_EXTENSIONS:
            if path.endswith(extension) is True:
                is_supported = True

        return is_supported
