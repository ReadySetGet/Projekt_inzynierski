from __future__ import annotations

from typing import Dict, List

import numpy as np

from app.view_models.base_view_model import BaseViewModel


class AreaPlotViewModel(BaseViewModel):
    """View model powering the control surface / area plot window."""

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
            return {
                "error": "system_not_ready",
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

        # Default values for all other inputs (midpoint of their ranges)
        fixed_inputs = dict(fixed_inputs) if fixed_inputs else {}
        default_inputs = []
        for var in inputs:
            var_range = var.get("range", [0, 1])
            name = var.get("name", "")
            if name in fixed_inputs:
                midpoint = float(fixed_inputs[name])
            else:
                midpoint = (var_range[0] + var_range[1]) / 2 if len(var_range) == 2 else 0.0
            default_inputs.append(midpoint)

        success_count = 0
        for yi, y_val in enumerate(y_values):
            for xi, x_val in enumerate(x_values):
                input_vector = default_inputs.copy()
                input_vector[x_idx] = float(x_val)
                input_vector[y_idx] = float(y_val)

                outputs_vector, success = self.fuzzy_service.perform_inference(input_vector)
                if success and output_idx < len(outputs_vector):
                    Z[yi, xi] = outputs_vector[output_idx]
                    success_count += 1
                else:
                    Z[yi, xi] = np.nan

        return {
            "X": X,
            "Y": Y,
            "Z": Z,
            "defaults": default_inputs,
            "success_count": success_count,
            "error": None if success_count > 0 else "no_valid_output",
        }
