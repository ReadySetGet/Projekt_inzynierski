from typing import Dict, List, Optional

from PyQt6.QtCore import pyqtSignal

from app.view_models.base_view_model import BaseViewModel


class RulesEditorViewModel(BaseViewModel):
    """View model for the rules editor tab."""

    rules_updated = pyqtSignal(list)
    rule_added = pyqtSignal(int)
    rule_deleted = pyqtSignal(int)
    rule_updated = pyqtSignal(int)
    rule_selected = pyqtSignal(int)
    rule_name_changed = pyqtSignal(int, str)
    rule_weight_changed = pyqtSignal(int, float)
    rule_connection_changed = pyqtSignal(int, int)
    antecedent_changed = pyqtSignal(int, list)
    consequent_changed = pyqtSignal(int, list)
    is_mf_changed = pyqtSignal(int, list)
    input_mf_options_updated = pyqtSignal(list)
    output_mf_options_updated = pyqtSignal(list)

    def __init__(self) -> None:
        """Initialize the RulesEditorViewModel."""
        super().__init__()
        self._selected_rule_index = -1
        self._rules = []
        self._input_mf_options = []
        self._output_mf_options = []

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
        if not self.fuzzy_service:
            self._rules = []
            self.rules_updated.emit(self._rules)
            return

        rules_data = self.fuzzy_service.get_rules()
        self._rules = []

        for i, rule_data in enumerate(rules_data):
            rule_dict = {
                "index": i,
                "name": rule_data.get("name", f"Rule {i+1}"),
                "antecedent": rule_data.get("antecedent", []),
                "consequent": rule_data.get("consequent", []),
                "weight": rule_data.get("weight", 1.0),
                "connection": rule_data.get("connection", 1),
                "is_mf": rule_data.get("is_mf", []),
            }
            self._rules.append(rule_dict)

        self.rules_updated.emit(self._rules)

    def _update_mf_options(self) -> None:
        """Update membership function options from the model."""
        if not self.fuzzy_service:
            self._input_mf_options = []
            self._output_mf_options = []
            return

        input_variables = self.fuzzy_service.get_input_variables()
        output_variables = self.fuzzy_service.get_output_variables()

        self._input_mf_options = []
        for input_var in input_variables:
            var_name = input_var.get("name", "")
            mfs = self.fuzzy_service.get_membership_functions(var_name, "input")
            for mf in mfs:
                mf_name = mf.get("name", "")
                self._input_mf_options.append(f"{var_name}.{mf_name}")

        self._output_mf_options = []
        for output_var in output_variables:
            var_name = output_var.get("name", "")
            mfs = self.fuzzy_service.get_membership_functions(var_name, "output")
            for mf in mfs:
                mf_name = mf.get("name", "")
                self._output_mf_options.append(f"{var_name}.{mf_name}")

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
        if not self.fuzzy_service:
            return False

        result = self.fuzzy_service.add_rule(
            rule_name,
            antecedent,
            consequent,
            weight,
            connection,
            is_mf,
        )

        if result:
            self._update_rules()
            new_rule_index = len(self._rules) - 1
            self.rule_added.emit(new_rule_index)
            self.notify_data_changed.emit()
            return True

        return False

    def delete_rule(self, rule_index: int) -> bool:
        """Delete a rule."""
        if not self.fuzzy_service or not (0 <= rule_index < len(self._rules)):
            return False

        result = self.fuzzy_service.delete_rule(rule_index)

        if result:
            self.rule_deleted.emit(rule_index)
            self._update_rules()
            self.notify_data_changed.emit()
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
        if not self.fuzzy_service or not (0 <= rule_index < len(self._rules)):
            return False

        result = self.fuzzy_service.update_rule(
            rule_index,
            new_antecedent,
            new_consequent,
            new_weight,
            new_connection,
            new_is_mf,
        )

        if result:
            self.rule_updated.emit(rule_index)
            self._update_rules()
            self.notify_data_changed.emit()
            return True

        return False

    def update_rule_name(self, rule_index: int, new_name: str) -> bool:
        """Update a rule's name."""
        if not (0 <= rule_index < len(self._rules)):
            return False

        if self.fuzzy_service._rule_manager:
            result = self.fuzzy_service._rule_manager.update_rule_name(rule_index, new_name)
            if result:
                self._rules[rule_index]["name"] = new_name
                self.rule_name_changed.emit(rule_index, new_name)
                self._update_rules()
                self.notify_data_changed.emit()
                return True
        else:
            return False

        return False

    def update_rule_weight(self, rule_index: int, new_weight: float) -> bool:
        """Update a rule's weight."""
        if not (0 <= rule_index < len(self._rules)):
            return False

        current_rule = self._rules[rule_index]
        result = self.fuzzy_service.update_rule(
            rule_index,
            current_rule["antecedent"],
            current_rule["consequent"],
            new_weight,
            current_rule["connection"],
            current_rule["is_mf"],
        )
        if result:
            self._rules[rule_index]["weight"] = new_weight
            self.rule_weight_changed.emit(rule_index, new_weight)
            self._update_rules()
            self.notify_data_changed.emit()
            return True

        return False

    def update_rule_connection(self, rule_index: int, new_connection: int) -> bool:
        """Update a rule's connection (AND/OR)."""
        if not (0 <= rule_index < len(self._rules)):
            return False

        current_rule = self._rules[rule_index]
        result = self.fuzzy_service.update_rule(
            rule_index,
            current_rule["antecedent"],
            current_rule["consequent"],
            current_rule["weight"],
            new_connection,
            current_rule["is_mf"],
        )
        if result:
            self._rules[rule_index]["connection"] = new_connection
            self.rule_connection_changed.emit(rule_index, new_connection)
            self._update_rules()
            self.notify_data_changed.emit()
            return True

        return False

    def get_rule_text(self, rule_index: int) -> str:
        """Get the text representation of a rule."""
        if not (0 <= rule_index < len(self._rules)):
            return ""

        rule = self._rules[rule_index]

        if not self.fuzzy_service:
            return f"Rule {rule_index}: {rule['name']}"

        try:
            return self.fuzzy_service.get_rule_text(rule_index)
        except Exception:
            return f"Rule {rule_index}: {rule['name']}"

    def get_selected_rule(self) -> Optional[Dict]:
        """Get the currently selected rule."""
        if 0 <= self._selected_rule_index < len(self._rules):
            return self._rules[self._selected_rule_index]
        return None

    def clear_all_rules(self) -> bool:
        """Clear all rules."""
        result = self.fuzzy_service.clear_all_rules()
        if result:
            self._update_rules()
            self.notify_data_changed.emit()
            return True
        return False

    def update_data(self) -> None:
        """Update data from the model."""
        self._update_rules()
        self._update_mf_options()

    def refresh_data(self) -> None:
        """Refresh all data from the model - only updates logic, no signal emission."""
        self._update_rules()
        self._update_mf_options()

    def add_all_possible_rules(self) -> bool:
        """Add all possible rules."""
        result = self.fuzzy_service.add_all_possible_rules()
        if result:
            self._update_rules()
            self.notify_data_changed.emit()
        return result
