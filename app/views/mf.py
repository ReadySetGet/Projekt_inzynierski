"""Membership function class for fuzzy logic system."""


class MembershipFunction:
    """Represents a membership function with x and y coordinates."""

    def __init__(self, x, y):
        """Initialize membership function with x and y coordinates.

        Args:
            x: X coordinate values
            y: Y coordinate values
        """
        self._x = x
        self._y = y

    def getX(self):
        """Get x coordinates.

        Returns:
            X coordinate values
        """
        return self._x

    def getY(self):
        """Get y coordinates.

        Returns:
            Y coordinate values
        """
        return self._y
