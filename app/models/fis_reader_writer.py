"""Utilities for reading from and writing to FIS inference system files."""

import os.path

from .fis_model import FISModel
from .modelsresources.readfis_ext import readfis

SUPPORTED_EXTENSIONS: list[str] = [".fis"]
"""File extensions supported by the reader/writer."""


class FISReaderWriter:
    """Reader and writer for `.fis` files backed by an `FISModel`."""

    model: FISModel
    """Model containing the fis system."""

    def __init__(self, model: FISModel = None):
        """Initialise the reader/writer with an optional model instance.

        Parameters
        ----------
        model : FISModel, optional
            Model instance to associate with the reader. May be `None` when the
            instance is only used for reading.
        """
        self.model = model

    def read_fis(self, path: str) -> int:
        """Read the FIS model at `path` into the `model` attribute.

        Parameters
        ----------
        path : str
            Path to the `.fis` file, including the filename.

        Returns
        -------
        int
            1 when the file is read successfully.
            -1 when the selected file has an unsupported extension.
            -2 when the file does not exist.
            -3 when reading the file fails.
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
