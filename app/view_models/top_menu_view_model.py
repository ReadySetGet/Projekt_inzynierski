# No imports needed

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

    def __init__(self) -> None:
        """Initialize the TopMenuViewModel."""
        super().__init__()
        self._current_tab = 0

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
        # Add a new input variable with default name and range
        input_count = self.fuzzy_service.get_input_count()
        success = self.fuzzy_service.add_input_variable(f"input{input_count + 1}", 0.0, 100.0)
        if success:
            self.notify_data_changed.emit()

    def delete_input(self) -> None:
        """Handle delete input button click."""
        input_count = self.fuzzy_service.get_input_count()
        if input_count > 0:
            # Delete the last input variable
            success = self.fuzzy_service.delete_input_variable(input_count - 1)
            if success:
                self.notify_data_changed.emit()

    def add_output(self) -> None:
        """Handle add output button click."""
        # Add a new output variable with default name and range
        output_count = self.fuzzy_service.get_output_count()
        success = self.fuzzy_service.add_output_variable(f"output{output_count}", 0.0, 100.0)
        if success:
            self.notify_data_changed.emit()

    def delete_output(self) -> None:
        """Handle delete output button click."""
        output_count = self.fuzzy_service.get_output_count()
        if output_count > 0:
            # Delete the last output variable
            success = self.fuzzy_service.delete_output_variable(output_count - 1)
            if success:
                self.notify_data_changed.emit()

    def can_delete_input(self) -> bool:
        """Check if input can be deleted."""
        return self.fuzzy_service.get_input_count() > 0

    def can_delete_output(self) -> bool:
        """Check if output can be deleted."""
        return self.fuzzy_service.get_output_count() > 0

    def get_input_count(self) -> int:
        """Get the number of inputs."""
        return self.fuzzy_service.get_input_count()

    def get_output_count(self) -> int:
        """Get the number of outputs."""
        return self.fuzzy_service.get_output_count()

    def refresh_data(self) -> None:
        """Refresh all data from the model - only updates logic, no signal emission."""
        # TopMenuViewModel doesn't need to refresh data as it's mostly action-based
        pass
