from typing import Any, List

from PyQt6.QtCore import pyqtSignal

from app.view_models.base_view_model import BaseViewModel


class BrowserFrameViewModel(BaseViewModel):
    """View model for the browser frame view."""

    # Signals for system browser updates
    system_browser_updated = pyqtSignal(list)
    design_browser_updated = pyqtSignal(list)

    # Signals for selection changes
    system_item_selected = pyqtSignal(str, dict)  # item_name, item_data
    design_item_selected = pyqtSignal(str, dict)  # item_name, item_data

    def __init__(self, model: Any = None) -> None:
        """Initialize the BrowserFrameViewModel.

        Args:
            model (Any): The FIS model instance for the browser.
        """
        super().__init__()
        self._model = model
        self._system_items = []
        self._design_items = []

    @property
    def model(self) -> Any:
        """Get the FIS model."""
        return self._model

    @model.setter
    def model(self, value: Any) -> None:
        """Set the FIS model and update browser data."""
        self._model = value
        self._update_browser_data()

    @property
    def system_items(self) -> List[dict]:
        """Get the system browser items."""
        return self._system_items

    @property
    def design_items(self) -> List[dict]:
        """Get the design browser items."""
        return self._design_items

    def _update_browser_data(self) -> None:
        """Update the browser data from the model."""
        if not self._model:
            return

        # Update system items (inputs, outputs, rules)
        self._system_items = self._get_system_items()
        self.system_browser_updated.emit(self._system_items)

        # Update design items (membership functions, etc.)
        self._design_items = self._get_design_items()
        self.design_browser_updated.emit(self._design_items)

    def _get_system_items(self) -> List[dict]:
        """Get system items from the FIS model."""
        items = []

        if not self._model or not hasattr(self._model, "_fis"):
            return items

        fis = self._model._fis

        # Add inputs
        for i, input_var in enumerate(fis.Inputs):
            items.append(
                {
                    "type": "input",
                    "name": input_var.Name,
                    "index": i,
                    "range": input_var.Range,
                    "mf_count": len(input_var.MembershipFunctions),
                }
            )

        # Add outputs
        for i, output_var in enumerate(fis.Outputs):
            items.append(
                {
                    "type": "output",
                    "name": output_var.Name,
                    "index": i,
                    "range": output_var.Range,
                    "mf_count": len(output_var.MembershipFunctions),
                }
            )

        # Add rules
        for i, rule in enumerate(fis.Rules):
            items.append(
                {
                    "type": "rule",
                    "name": rule.Name,
                    "index": i,
                    "antecedent": rule.Antecedent,
                    "consequent": rule.Consequent,
                    "weight": rule.Weight,
                    "connection": rule.Connection,
                }
            )

        return items

    def _get_design_items(self) -> List[dict]:
        """Get design items from the FIS model."""
        items = []

        if not self._model or not hasattr(self._model, "_fis"):
            return items

        fis = self._model._fis

        # Add membership functions for inputs
        for input_var in fis.Inputs:
            for i, mf in enumerate(input_var.MembershipFunctions):
                items.append(
                    {
                        "type": "input_mf",
                        "variable_name": input_var.Name,
                        "name": mf.Name,
                        "index": i,
                        "mf_type": mf.Type,
                        "parameters": mf.Parameters,
                    }
                )

        # Add membership functions for outputs
        for output_var in fis.Outputs:
            for i, mf in enumerate(output_var.MembershipFunctions):
                items.append(
                    {
                        "type": "output_mf",
                        "variable_name": output_var.Name,
                        "name": mf.Name,
                        "index": i,
                        "mf_type": mf.Type,
                        "parameters": mf.Parameters,
                    }
                )

        return items

    def select_system_item(self, item_name: str, item_data: dict) -> None:
        """Handle system item selection."""
        self.system_item_selected.emit(item_name, item_data)

    def select_design_item(self, item_name: str, item_data: dict) -> None:
        """Handle design item selection."""
        self.design_item_selected.emit(item_name, item_data)

    def refresh_browser(self) -> None:
        """Refresh the browser data."""
        self._update_browser_data()
