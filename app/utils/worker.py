import inspect

from PyQt6.QtCore import pyqtSignal, QObject

from app.utils.keys import PROGRESS_CALLBACK


class Worker(QObject):
    """
    General-purpose worker for running any function in a background thread,
    with support for result, error, progress, and finished signals.
    """
    finished = pyqtSignal()
    error = pyqtSignal(Exception)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)

    def __init__(self, fn, *args, **kwargs):
        super().__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

        signature = inspect.signature(fn)
        if PROGRESS_CALLBACK in signature.parameters:
            self.kwargs[PROGRESS_CALLBACK] = self.progress.emit  # Inject progress callback if used

    def run(self):
        try:
            result = self.fn(*self.args, **self.kwargs)
            self.result.emit(result)
        except Exception as e:
            self.error.emit(e)
        finally:
            self.finished.emit()