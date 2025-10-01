from typing import Any, List

from PyQt6.QtCore import pyqtSignal

from app.view_models.base_view_model import BaseViewModel


class CentralTabViewModel(BaseViewModel):
    """View model for the central tab view."""

    # Signals for tab changes
    current_tab_changed = pyqtSignal(int)

    # Signals for FIS plot updates
    fis_plot_updated = pyqtSignal()

    # Signals for MF plot updates
    mf_plot_updated = pyqtSignal(str, int)  # variable_name, mf_index

    # Signals for rule editor updates
    rules_updated = pyqtSignal(list)
    rule_selected = pyqtSignal(int)
    clear_rules_requested = pyqtSignal()

    # Signals for system updates
    system_name_changed = pyqtSignal(str)

    def __init__(self, model: Any = None) -> None:
        """Initialize the CentralTabViewModel.

        Args:
            model (Any): The FIS model instance.
        """
        super().__init__()
        self._model = model
        self._current_tab = 0
        self._rules = []
        self._system_name = "Placeholder Name"
        self._selected_rule_index = -1

    @property
    def model(self) -> Any:
        """Get the FIS model."""
        return self._model

    @model.setter
    def model(self, value: Any) -> None:
        """Set the FIS model and update data."""
        self._model = value
        self._update_data()

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

    @property
    def system_name(self) -> str:
        """Get the system name."""
        return self._system_name

    @system_name.setter
    def system_name(self, value: str) -> None:
        """Set the system name."""
        if self._system_name != value:
            self._system_name = value
            self.system_name_changed.emit(value)

    @property
    def rules(self) -> List[dict]:
        """Get the rules list."""
        return self._rules

    @property
    def selected_rule_index(self) -> int:
        """Get the selected rule index."""
        return self._selected_rule_index

    def _update_data(self) -> None:
        """Update data from the model."""
        if not self._model:
            return

        self._update_rules()
        self._update_system_name()

    def _update_rules(self) -> None:
        """Update rules from the model."""
        if not self._model or not hasattr(self._model, "_fis"):
            self._rules = []
            return

        fis = self._model._fis
        self._rules = []

        for i, rule in enumerate(fis.Rules):
            rule_data = {
                "index": i,
                "name": rule.Name,
                "antecedent": rule.Antecedent.copy(),
                "consequent": rule.Consequent.copy(),
                "weight": rule.Weight,
                "connection": rule.Connection,
                "is_mf": rule.IsMF.copy() if hasattr(rule, "IsMF") else [],
            }
            self._rules.append(rule_data)

        self.rules_updated.emit(self._rules)

    def _update_system_name(self) -> None:
        """Update system name from the model."""
        if not self._model or not hasattr(self._model, "_fis"):
            return

        fis = self._model._fis
        if hasattr(fis, "Name") and fis.Name:
            self.system_name = fis.Name

    def set_current_tab(self, tab_index: int) -> None:
        """Set the current tab."""
        self.current_tab = tab_index

    def select_rule(self, rule_index: int) -> None:
        """Select a rule."""
        if 0 <= rule_index < len(self._rules):
            self._selected_rule_index = rule_index
            self.rule_selected.emit(rule_index)

    def clear_rules(self) -> None:
        """Clear all rules."""
        if self._model:
            self._model.clear_all_rules()
            self._update_rules()
        self.clear_rules_requested.emit()

    def update_fis_plot(self) -> None:
        """Update the FIS plot."""
        self.fis_plot_updated.emit()

    def update_mf_plot(self, variable_name: str, mf_index: int) -> None:
        """Update the MF plot for a specific variable and membership function."""
        self.mf_plot_updated.emit(variable_name, mf_index)

    def get_rule_text(self, rule_index: int) -> str:
        """Get the text representation of a rule."""
        if not (0 <= rule_index < len(self._rules)):
            return ""

        rule = self._rules[rule_index]

        # Build antecedent text
        antecedent_parts = []
        for i, mf_idx in enumerate(rule["antecedent"]):
            if mf_idx > 0:  # 0 means no condition
                if i < len(self._model._fis.Inputs):
                    input_name = self._model._fis.Inputs[i].Name
                    if mf_idx <= len(self._model._fis.Inputs[i].MembershipFunctions):
                        mf_name = (
                            self._model._fis.Inputs[i]
                            .MembershipFunctions[mf_idx - 1]
                            .Name
                        )
                        is_not = (
                            "not "
                            if (i < len(rule["is_mf"]) and rule["is_mf"][i] != 1)
                            else ""
                        )
                        antecedent_parts.append(f"{input_name} is {is_not}{mf_name}")

        # Build consequent text
        consequent_parts = []
        for i, mf_idx in enumerate(rule["consequent"]):
            if mf_idx > 0:  # 0 means no condition
                output_idx = i + len(rule["antecedent"])
                if output_idx < len(self._model._fis.Outputs):
                    output_name = self._model._fis.Outputs[i].Name
                    if mf_idx <= len(self._model._fis.Outputs[i].MembershipFunctions):
                        mf_name = (
                            self._model._fis.Outputs[i]
                            .MembershipFunctions[mf_idx - 1]
                            .Name
                        )
                        is_not = (
                            "not "
                            if (
                                output_idx < len(rule["is_mf"])
                                and rule["is_mf"][output_idx] != 1
                            )
                            else ""
                        )
                        consequent_parts.append(f"{output_name} is {is_not}{mf_name}")

        # Combine parts
        connection = " and " if rule["connection"] == 1 else " or "
        antecedent_text = connection.join(antecedent_parts)
        consequent_text = " and ".join(consequent_parts)

        return f"If {antecedent_text} then {consequent_text} (weight: {rule['weight']})"

    def refresh_data(self) -> None:
        """Refresh all data from the model."""
        self._update_data()
        self.update_fis_plot()
