from typing import Any

from PyQt6.QtCore import pyqtSignal

from app.view_models.base_view_model import BaseViewModel


class CounterViewModel(BaseViewModel):
    """View model for the counter view."""

    count_changed = pyqtSignal(int)  # Signal to update the count in the views
    can_increment_changed = pyqtSignal(bool)
    model: Any

    def __init__(self, model: Any) -> None:
        """Initialize the CounterViewModel.

        Args:
            model (Any): The model instance for the counter.
        """
        super().__init__()
        self._model = model
        # Add any additional initialization or properties as needed

    def increment(self) -> None:
        """Increment the counter in the model."""
        self.model.increment()
