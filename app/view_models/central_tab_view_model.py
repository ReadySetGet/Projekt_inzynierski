from typing import List

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

    # Signals for MF Editor communication
    mf_editor_connected = pyqtSignal()
    selected_variable_changed = pyqtSignal(str, bool)

    membership_functions_data_ready = pyqtSignal(str, list, list, list)
    fis_plot_data_ready = pyqtSignal(list, list)
    inference_data_ready = pyqtSignal(list, list)

    def __init__(self) -> None:
        """Initialize the CentralTabViewModel."""
        super().__init__()
        self._current_tab = 0
        self._rules = []
        self._system_name = "Placeholder Name"
        self._selected_rule_index = -1
        self._fuzzy_service = None
        self._mf_editor = None
        self._selected_variable = None
        self._selected_variable_is_input = True
        self._updating = False

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
        if not self.fuzzy_service:
            return

        self._update_rules()
        self._update_system_name()

    def _update_rules(self) -> None:
        """Update rules from the model."""
        if not self.fuzzy_service:
            self._rules = []
            return

        # Use the service API to get rules
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

    def _update_system_name(self) -> None:
        """Update system name from the model."""
        if not self.fuzzy_service:
            return

        system_status = self.fuzzy_service.get_system_status()
        if system_status and "name" in system_status:
            self.system_name = system_status["name"]

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

        antecedent_parts = []
        for i, mf_idx in enumerate(rule["antecedent"]):
            if mf_idx > 0:  # 0 means no condition
                if i < len(self._model._fis.Inputs):
                    input_name = self._model._fis.Inputs[i].Name
                    if mf_idx <= len(self._model._fis.Inputs[i].MembershipFunctions):
                        mf_name = self._model._fis.Inputs[i].MembershipFunctions[mf_idx - 1].Name
                        is_not = "not " if (i < len(rule["is_mf"]) and rule["is_mf"][i] != 1) else ""
                        antecedent_parts.append(f"{input_name} is {is_not}{mf_name}")

        consequent_parts = []
        for i, mf_idx in enumerate(rule["consequent"]):
            if mf_idx > 0:  # 0 means no condition
                output_idx = i + len(rule["antecedent"])
                if output_idx < len(self._model._fis.Outputs):
                    output_name = self._model._fis.Outputs[i].Name
                    if mf_idx <= len(self._model._fis.Outputs[i].MembershipFunctions):
                        mf_name = self._model._fis.Outputs[i].MembershipFunctions[mf_idx - 1].Name
                        is_not = "not " if (output_idx < len(rule["is_mf"]) and rule["is_mf"][output_idx] != 1) else ""
                        consequent_parts.append(f"{output_name} is {is_not}{mf_name}")

        connection = " and " if rule["connection"] == 1 else " or "
        antecedent_text = connection.join(antecedent_parts)
        consequent_text = " and ".join(consequent_parts)

        return f"If {antecedent_text} then {consequent_text} (weight: {rule['weight']})"

    def refresh_data(self) -> None:
        """Refresh all data from the model - only updates logic, no signal emission."""
        self._update_data()
        # Note: update_fis_plot() emits signals, so we don't call it here
        # The view should handle plot updates through other mechanisms

    def set_fuzzy_service(self, fuzzy_service) -> None:
        """Set the fuzzy calculation service."""
        self._fuzzy_service = fuzzy_service
        if fuzzy_service:
            fuzzy_service.system_changed.connect(self._on_system_changed)
            fuzzy_service.inference_completed.connect(self._on_inference_completed)

    def connect_mf_editor(self, mf_editor) -> None:
        """Connect the MF Editor to this view model.

        Args:
            mf_editor: The MF Editor widget to connect
        """
        self._mf_editor = mf_editor
        self.mf_editor_connected.emit()

        if mf_editor.view_model:
            mf_editor.view_model.variable_selected.connect(self._on_mf_editor_variable_selected)
            mf_editor.view_model.mf_list_updated.connect(self._on_mf_list_updated)
            mf_editor.view_model.mf_added.connect(self._on_mf_added)
            mf_editor.view_model.mf_deleted.connect(self._on_mf_deleted)

    def _on_system_changed(self) -> None:
        """Handle system changes from fuzzy service."""
        if self._updating:
            return
        self._updating = True
        try:
            self._update_data()
            self._update_membership_functions_plot()
        finally:
            self._updating = False

    def _on_inference_completed(self, inputs: List, outputs: List) -> None:
        """Handle inference completion."""
        self.inference_data_ready.emit(inputs, outputs)

    def _on_mf_editor_variable_selected(self, variable_name: str, variable_type: str) -> None:
        """Handle variable selection from MF Editor."""
        self._selected_variable = variable_name
        self._selected_variable_is_input = variable_type == "input"
        self.selected_variable_changed.emit(variable_name, self._selected_variable_is_input)
        self._update_membership_functions_plot()
        self.notify_data_changed()

    def _on_mf_list_updated(self) -> None:
        """Handle MF list updates from MF Editor."""
        self._update_membership_functions_plot()
        self.notify_data_changed()

    def _on_mf_added(self) -> None:
        """Handle MF addition from MF Editor."""
        self._update_membership_functions_plot()
        self.notify_data_changed()

    def _on_mf_deleted(self) -> None:
        """Handle MF deletion from MF Editor."""
        self._update_membership_functions_plot()
        self.notify_data_changed()

    def _update_membership_functions_plot(self) -> None:
        """Update the membership functions plot data."""
        if not self._fuzzy_service:
            return

        selected_variable = self._selected_variable
        is_input = self._selected_variable_is_input

        if not selected_variable:
            inputs = self._fuzzy_service.get_input_variables()
            if inputs:
                selected_variable = inputs[0]["name"]
                is_input = True
            else:
                outputs = self._fuzzy_service.get_output_variables()
                if outputs:
                    selected_variable = outputs[0]["name"]
                    is_input = False
                else:
                    return

        mfs = self._fuzzy_service.get_membership_functions(selected_variable, is_input)
        if not mfs:
            return

        if is_input:
            variables = self._fuzzy_service.get_input_variables()
        else:
            variables = self._fuzzy_service.get_output_variables()

        var_info = next((v for v in variables if v["name"] == selected_variable), None)
        if not var_info:
            return

        var_range = var_info["range"]

        import numpy as np

        interpolation_points = self._fuzzy_service.get_interpolation_points()
        x_data = np.linspace(var_range[0], var_range[1], interpolation_points)
        y_data_list = []
        colors = ["r", "g", "b", "m", "c", "y", "k"]

        for i, mf in enumerate(mfs):
            mf_type = mf.get("type", "")
            type_mapping = {
                "trojkatna": "trimf",
                "trapezoidalna": "trapmf",
                "gaussowska": "gaussmf",
                "dzwonowa": "gbellmf",
                "stala": "constant",
                "liniowa": "linear",
            }
            mf_type = type_mapping.get(mf_type, mf_type)

            if mf_type == "trimf":
                params = mf["parameters"]
                if len(params) >= 3:
                    y = self._triangular_mf(x_data, params[0], params[1], params[2])
                else:
                    y = np.zeros_like(x_data)
            elif mf_type == "trapmf":
                params = mf["parameters"]
                if len(params) >= 4:
                    y = self._trapezoidal_mf(x_data, params[0], params[1], params[2], params[3])
                else:
                    y = np.zeros_like(x_data)
            elif mf_type == "gaussmf":
                params = mf["parameters"]
                if len(params) >= 2:
                    y = self._gaussian_mf(x_data, params[0], params[1])
                else:
                    y = np.zeros_like(x_data)
            elif mf_type == "gbellmf":
                params = mf["parameters"]
                if len(params) >= 3:
                    y = self._bell_mf(x_data, params[0], params[1], params[2])
                else:
                    y = np.zeros_like(x_data)
            elif mf_type == "constant":
                params = mf["parameters"]
                if isinstance(params, (int, float)):
                    const_value = float(params)
                elif isinstance(params, (list, tuple)) and len(params) > 0:
                    const_value = float(params[0])
                else:
                    const_value = 0.5
                y = np.full_like(x_data, np.clip(const_value, 0.0, 1.0))
            elif mf_type == "linear":
                params = mf["parameters"]
                if isinstance(params, (list, tuple)) and len(params) > 0:
                    constant_term = float(params[-1])
                else:
                    constant_term = 0.5
                y = np.full_like(x_data, np.clip(constant_term, 0.0, 1.0))
            else:
                y = np.zeros_like(x_data)

            y_data_list.append(y)

        self.membership_functions_data_ready.emit(selected_variable, x_data.tolist(), y_data_list, colors)

    def _triangular_mf(self, x, a, b, c):
        """Triangular membership function."""
        import numpy as np

        y = np.zeros_like(x)
        y[(x >= a) & (x <= b)] = (x[(x >= a) & (x <= b)] - a) / (b - a)
        y[(x > b) & (x <= c)] = (c - x[(x > b) & (x <= c)]) / (c - b)
        return y

    def _trapezoidal_mf(self, x, a, b, c, d):
        """Trapezoidal membership function."""
        import numpy as np

        y = np.zeros_like(x)
        y[(x >= a) & (x < b)] = (x[(x >= a) & (x < b)] - a) / (b - a)
        y[(x >= b) & (x <= c)] = 1.0
        y[(x > c) & (x <= d)] = (d - x[(x > c) & (x <= d)]) / (d - c)
        return y

    def _gaussian_mf(self, x, c, sigma):
        """Gaussian membership function."""
        import numpy as np

        return np.exp(-0.5 * ((x - c) / sigma) ** 2)

    def _bell_mf(self, x, a, b, c):
        """Bell-shaped membership function."""
        import numpy as np

        return 1 / (1 + np.abs((x - c) / a) ** (2 * b))
