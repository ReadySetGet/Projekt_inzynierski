from typing import List

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

    def __init__(self) -> None:
        """Initialize the BrowserFrameViewModel."""
        super().__init__()
        self._system_items = []
        self._design_items = []

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
        if not self.fuzzy_service:
            return

        self._system_items = self._get_system_items()
        self.system_browser_updated.emit(self._system_items)

        self._design_items = self._get_design_items()
        self.design_browser_updated.emit(self._design_items)

    def _get_system_items(self) -> List[dict]:
        """Get system items from the FIS model."""
        items = []

        if not self.fuzzy_service:
            return items

        input_variables = self.fuzzy_service.get_input_variables()
        for i, input_var in enumerate(input_variables):
            items.append(
                {
                    "type": "input",
                    "name": input_var.get("name", f"Input_{i}"),
                    "index": i,
                    "range": input_var.get("range", [0, 1]),
                    "mf_count": len(input_var.get("membership_functions", [])),
                    "membership_functions": input_var.get("membership_functions", []),
                }
            )

        output_variables = self.fuzzy_service.get_output_variables()
        for i, output_var in enumerate(output_variables):
            items.append(
                {
                    "type": "output",
                    "name": output_var.get("name", f"Output_{i}"),
                    "index": i,
                    "range": output_var.get("range", [0, 1]),
                    "mf_count": len(output_var.get("membership_functions", [])),
                    "membership_functions": output_var.get("membership_functions", []),
                }
            )

        rules = self.fuzzy_service.get_rules()
        for i, rule in enumerate(rules):
            items.append(
                {
                    "type": "rule",
                    "name": rule.get("name", f"Rule_{i+1}"),
                    "index": i,
                    "antecedent": rule.get("antecedent", []),
                    "consequent": rule.get("consequent", []),
                    "weight": rule.get("weight", 1.0),
                    "connection": rule.get("connection", 1),
                }
            )

        return items

    def _get_design_items(self) -> List[dict]:
        """Get design items from the FIS model."""
        items = []

        if not self.fuzzy_service:
            return items

        input_variables = self.fuzzy_service.get_input_variables()
        for input_var in input_variables:
            var_name = input_var.get("name", "")
            mfs = self.fuzzy_service.get_membership_functions(var_name, "input")
            for i, mf in enumerate(mfs):
                items.append(
                    {
                        "type": "input_mf",
                        "variable_name": var_name,
                        "name": mf.get("name", f"MF_{i}"),
                        "index": i,
                        "mf_type": mf.get("type", "triangular"),
                        "parameters": mf.get("parameters", []),
                    }
                )

        output_variables = self.fuzzy_service.get_output_variables()
        for output_var in output_variables:
            var_name = output_var.get("name", "")
            mfs = self.fuzzy_service.get_membership_functions(var_name, "output")
            for i, mf in enumerate(mfs):
                items.append(
                    {
                        "type": "output_mf",
                        "variable_name": var_name,
                        "name": mf.get("name", f"MF_{i}"),
                        "index": i,
                        "mf_type": mf.get("type", "triangular"),
                        "parameters": mf.get("parameters", []),
                    }
                )

        return items

    def select_system_item(self, item_name: str, item_data: dict) -> None:
        """Handle system item selection."""
        self.system_item_selected.emit(item_name, item_data)

    def select_design_item(self, item_name: str, item_data: dict) -> None:
        """Handle design item selection."""
        self.design_item_selected.emit(item_name, item_data)

    def refresh_data(self) -> None:
        """Refresh all data from the model - only updates logic, no signal emission."""
        self._update_browser_data()

    def refresh_browser(self) -> None:
        """Refresh the browser data."""
        self._update_browser_data()
