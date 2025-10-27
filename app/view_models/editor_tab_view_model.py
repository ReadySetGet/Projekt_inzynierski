from PyQt6.QtCore import pyqtSignal

from app.view_models.base_view_model import BaseViewModel


class EditorTabViewModel(BaseViewModel):
    """View model for the editor tab view."""

    # Signals for tab changes
    current_tab_changed = pyqtSignal(int)

    # Signals for FIS properties tab
    fis_properties_updated = pyqtSignal()

    # Signals for MF properties tab
    mf_properties_updated = pyqtSignal()

    # Signals for rule properties tab
    rule_properties_updated = pyqtSignal()

    def __init__(self) -> None:
        """Initialize the EditorTabViewModel."""
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

    def _update_all_tabs(self) -> None:
        """Update all tab data from the model."""
        if not self.fuzzy_service:
            return

        self.fis_properties_updated.emit()
        self.mf_properties_updated.emit()
        self.rule_properties_updated.emit()

    def update_fis_properties_tab(self) -> None:
        """Update the FIS properties tab."""
        self.fis_properties_updated.emit()

    def update_mf_properties_tab(self) -> None:
        """Update the MF properties tab."""
        self.mf_properties_updated.emit()

    def update_rule_properties_tab(self) -> None:
        """Update the rule properties tab."""
        self.rule_properties_updated.emit()

    def refresh_data(self) -> None:
        """Refresh all data from the model - only updates logic, no signal emission."""
        self._update_all_tabs()

    def refresh_all_tabs(self) -> None:
        """Refresh all tabs with current model data."""
        self._update_all_tabs()
