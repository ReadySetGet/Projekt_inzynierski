"""Utilities for reading from and writing to FIS inference system files."""

import os.path

from .fis_model import FISModel
from .modelsresources.readfis_ext import readfis
from .modelsresources.writefis_ext import writeFIS

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
        except (ValueError, AssertionError, IndexError, KeyError) as e:
            import traceback

            print(f"Error reading FIS file {path}: {e}")
            print(f"Traceback: {traceback.format_exc()}")
            return -3
        except Exception as e:
            import traceback

            print(f"Unexpected error reading FIS file {path}: {e}")
            print(f"Traceback: {traceback.format_exc()}")
            return -3

        if new_fis is None:
            return -3

        try:
            self.model = FISModel(fis=new_fis)
        except Exception as e:
            print(f"Error creating FIS model from file {path}: {e}")
            return -3

        return 1

    def write_fis(self, path: str) -> int:
        """Write the current model to `path`, overwriting existing files.

        Parameters
        ----------
        path : str
            Destination path for the `.fis` file, including the filename.

        Returns
        -------
        int
            1 when the file is written successfully.
            -1 when the selected file has an unsupported extension.
            -2 when no model is available to write.
            -3 when writing the file fails.
        """
        if not self._check_if_extension_is_supported(path):
            return -1

        if self.model is None:
            return -2

        try:
            writeFIS(self.model._fis, path)
        except Exception:  # pragma: no cover
            return -3

        if not os.path.isfile(path):
            return -3

        return 1

    def _check_if_extension_is_supported(self, path: str) -> bool:
        is_supported = False
        for extension in SUPPORTED_EXTENSIONS:
            if path.endswith(extension) is True:
                is_supported = True

        return is_supported
