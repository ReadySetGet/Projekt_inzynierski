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
            rule_count = self.fuzzy_service.get_rule_count()

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

        if len(x_range) < 2:
            x_range = [0.0, 1.0]
        if len(y_range) < 2:
            y_range = [0.0, 1.0]

        x_min, x_max = float(x_range[0]), float(x_range[1])
        y_min, y_max = float(y_range[0]), float(y_range[1])

        if x_min >= x_max:
            x_max = x_min + 1.0
        if y_min >= y_max:
            y_max = y_min + 1.0

        x_points = max(2, min(200, int(x_points)))
        y_points = max(2, min(200, int(y_points)))

        x_values = np.linspace(x_min, x_max, x_points)
        y_values = np.linspace(y_min, y_max, y_points)

        X, Y = np.meshgrid(x_values, y_values)
        Z = np.full_like(X, np.nan, dtype=float)

        fixed_inputs = dict(fixed_inputs) if fixed_inputs else {}
        default_inputs = []
        for idx, var in enumerate(inputs):
            var_range = var.get("range", [0, 1])
            name = var.get("name", "")
            if name in fixed_inputs:
                default_value = float(fixed_inputs[name])
            elif idx == x_idx or idx == y_idx:
                default_value = (var_range[0] + var_range[1]) / 2.0 if len(var_range) >= 2 else 0.0
            else:
                default_value = self._get_mf_center_value(name, var_range)
            default_inputs.append(float(default_value))

        success_count = 0
        nan_count = 0
        inf_count = 0

        for yi, y_val in enumerate(y_values):
            for xi, x_val in enumerate(x_values):
                input_vector = default_inputs.copy()
                input_vector[x_idx] = float(x_val)
                input_vector[y_idx] = float(y_val)

                try:
                    outputs_vector, success = self.fuzzy_service.perform_inference(input_vector)
                    if success:
                        if isinstance(outputs_vector, (int, float)):
                            if output_idx == 0:
                                z_val = float(outputs_vector)
                                if np.isnan(z_val):
                                    nan_count += 1
                                elif np.isinf(z_val):
                                    inf_count += 1
                                else:
                                    Z[yi, xi] = z_val
                                    success_count += 1
                            else:
                                nan_count += 1
                        elif isinstance(outputs_vector, (list, tuple)) and output_idx < len(outputs_vector):
                            z_val = float(outputs_vector[output_idx])
                            if np.isnan(z_val):
                                nan_count += 1
                            elif np.isinf(z_val):
                                inf_count += 1
                            else:
                                Z[yi, xi] = z_val
                                success_count += 1
                        else:
                            nan_count += 1
                    else:
                        nan_count += 1
                except Exception:
                    nan_count += 1

        if success_count == 0:
            return {
                "X": X,
                "Y": Y,
                "Z": Z,
                "defaults": default_inputs,
                "success_count": 0,
                "z_min": np.nan,
                "z_max": np.nan,
                "error": "no_valid_output",
            }

        valid_Z = Z[~np.isnan(Z) & ~np.isinf(Z)]
        if len(valid_Z) == 0:
            return {
                "X": X,
                "Y": Y,
                "Z": Z,
                "defaults": default_inputs,
                "success_count": 0,
                "z_min": np.nan,
                "z_max": np.nan,
                "error": "no_valid_output",
            }

        z_min = float(np.nanmin(valid_Z))
        z_max = float(np.nanmax(valid_Z))

        if z_min == z_max or abs(z_max - z_min) < 1e-10:
            if not np.isnan(z_min) and not np.isinf(z_min):
                output_var_info = next((var for var in outputs if var.get("name") == output_variable), None)
                output_range = output_var_info.get("range", [0, 1]) if output_var_info else [0, 1]
                output_range_size = abs(output_range[1] - output_range[0]) if len(output_range) >= 2 else 1.0
                offset = max(output_range_size * 0.05, 0.1)
                z_min = z_min - offset
                z_max = z_max + offset
            else:
                output_var_info = next((var for var in outputs if var.get("name") == output_variable), None)
                output_range = output_var_info.get("range", [0, 1]) if output_var_info else [0, 1]
                if len(output_range) >= 2:
                    z_min = float(output_range[0])
                    z_max = float(output_range[1])
                    if z_min == z_max:
                        z_min -= 0.1
                        z_max += 0.1
                else:
                    z_min = z_min - 0.1 if not np.isnan(z_min) else -0.1
                    z_max = z_max + 0.1 if not np.isnan(z_max) else 0.1
        else:
            range_size = abs(z_max - z_min)
            padding = max(range_size * 0.05, 1e-6)
            z_min = z_min - padding
            z_max = z_max + padding

        return {
            "X": X,
            "Y": Y,
            "Z": Z,
            "defaults": default_inputs,
            "success_count": success_count,
            "z_min": z_min,
            "z_max": z_max,
            "error": None,
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
            return (var_range[0] + var_range[1]) / 2 if len(var_range) >= 2 else 0.0

        mfs = self.fuzzy_service.get_membership_functions(variable_name, "input")
        if not mfs or len(mfs) == 0:
            return (var_range[0] + var_range[1]) / 2 if len(var_range) >= 2 else 0.0

        mf = mfs[0]
        mf_type = mf.get("type", "")
        params = mf.get("parameters", [])

        if not params:
            return (var_range[0] + var_range[1]) / 2 if len(var_range) >= 2 else 0.0

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
            center = float(params[1])
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
            return (var_range[0] + var_range[1]) / 2 if len(var_range) >= 2 else 0.0
