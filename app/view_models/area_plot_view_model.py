from __future__ import annotations

from typing import Dict, List

import numpy as np

from app.view_models.base_view_model import BaseViewModel


class AreaPlotViewModel(BaseViewModel):
    """View model powering the control surface / area plot window."""

    def refresh_data(self) -> None:
        """Refresh data when notified by event bus."""
        self.notify_data_changed.emit()

    def get_input_variables(self) -> List[Dict]:
        """Return available input variables."""
        if not self.fuzzy_service:
            return []
        return self.fuzzy_service.get_input_variables()

    def get_output_variables(self) -> List[Dict]:
        """Return available output variables."""
        if not self.fuzzy_service:
            return []
        return self.fuzzy_service.get_output_variables()

    def compute_surface(
        self,
        x_variable: str,
        y_variable: str,
        output_variable: str,
        x_points: int,
        y_points: int,
        fixed_inputs: Dict[str, float] | None = None,
    ) -> Dict | None:
        """Compute the control surface for the selected variables.

        Args:
            x_variable: Name of the first input variable (x-axis).
            y_variable: Name of the second input variable (y-axis).
            output_variable: Name of the output variable (z-axis).
            x_points: Number of sample points for the x-axis.
            y_points: Number of sample points for the y-axis.
            fixed_inputs: Optional mapping of input names to fixed values for
                variables not used on the axes.

        Returns:
            Dictionary containing mesh grids ``X``, ``Y``, surface ``Z`` and
            the default input vector used for the remaining inputs.
        """
        if not self.fuzzy_service:
            return None

        inputs = self.get_input_variables()
        outputs = self.get_output_variables()

        if len(inputs) < 2 or not outputs:
            return None

        input_index_map = {var.get("name", ""): idx for idx, var in enumerate(inputs)}
        output_index_map = {var.get("name", ""): idx for idx, var in enumerate(outputs)}

        if x_variable not in input_index_map or y_variable not in input_index_map:
            return None
        if output_variable not in output_index_map:
            return None

        if not self.fuzzy_service.is_system_ready():
            inputs = self.get_input_variables()
            outputs = self.get_output_variables()
            rule_count = self.fuzzy_service.get_rule_count() if hasattr(self.fuzzy_service, "get_rule_count") else 0

            missing = []
            if len(inputs) == 0:
                missing.append("inputs")
            if len(outputs) == 0:
                missing.append("outputs")
            if rule_count == 0:
                missing.append("rules")

            return {
                "error": "system_not_ready",
                "missing": missing,
            }

        x_idx = input_index_map[x_variable]
        y_idx = input_index_map[y_variable]
        output_idx = output_index_map[output_variable]

        x_var = inputs[x_idx]
        y_var = inputs[y_idx]

        x_range = x_var.get("range", [0, 1])
        y_range = y_var.get("range", [0, 1])

        x_values = np.linspace(x_range[0], x_range[1], max(2, x_points))
        y_values = np.linspace(y_range[0], y_range[1], max(2, y_points))

        X, Y = np.meshgrid(x_values, y_values)
        Z = np.zeros_like(X, dtype=float)

        # Default values for all other inputs (based on MF centers/peaks)
        # For inputs used as axes, we'll overwrite these values anyway
        fixed_inputs = dict(fixed_inputs) if fixed_inputs else {}
        default_inputs = []
        for idx, var in enumerate(inputs):
            var_range = var.get("range", [0, 1])
            name = var.get("name", "")
            if name in fixed_inputs:
                default_value = float(fixed_inputs[name])
            elif idx == x_idx or idx == y_idx:
                default_value = (var_range[0] + var_range[1]) / 2.0 if len(var_range) == 2 else 0.0
            else:
                default_value = self._get_mf_center_value(name, var_range)
            default_inputs.append(default_value)

        success_count = 0
        for yi, y_val in enumerate(y_values):
            for xi, x_val in enumerate(x_values):
                input_vector = default_inputs.copy()
                input_vector[x_idx] = float(x_val)
                input_vector[y_idx] = float(y_val)

                outputs_vector, success = self.fuzzy_service.perform_inference(input_vector)
                if success:
                    if isinstance(outputs_vector, (int, float)):
                        if output_idx == 0:
                            Z[yi, xi] = float(outputs_vector)
                            success_count += 1
                        else:
                            Z[yi, xi] = np.nan
                    elif isinstance(outputs_vector, (list, tuple)) and output_idx < len(outputs_vector):
                        Z[yi, xi] = float(outputs_vector[output_idx])
                        success_count += 1
                    else:
                        Z[yi, xi] = np.nan
                else:
                    Z[yi, xi] = np.nan

        z_min = np.nanmin(Z) if success_count > 0 else np.nan
        z_max = np.nanmax(Z) if success_count > 0 else np.nan

        return {
            "X": X,
            "Y": Y,
            "Z": Z,
            "defaults": default_inputs,
            "success_count": success_count,
            "z_min": z_min,
            "z_max": z_max,
            "error": None if success_count > 0 else "no_valid_output",
        }

    def _get_mf_center_value(self, variable_name: str, var_range: List[float]) -> float:
        """Get a meaningful default value for a variable based on its MFs.

        Uses the center/peak of the first MF, or falls back to range midpoint.

        Args:
            variable_name: Name of the variable.
            var_range: Range of the variable [min, max].

        Returns:
            Default value based on MF center, or range midpoint if no MFs.
        """
        if not self.fuzzy_service:
            return (var_range[0] + var_range[1]) / 2 if len(var_range) == 2 else 0.0

        mfs = self.fuzzy_service.get_membership_functions(variable_name, "input")
        if not mfs or len(mfs) == 0:
            return (var_range[0] + var_range[1]) / 2 if len(var_range) == 2 else 0.0

        mf = mfs[0]
        mf_type = mf.get("type", "")
        params = mf.get("parameters", [])

        if not params:
            return (var_range[0] + var_range[1]) / 2 if len(var_range) == 2 else 0.0

        var_min, var_max = var_range[0], var_range[1] if len(var_range) >= 2 else (0.0, 1.0)
        range_size = var_max - var_min

        if mf_type == "trimf" and len(params) >= 3:
            center = float(params[1])
            param_min, param_max = min(params), max(params)
            if param_min >= var_min and param_max <= var_max:
                return center
            elif param_min >= 0.0 and param_max <= 1.0 and range_size > 0:
                center = var_min + center * range_size
            elif center < var_min or center > var_max:
                center = (var_min + var_max) / 2.0
            return center
        elif mf_type == "trapmf" and len(params) >= 4:
            center = (float(params[1]) + float(params[2])) / 2.0
            param_min, param_max = min(params), max(params)
            if param_min >= var_min and param_max <= var_max:
                return center
            elif param_min >= 0.0 and param_max <= 1.0 and range_size > 0:
                center = var_min + center * range_size
            elif center < var_min or center > var_max:
                center = (var_min + var_max) / 2.0
            return center
        elif mf_type == "gaussmf" and len(params) >= 2:
            center = float(params[0])
            if center >= var_min and center <= var_max:
                return center
            elif center >= 0.0 and center <= 1.0 and range_size > 0:
                center = var_min + center * range_size
            elif center < var_min or center > var_max:
                center = (var_min + var_max) / 2.0
            return center
        elif mf_type == "gbellmf" and len(params) >= 3:
            center = float(params[2])
            if center >= var_min and center <= var_max:
                return center
            elif center >= 0.0 and center <= 1.0 and range_size > 0:
                center = var_min + center * range_size
            elif center < var_min or center > var_max:
                center = (var_min + var_max) / 2.0
            return center
        else:
            return (var_range[0] + var_range[1]) / 2 if len(var_range) == 2 else 0.0
