from typing import Any, Dict, List, Optional

from PyQt6.QtCore import pyqtSignal

from app.view_models.base_view_model import BaseViewModel


class RulesEditorViewModel(BaseViewModel):
    """View model for the rules editor tab."""

    # Signals for rule updates
    rules_updated = pyqtSignal(list)
    rule_added = pyqtSignal(int)  # rule_index
    rule_deleted = pyqtSignal(int)  # rule_index
    rule_updated = pyqtSignal(int)  # rule_index

    # Signals for rule editing
    rule_selected = pyqtSignal(int)  # rule_index
    rule_name_changed = pyqtSignal(int, str)  # rule_index, new_name
    rule_weight_changed = pyqtSignal(int, float)  # rule_index, new_weight
    rule_connection_changed = pyqtSignal(
        int, int
    )  # rule_index, new_connection (1=AND, 0=OR)

    # Signals for condition updates
    antecedent_changed = pyqtSignal(int, list)  # rule_index, new_antecedent
    consequent_changed = pyqtSignal(int, list)  # rule_index, new_consequent
    is_mf_changed = pyqtSignal(int, list)  # rule_index, new_is_mf list

    # Signals for dropdown updates
    input_mf_options_updated = pyqtSignal(list)  # list of input MF options
    output_mf_options_updated = pyqtSignal(list)  # list of output MF options

    def __init__(self, model: Any = None) -> None:
        """Initialize the RulesEditorViewModel.

        Args:
            model (Any): The FIS model instance.
        """
        super().__init__()
        self._model = model
        self._selected_rule_index = -1
        self._rules = []
        self._input_mf_options = []
        self._output_mf_options = []

    @property
    def model(self) -> Any:
        """Get the FIS model."""
        return self._model

    @model.setter
    def model(self, value: Any) -> None:
        """Set the FIS model and update data."""
        self._model = value
        self._update_rules()
        self._update_mf_options()

    @property
    def rules(self) -> List[Dict]:
        """Get the rules list."""
        return self._rules

    @property
    def selected_rule_index(self) -> int:
        """Get the selected rule index."""
        return self._selected_rule_index

    @property
    def input_mf_options(self) -> List[Dict]:
        """Get the input membership function options."""
        return self._input_mf_options

    @property
    def output_mf_options(self) -> List[Dict]:
        """Get the output membership function options."""
        return self._output_mf_options

    def _update_rules(self) -> None:
        """Update rules from the model."""
        if not self._model or not hasattr(self._model, "_fis"):
            self._rules = []
            self.rules_updated.emit(self._rules)
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

    def _update_mf_options(self) -> None:
        """Update membership function options from the model."""
        if not self._model or not hasattr(self._model, "_fis"):
            self._input_mf_options = []
            self._output_mf_options = []
            return

        fis = self._model._fis

        # Update input MF options
        self._input_mf_options = []
        for input_var in fis.Inputs:
            for i, mf in enumerate(input_var.MembershipFunctions):
                self._input_mf_options.append(
                    {
                        "variable_name": input_var.Name,
                        "mf_name": mf.Name,
                        "mf_index": i,
                        "display_name": f"{input_var.Name}.{mf.Name}",
                    }
                )

        # Update output MF options
        self._output_mf_options = []
        for output_var in fis.Outputs:
            for i, mf in enumerate(output_var.MembershipFunctions):
                self._output_mf_options.append(
                    {
                        "variable_name": output_var.Name,
                        "mf_name": mf.Name,
                        "mf_index": i,
                        "display_name": f"{output_var.Name}.{mf.Name}",
                    }
                )

        self.input_mf_options_updated.emit(self._input_mf_options)
        self.output_mf_options_updated.emit(self._output_mf_options)

    def select_rule(self, rule_index: int) -> None:
        """Select a rule."""
        if 0 <= rule_index < len(self._rules):
            self._selected_rule_index = rule_index
            self.rule_selected.emit(rule_index)

    def add_rule(
        self,
        rule_name: str = "Placeholder",
        weight: float = 1.0,
        connection: int = 1,
        antecedent: List[int] = None,
        consequent: List[int] = None,
        is_mf: List[int] = None,
    ) -> bool:
        """Add a new rule."""
        if not self._model:
            return False

        result = self._model.add_rule(
            is_mf,
            (
                antecedent + consequent + [weight, connection]
                if antecedent and consequent
                else None
            ),
        )

        if result == 1:  # Success
            self._update_rules()
            new_rule_index = len(self._rules) - 1
            self.rule_added.emit(new_rule_index)
            return True

        return False

    def delete_rule(self, rule_index: int) -> bool:
        """Delete a rule."""
        if not self._model or not (0 <= rule_index < len(self._rules)):
            return False

        result = self._model.delete_rule(rule_index)

        if result == 1:  # Success
            self.rule_deleted.emit(rule_index)
            self._update_rules()
            return True

        return False

    def update_rule(
        self,
        rule_index: int,
        new_antecedent: List[int],
        new_consequent: List[int],
        new_weight: float,
        new_connection: int,
        new_is_mf: List[int],
    ) -> bool:
        """Update a rule."""
        if not self._model or not (0 <= rule_index < len(self._rules)):
            return False

        new_rule_data = new_antecedent + new_consequent + [new_weight, new_connection]
        result = self._model.update_rule(rule_index, new_is_mf, new_rule_data)

        if result == 1:  # Success
            self.rule_updated.emit(rule_index)
            self._update_rules()
            return True

        return False

    def update_rule_name(self, rule_index: int, new_name: str) -> bool:
        """Update a rule's name."""
        if not (0 <= rule_index < len(self._rules)):
            return False

        if self._model and hasattr(self._model, "_fis"):
            fis = self._model._fis
            if 0 <= rule_index < len(fis.Rules):
                fis.Rules[rule_index].Name = new_name
                self.rule_name_changed.emit(rule_index, new_name)
                self._update_rules()
                return True

        return False

    def update_rule_weight(self, rule_index: int, new_weight: float) -> bool:
        """Update a rule's weight."""
        if not (0 <= rule_index < len(self._rules)):
            return False

        if self._model and hasattr(self._model, "_fis"):
            fis = self._model._fis
            if 0 <= rule_index < len(fis.Rules):
                fis.Rules[rule_index].Weight = new_weight
                self.rule_weight_changed.emit(rule_index, new_weight)
                self._update_rules()
                return True

        return False

    def update_rule_connection(self, rule_index: int, new_connection: int) -> bool:
        """Update a rule's connection (AND/OR)."""
        if not (0 <= rule_index < len(self._rules)):
            return False

        if self._model and hasattr(self._model, "_fis"):
            fis = self._model._fis
            if 0 <= rule_index < len(fis.Rules):
                fis.Rules[rule_index].Connection = new_connection
                self.rule_connection_changed.emit(rule_index, new_connection)
                self._update_rules()
                return True

        return False

    def get_rule_text(self, rule_index: int) -> str:
        """Get the text representation of a rule."""
        if not (0 <= rule_index < len(self._rules)):
            return ""

        rule = self._rules[rule_index]

        if not self._model or not hasattr(self._model, "_fis"):
            return f"Rule {rule_index}: {rule['name']}"

        fis = self._model._fis

        # Build antecedent text
        antecedent_parts = []
        for i, mf_idx in enumerate(rule["antecedent"]):
            if mf_idx > 0:  # 0 means no condition
                if i < len(fis.Inputs):
                    input_name = fis.Inputs[i].Name
                    if mf_idx <= len(fis.Inputs[i].MembershipFunctions):
                        mf_name = fis.Inputs[i].MembershipFunctions[mf_idx - 1].Name
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
                if i < len(fis.Outputs):
                    output_name = fis.Outputs[i].Name
                    if mf_idx <= len(fis.Outputs[i].MembershipFunctions):
                        mf_name = fis.Outputs[i].MembershipFunctions[mf_idx - 1].Name
                        output_idx = i + len(rule["antecedent"])
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

    def get_selected_rule(self) -> Optional[Dict]:
        """Get the currently selected rule."""
        if 0 <= self._selected_rule_index < len(self._rules):
            return self._rules[self._selected_rule_index]
        return None

    def clear_all_rules(self) -> bool:
        """Clear all rules."""
        if self._model:
            self._model.clear_all_rules()
            self._update_rules()
            return True
        return False

    def refresh_data(self) -> None:
        """Refresh all data from the model."""
        self._update_rules()
        self._update_mf_options()
