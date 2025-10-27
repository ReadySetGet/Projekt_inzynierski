"""Input/Output class for fuzzy logic system."""


class InOutput:
    """Represents an input or output in the fuzzy logic system."""

    def __init__(self, name, mfs):
        """Initialize input/output with name and membership functions.

        Args:
            name: Name of the input/output
            mfs: List of membership functions
        """
        self._name = name
        self._mfs = mfs

    def GetName(self):
        """Get the name of the input/output.

        Returns:
            Name of the input/output
        """
        return self._name

    def GetMfs(self):
        """Get the membership functions.

        Returns:
            List of membership functions
        """
        return self._mfs
