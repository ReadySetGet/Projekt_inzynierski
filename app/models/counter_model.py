"""Counter model for the application."""

import time


class CounterModel:
    """Model for counting operations."""

    count: int

    def __init__(self) -> None:
        """Initialize the counter model."""
        self.count = 0

    def increment(self) -> None:
        """Increment the counter by 1."""
        self.count += 1
        time.sleep(0.1)
