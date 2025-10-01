import inspect
from typing import Any, Callable

from PyQt6.QtCore import QObject, pyqtSignal

from app.utils.keys import PROGRESS_CALLBACK


class Worker(QObject):
    """General-purpose worker for running any function in a background thread.

    This worker provides support for result, error, progress, and finished signals.
    """

    finished = pyqtSignal()
    error = pyqtSignal(Exception)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)

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

        # Check if the function accepts a progress callback
        signature = inspect.signature(fn)
        if PROGRESS_CALLBACK in signature.parameters:
            # Inject progress callback if used
            self.kwargs[PROGRESS_CALLBACK] = self.progress.emit

    def run(self) -> None:
        """Run the worker function in a background thread."""
        try:
            result = self.fn(*self.args, **self.kwargs)
            self.result.emit(result)
        except Exception as e:
            self.error.emit(e)
        finally:
            self.finished.emit()
