from typing import Any, Callable

from PyQt6.QtCore import QObject


class Worker(QObject):
    """General-purpose worker for running any function in a background thread."""

    fn: Callable[..., Any]
    args: tuple[Any, ...]
    kwargs: dict[str, Any]

    def __init__(self, fn: Callable[..., Any], *args: Any, **kwargs: Any) -> None:
        """Initialize the worker.

        Args:
            fn: The function to run.
            *args: Positional arguments for the function.
            **kwargs: Keyword arguments for the function.
        """
        super().__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    def run(self) -> None:
        """Run the worker function in a background thread."""
        self.fn(*self.args, **self.kwargs)
