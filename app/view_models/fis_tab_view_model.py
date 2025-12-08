"""View model for the FIS plot tab."""

from typing import Dict, List, Tuple

from PyQt6.QtCore import pyqtSignal

from app.view_models.base_view_model import BaseViewModel


class FisTabViewModel(BaseViewModel):
    """View model for the FIS plot tab."""

    fis_data_updated = pyqtSignal(dict)

    def __init__(self) -> None:
        """Initialize the FisTabViewModel."""
        super().__init__()
        self._inputs = self.fuzzy_service.get_input_variables()
        self._outputs = self.fuzzy_service.get_output_variables()
        self._system_info = self.fuzzy_service.get_system_status()
        self.notify_data_changed.connect(self.refresh_data)

    @property
    def inputs(self) -> List[Dict]:
        """Get the inputs list."""
        return self._inputs

    @property
    def outputs(self) -> List[Dict]:
        """Get the outputs list."""
        return self._outputs

    def refresh_data(self) -> None:
        """Refresh all data from the fuzzy service."""
        self._update_fis_data()

    def _update_fis_data(self) -> None:
        """Update FIS data from the fuzzy service."""
        system_status = self.fuzzy_service.get_system_status()
        self._system_info = {
            "name": "FIS System",
            "type": system_status.get("fis_type", "mamdani"),
            "has_inputs": system_status.get("has_inputs", False),
            "has_outputs": system_status.get("has_outputs", False),
            "has_rules": system_status.get("has_rules", False),
            "is_ready": system_status.get("is_ready", False),
            "inference_state": system_status.get("inference_state", "idle"),
        }

        self._inputs = self._get_variables_data("input")

        self._outputs = self._get_variables_data("output")

        fis_data = {
            "system_info": self._system_info,
            "inputs": self._inputs,
            "outputs": self._outputs,
        }
        self.fis_data_updated.emit(fis_data)

    def _get_variables_data(self, variable_type: str) -> List[Dict]:
        """Get data for input or output variables."""
        variables = []

        if variable_type == "input":
            var_list = self.fuzzy_service.get_input_variables()
        else:
            var_list = self.fuzzy_service.get_output_variables()

        for var in var_list:
            var_data = {
                "name": var.get("name", ""),
                "range": var.get("range", [0, 100]),
                "membership_functions": self._get_membership_functions_data(var.get("name", ""), variable_type),
            }
            variables.append(var_data)

        return variables

    def _get_membership_functions_data(self, variable_name: str, variable_type: str) -> List[Dict]:
        """Get membership functions data for a specific variable."""
        mfs = self.fuzzy_service.get_membership_functions(variable_name, variable_type)

        var_range = [0, 100]
        if variable_type == "input":
            inputs = self.fuzzy_service.get_input_variables()
            for var in inputs:
                if var.get("name") == variable_name:
                    var_range = var.get("range", [0, 100])
                    break
        else:
            outputs = self.fuzzy_service.get_output_variables()
            for var in outputs:
                if var.get("name") == variable_name:
                    var_range = var.get("range", [0, 100])
                    break

        mf_data = []
        for i, mf in enumerate(mfs):
            plot_data = self._generate_plot_data(mf, var_range)
            mf_info = {
                "name": mf.get("name", ""),
                "type": mf.get("type", ""),
                "parameters": mf.get("parameters", []),
                "range": var_range,
                "plot_data": plot_data,
            }
            mf_data.append(mf_info)

        return mf_data

    def _generate_plot_data(self, mf: Dict, var_range: List[float]) -> Tuple[List[float], List[float]]:
        """Generate x, y data for plotting membership function."""
        mf_type = mf.get("type", "")
        parameters = mf.get("parameters", [])

        x_min, x_max = var_range
        interpolation_points = self.fuzzy_service.get_interpolation_points()
        x = [x_min + i * (x_max - x_min) / (interpolation_points - 1) for i in range(interpolation_points)]

        y = self._calculate_membership_values(x, mf_type, parameters)

        return x, y

    def _calculate_membership_values(self, x: List[float], mf_type: str, parameters: List[float]) -> List[float]:
        """Calculate membership values for given x values."""
        import numpy as np

        type_mapping = {
            "trojkatna": "trimf",
            "trapezoidalna": "trapmf",
            "gaussowska": "gaussmf",
            "dzwonowa": "gbellmf",
            "stala": "constant",
            "liniowa": "linear",
        }

        mf_type = type_mapping.get(mf_type, mf_type)

        x = np.array(x)
        y = np.zeros_like(x)

        if mf_type == "trimf" and len(parameters) >= 3:
            a, b, c = parameters[0], parameters[1], parameters[2]

            if max(parameters) <= 1.0 and min(parameters) >= 0.0:
                x_min, x_max = min(x), max(x)
                a = x_min + a * (x_max - x_min)
                b = x_min + b * (x_max - x_min)
                c = x_min + c * (x_max - x_min)

            if abs(b - a) > 1e-10:
                y[(x >= a) & (x <= b)] = (x[(x >= a) & (x <= b)] - a) / (b - a)
            else:
                y[(x >= a) & (x <= b)] = 1.0 if b == a else 0.0

            if abs(c - b) > 1e-10:
                y[(x > b) & (x <= c)] = (c - x[(x > b) & (x <= c)]) / (c - b)
            else:
                y[(x > b) & (x <= c)] = 1.0 if c == b else 0.0

        elif mf_type == "trapmf" and len(parameters) >= 4:
            a, b, c, d = parameters[0], parameters[1], parameters[2], parameters[3]

            if max(parameters) <= 1.0 and min(parameters) >= 0.0:
                x_min, x_max = min(x), max(x)
                a = x_min + a * (x_max - x_min)
                b = x_min + b * (x_max - x_min)
                c = x_min + c * (x_max - x_min)
                d = x_min + d * (x_max - x_min)

            y[(x >= a) & (x < b)] = (x[(x >= a) & (x < b)] - a) / (b - a)
            y[(x >= b) & (x <= c)] = 1.0
            y[(x > c) & (x <= d)] = (d - x[(x > c) & (x <= d)]) / (d - c)

        elif mf_type == "gaussmf" and len(parameters) >= 2:
            sigma, c = parameters[0], parameters[1]

            if c <= 1.0 and c >= 0.0:
                x_min, x_max = min(x), max(x)
                c = x_min + c * (x_max - x_min)
                sigma = sigma * (x_max - x_min)

            y = np.exp(-((x - c) ** 2) / (2 * sigma**2))

        elif mf_type == "gbellmf" and len(parameters) >= 3:
            a, b, c = parameters[0], parameters[1], parameters[2]

            if c <= 1.0 and c >= 0.0:
                x_min, x_max = min(x), max(x)
                c = x_min + c * (x_max - x_min)
                a = a * (x_max - x_min)

            y = 1 / (1 + ((x - c) / a) ** (2 * b))

        elif mf_type == "sigmf" and len(parameters) >= 2:
            a, c = parameters[0], parameters[1]

            if c <= 1.0 and c >= 0.0:
                x_min, x_max = min(x), max(x)
                c = x_min + c * (x_max - x_min)
                a = a / (x_max - x_min)

            y = 1 / (1 + np.exp(-a * (x - c)))

        elif mf_type == "constant":
            if isinstance(parameters, (int, float)):
                const_value = float(parameters)
            elif isinstance(parameters, (list, tuple)) and len(parameters) > 0:
                const_value = float(parameters[0])
            else:
                const_value = 0.5
            y = np.full_like(x, np.clip(const_value, 0.0, 1.0))

        elif mf_type == "linear":
            if isinstance(parameters, (list, tuple)) and len(parameters) > 0:
                constant_term = float(parameters[-1])
            else:
                constant_term = 0.5
            y = np.full_like(x, np.clip(constant_term, 0.0, 1.0))

        return y.tolist()

    def get_system_display_name(self) -> str:
        """Get the display name for the system."""
        system_type = self._system_info.get("type", "mamdani")
        system_type_capitalized = system_type.capitalize() if system_type else "Mamdani"
        return f"{system_type_capitalized} Type 1"

    def get_variable_display_name(self, var_data: Dict) -> str:
        """Get display name for a variable."""
        name = var_data.get("name", "Unknown")
        mf_count = len(var_data.get("membership_functions", []))
        return f"{name} ({mf_count} MFs)"
