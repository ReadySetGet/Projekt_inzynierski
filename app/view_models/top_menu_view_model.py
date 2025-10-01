from typing import Any

from PyQt6.QtCore import pyqtSignal

from app.view_models.base_view_model import BaseViewModel


class TopMenuViewModel(BaseViewModel):
    """View model for the top menu view."""

    # Signals for tab changes
    current_tab_changed = pyqtSignal(int)

    # Signals for input/output management
    add_input_clicked = pyqtSignal()
    delete_input_clicked = pyqtSignal()
    add_output_clicked = pyqtSignal()
    delete_output_clicked = pyqtSignal()

    # Signals for system updates
    system_updated = pyqtSignal()

    def __init__(self, model: Any = None) -> None:
        """Initialize the TopMenuViewModel.

        Args:
            model (Any): The FIS model instance.
        """
        super().__init__()
        self._model = model
        self._current_tab = 0

    @property
    def model(self) -> Any:
        """Get the FIS model."""
        return self._model

    @model.setter
    def model(self, value: Any) -> None:
        """Set the FIS model."""
        self._model = value

    @property
    def current_tab(self) -> int:
        """Get the current tab index."""
        return self._current_tab

    @current_tab.setter
    def current_tab(self, value: int) -> None:
        """Set the current tab index."""
        if self._current_tab != value:
            self._current_tab = value
            self.current_tab_changed.emit(value)

    def set_current_tab(self, tab_index: int) -> None:
        """Set the current tab."""
        self.current_tab = tab_index

    def add_input(self) -> None:
        """Handle add input button click."""
        if self._model:
            self._model.add_input()
            self.system_updated.emit()
        self.add_input_clicked.emit()

    def delete_input(self) -> None:
        """Handle delete input button click."""
        if self._model and hasattr(self._model, "_fis"):
            fis = self._model._fis
            if fis.Inputs:  # Only delete if there are inputs
                # Delete the last input (or could be more sophisticated)
                result = self._model.delete_input(len(fis.Inputs) - 1)
                if result == 1:  # Success
                    self.system_updated.emit()
        self.delete_input_clicked.emit()

    def add_output(self) -> None:
        """Handle add output button click."""
        if self._model:
            self._model.add_output()
            self.system_updated.emit()
        self.add_output_clicked.emit()

    def delete_output(self) -> None:
        """Handle delete output button click."""
        if self._model and hasattr(self._model, "_fis"):
            fis = self._model._fis
            if fis.Outputs:  # Only delete if there are outputs
                # Delete the last output (or could be more sophisticated)
                result = self._model.delete_output(len(fis.Outputs) - 1)
                if result == 1:  # Success
                    self.system_updated.emit()
        self.delete_output_clicked.emit()

    def can_delete_input(self) -> bool:
        """Check if input can be deleted."""
        if not self._model or not hasattr(self._model, "_fis"):
            return False
        return len(self._model._fis.Inputs) > 0

    def can_delete_output(self) -> bool:
        """Check if output can be deleted."""
        if not self._model or not hasattr(self._model, "_fis"):
            return False
        return len(self._model._fis.Outputs) > 0

    def get_input_count(self) -> int:
        """Get the number of inputs."""
        if not self._model or not hasattr(self._model, "_fis"):
            return 0
        return len(self._model._fis.Inputs)

    def get_output_count(self) -> int:
        """Get the number of outputs."""
        if not self._model or not hasattr(self._model, "_fis"):
            return 0
        return len(self._model._fis.Outputs)
