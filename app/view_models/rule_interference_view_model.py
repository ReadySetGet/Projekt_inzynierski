from __future__ import annotations

from typing import Any, Dict, List, Sequence, Tuple

import numpy as np
from PyQt6.QtCore import pyqtSignal

from app.view_models.base_view_model import BaseViewModel


class RuleInterferenceViewModel(BaseViewModel):
    """View model that exposes rule interference data sourced from the fuzzy service."""

    inputs_updated = pyqtSignal(list)
    outputs_updated = pyqtSignal(list)
    rules_updated = pyqtSignal(list)
    inference_updated = pyqtSignal(list, list)  # inputs, outputs
    status_message = pyqtSignal(str)

    def __init__(self) -> None:
        """Initialize the rule interference view model."""
        super().__init__()
        self._inputs: List[Dict] = []
        self._outputs: List[Dict] = []
        self._rules: List[Dict] = []
        self._current_inputs: List[float] = []
        self._current_outputs: List[float] = []
        self._curve_cache: Dict[
            Tuple[str, Tuple[float, ...], Tuple[float, float], int],
            Tuple[List[float], List[float]],
        ] = {}
        self._last_rules_hash: int = 0
        self._connect_to_fuzzy_service()

    # ---------------------------------------------------------------------- #
    # Public API                                                             #
    # ---------------------------------------------------------------------- #
    @property
    def current_input_values(self) -> List[float]:
        """Return a copy of the current input values used for inference."""
        return list(self._current_inputs)

    @property
    def current_output_values(self) -> List[float]:
        """Return a copy of the latest inference results."""
        return list(self._current_outputs)

    @property
    def inputs(self) -> List[Dict]:
        """Return cached input variable descriptions."""
        return list(self._inputs)

    @property
    def outputs(self) -> List[Dict]:
        """Return cached output variable descriptions."""
        return list(self._outputs)

    @property
    def rules(self) -> List[Dict]:
        """Return cached rule descriptions."""
        return list(self._rules)

    def get_first_rule(self) -> Dict | None:
        """Return the first rule or None when no rules exist."""
        return self._rules[0] if self._rules else None

    def refresh_data(self) -> None:
        """Reload inputs, outputs, rules, and the latest inference result."""
        fuzzy_service = self.fuzzy_service

        if not fuzzy_service:
            self._reset_cache()
            self._emit_all()
            return

        self._curve_cache.clear()
        self._last_rules_hash = 0

        self._inputs = fuzzy_service.get_input_variables()
        self._outputs = fuzzy_service.get_output_variables()
        self._rules = fuzzy_service.get_rules()

        if len(self._current_inputs) != len(self._inputs):
            self._current_inputs = [self._default_value_for_input(var) for var in self._inputs]

        self._update_inference_results(run_inference=fuzzy_service.is_system_ready())
        self._emit_all()

    def update_data(self) -> None:
        """Dynamically update cached data when requested by the view."""
        self.refresh_data()

    def set_input_values(self, new_values: List[float]) -> bool:
        """Validate and persist new input values, triggering a fresh inference."""
        fuzzy_service = self.fuzzy_service

        if not fuzzy_service or not self._inputs:
            self._emit_status("Fuzzy service is not ready.")
            return False

        if len(new_values) != len(self._inputs):
            self._emit_status("Incorrect number of input values provided.")
            return False

        is_valid, error = fuzzy_service.validate_inputs(new_values)
        if not is_valid:
            self._emit_status(error or "Provided inputs are not valid.")
            return False

        self._current_inputs = list(new_values)
        self._update_inference_results(run_inference=True)
        self._emit_inference()
        return bool(self._current_outputs)

    # ------------------------------------------------------------------ #
    # Internal helpers                                                   #
    # ------------------------------------------------------------------ #
    def _connect_to_fuzzy_service(self) -> None:
        """Attach listeners to fuzzy service change notifications."""
        try:
            fuzzy_service = self.fuzzy_service
        except RuntimeError:
            fuzzy_service = None

        if fuzzy_service and hasattr(fuzzy_service, "system_changed"):
            fuzzy_service.system_changed.connect(self._on_system_changed)

    def _on_system_changed(self) -> None:
        """Handle incoming system change notifications."""
        self._curve_cache.clear()
        self._last_rules_hash = 0
        self.refresh_data()

    def _reset_cache(self) -> None:
        """Reset all cached data."""
        self._inputs = []
        self._outputs = []
        self._rules = []
        self._current_inputs = []
        self._current_outputs = []
        self._curve_cache.clear()
        self._last_rules_hash = 0

    def _default_value_for_input(self, variable: Dict) -> float:
        """Return a sensible default value within the variable range."""
        var_range = variable.get("range", [0, 1])
        if not isinstance(var_range, (list, tuple)) or len(var_range) != 2:
            return 0.5
        range_min, range_max = var_range
        try:
            range_min = float(range_min)
            range_max = float(range_max)
        except (TypeError, ValueError):
            return 0.5
        return (range_min + range_max) / 2 if range_max >= range_min else range_min

    def _update_inference_results(self, run_inference: bool) -> None:
        """Execute inference if requested and cache the latest results."""
        fuzzy_service = self.fuzzy_service
        if not fuzzy_service or not run_inference or not self._current_inputs:
            self._current_outputs = []
            return

        outputs, success = fuzzy_service.perform_inference(self._current_inputs)
        if success:
            self._current_outputs = self._normalize_outputs(outputs)
        else:
            self._current_outputs = []
            self._emit_status("Inference failed to execute.")

    def _emit_all(self) -> None:
        """Emit the cached data through the view model signals."""
        self.inputs_updated.emit(self.inputs)
        self.outputs_updated.emit(self.outputs)
        self.rules_updated.emit(self.rules)
        self._emit_inference()

    def _emit_inference(self) -> None:
        """Emit current inference data."""
        self.inference_updated.emit(
            self.current_input_values,
            self.current_output_values,
        )

    def _emit_status(self, message: str) -> None:
        """Emit a status message to the bound view if available."""
        if message:
            self.status_message.emit(message)

    def _normalize_outputs(self, outputs) -> List[float]:
        """Convert inference result into a flat list of floats."""
        if outputs is None:
            return []

        # Handle numpy arrays/scalars via tolist()
        if hasattr(outputs, "tolist"):
            converted = outputs.tolist()
            # Recursively normalise in case tolist() returned a scalar
            return self._normalize_outputs(converted)

        if isinstance(outputs, (list, tuple)):
            flattened: List[float] = []
            for value in outputs:
                flattened.extend(self._normalize_outputs(value))
            return flattened

        try:
            return [float(outputs)]
        except (TypeError, ValueError):
            return []

    def get_rule_text(self, rule_index: int) -> str:
        """Fetch human-readable rule text from the fuzzy service."""
        if not self.fuzzy_service:
            return ""
        try:
            return self.fuzzy_service.get_rule_text(rule_index)
        except Exception:
            return ""

    # ------------------------------------------------------------------ #
    # Visualization Helpers                                              #
    # ------------------------------------------------------------------ #
    def build_visualization_payload(self) -> Dict[str, Any]:
        """Build structured data used to render the rule interference view."""
        mf_data_hash = self._compute_mf_data_hash_from_variables()
        rules_hash = hash(
            tuple(
                (
                    r.get("index", 0),
                    r.get("name", ""),
                    tuple(r.get("antecedent", [])),
                    tuple(r.get("consequent", [])),
                    r.get("connection", 1),
                    r.get("weight", 1.0),
                    tuple(r.get("is_mf", [])),
                )
                for r in self._rules
            )
        )
        combined_hash = hash((rules_hash, mf_data_hash))

        if combined_hash != self._last_rules_hash:
            self._curve_cache.clear()
            self._last_rules_hash = combined_hash

        inputs_payload = self._build_inputs_payload()
        outputs_payload = self._build_outputs_payload()

        aggregated_curves: Dict[int, Dict[str, List[float]]] = {}
        rules_payload = []

        for rule in self._rules:
            rule_index = rule.get("index", 0)
            antecedent = rule.get("antecedent", [])
            consequent = rule.get("consequent", [])
            connection = rule.get("connection", 1)
            weight = float(rule.get("weight", 1.0))
            is_mf_flags = rule.get("is_mf", [])

            input_flags = is_mf_flags[: len(inputs_payload)] if is_mf_flags else []
            output_flags = is_mf_flags[len(inputs_payload) :] if is_mf_flags else []

            input_conditions = self._build_input_conditions(antecedent, inputs_payload, input_flags)
            activation = self._compute_activation(input_conditions, connection, weight)
            output_conditions = self._build_output_conditions(
                consequent,
                outputs_payload,
                activation,
                output_flags,
                aggregated_curves,
            )

            rule_text = self.get_rule_text(rule_index)
            display_text = rule_text or rule.get("name") or f"Rule {rule_index + 1}"

            rules_payload.append(
                {
                    "index": rule_index,
                    "display": display_text,
                    "connection_label": "AND (min)" if connection == 1 else "OR (max)",
                    "activation": activation,
                    "inputs": input_conditions,
                    "outputs": output_conditions,
                }
            )

        aggregated_outputs = self._build_aggregated_outputs(outputs_payload, aggregated_curves)

        return {
            "inputs": inputs_payload,
            "rules": rules_payload,
            "outputs": aggregated_outputs,
        }

    def _build_inputs_payload(self) -> List[Dict[str, Any]]:
        payload = []
        for idx, variable in enumerate(self._inputs):
            payload.append(
                {
                    "name": variable.get("name", f"Input {idx + 1}"),
                    "range": variable.get("range", [0, 1]),
                    "value": self._current_inputs[idx] if idx < len(self._current_inputs) else None,
                    "membership_functions": variable.get("membership_functions", []),
                }
            )
        return payload

    def _build_outputs_payload(self) -> List[Dict[str, Any]]:
        payload = []
        for idx, variable in enumerate(self._outputs):
            payload.append(
                {
                    "name": variable.get("name", f"Output {idx + 1}"),
                    "range": variable.get("range", [0, 1]),
                    "value": self._current_outputs[idx] if idx < len(self._current_outputs) else None,
                    "membership_functions": variable.get("membership_functions", []),
                }
            )
        return payload

    def _build_input_conditions(
        self,
        antecedent: Sequence[int],
        inputs_payload: List[Dict[str, Any]],
        input_flags: Sequence[int],
    ) -> List[Dict[str, Any]]:
        conditions = []
        for idx, mf_idx in enumerate(antecedent):
            if mf_idx <= 0 or idx >= len(inputs_payload):
                continue

            variable_info = inputs_payload[idx]
            mfs = variable_info.get("membership_functions", [])
            if not (0 < mf_idx <= len(mfs)):
                continue

            mf = mfs[mf_idx - 1]
            var_range = variable_info.get("range", [0, 1])
            curve_x, curve_y = self._generate_curve(mf.get("type", ""), mf.get("parameters", []), var_range)
            input_value = variable_info.get("value")
            membership = self._evaluate_membership(mf.get("type", ""), mf.get("parameters", []), input_value)

            is_not = False
            if input_flags and idx < len(input_flags):
                is_not = input_flags[idx] != 1
                if is_not:
                    membership = 1.0 - membership

            conditions.append(
                {
                    "variable_index": idx,
                    "variable_name": variable_info.get("name"),
                    "mf_name": mf.get("name", ""),
                    "curve_x": curve_x,
                    "curve_y": curve_y,
                    "value": input_value,
                    "membership": float(np.clip(membership, 0.0, 1.0)),
                    "is_not": is_not,
                }
            )
        return conditions

    def _compute_activation(
        self,
        input_conditions: List[Dict[str, Any]],
        connection: int,
        weight: float,
    ) -> float:
        if not input_conditions:
            return 0.0

        degrees = [cond["membership"] for cond in input_conditions]
        if connection == 1:  # AND
            activation = min(degrees)
        else:  # OR
            activation = max(degrees)
        activation *= weight
        return float(np.clip(activation, 0.0, 1.0))

    def _build_output_conditions(
        self,
        consequent: Sequence[int],
        outputs_payload: List[Dict[str, Any]],
        activation: float,
        output_flags: Sequence[int],
        aggregated_curves: Dict[int, Dict[str, List[float]]],
    ) -> List[Dict[str, Any]]:
        conditions = []
        for idx, mf_idx in enumerate(consequent):
            if mf_idx <= 0 or idx >= len(outputs_payload):
                continue

            variable_info = outputs_payload[idx]
            mfs = variable_info.get("membership_functions", [])
            if not (0 < mf_idx <= len(mfs)):
                continue

            mf = mfs[mf_idx - 1]
            var_range = variable_info.get("range", [0, 1])
            curve_x, curve_y = self._generate_curve(mf.get("type", ""), mf.get("parameters", []), var_range)
            clipped_y = [min(y, activation) for y in curve_y]

            # Update aggregated curve for this output
            if idx not in aggregated_curves:
                aggregated_curves[idx] = {"curve_x": curve_x, "curve_y": clipped_y.copy()}
            else:
                existing = aggregated_curves[idx]
                if len(existing["curve_y"]) == len(clipped_y):
                    existing["curve_y"] = [max(old, new) for old, new in zip(existing["curve_y"], clipped_y)]

            conditions.append(
                {
                    "variable_index": idx,
                    "variable_name": variable_info.get("name"),
                    "mf_name": mf.get("name", ""),
                    "curve_x": curve_x,
                    "curve_y": curve_y,
                    "clipped_curve_y": clipped_y,
                    "activation": activation,
                }
            )
        return conditions

    def _build_aggregated_outputs(
        self,
        outputs_payload: List[Dict[str, Any]],
        aggregated_curves: Dict[int, Dict[str, List[float]]],
    ) -> List[Dict[str, Any]]:
        aggregated_outputs = []
        for idx, variable in enumerate(outputs_payload):
            aggregated = aggregated_curves.get(idx, {"curve_x": [], "curve_y": []})
            aggregated_outputs.append(
                {
                    "variable_index": idx,
                    "variable_name": variable.get("name"),
                    "curve_x": aggregated.get("curve_x", []),
                    "curve_y": aggregated.get("curve_y", []),
                    "value": variable.get("value"),
                }
            )
        return aggregated_outputs

    def _generate_curve(
        self,
        mf_type: str,
        params: Sequence[float],
        var_range: Sequence[float],
        resolution: int = None,
    ) -> Tuple[List[float], List[float]]:
        try:
            range_min, range_max = float(var_range[0]), float(var_range[1])
        except Exception:
            range_min, range_max = 0.0, 1.0

        if range_max <= range_min:
            range_max = range_min + 1.0

        if resolution is None:
            resolution = self.fuzzy_service.get_interpolation_points()

        # Handle constant type - parameters might be a single float
        if mf_type.lower() == "constant":
            if isinstance(params, (int, float)):
                params_tuple = (float(params),)
            elif isinstance(params, (list, tuple)) and len(params) > 0:
                params_tuple = (float(params[0]),)
            else:
                params_tuple = (0.5,)
        else:
            params_tuple = tuple(float(p) for p in params)
        cache_key = (mf_type.lower(), params_tuple, (range_min, range_max), resolution)

        if cache_key in self._curve_cache:
            return self._curve_cache[cache_key]

        x_values = np.linspace(range_min, range_max, resolution)
        y_values = np.zeros_like(x_values, dtype=float)

        mf_type = mf_type.lower()
        if mf_type == "trimf" and len(params) >= 3:
            a, b, c = params[0], params[1], params[2]
            mask_left = x_values <= a
            mask_right = x_values >= c
            mask_peak = x_values == b
            mask_rising = (x_values > a) & (x_values < b)
            mask_falling = (x_values > b) & (x_values < c)

            y_values[mask_left] = 0.0
            y_values[mask_right] = 0.0
            y_values[mask_peak] = 1.0

            denom_rising = b - a if b != a else 1e-9
            y_values[mask_rising] = (x_values[mask_rising] - a) / denom_rising

            denom_falling = c - b if c != b else 1e-9
            y_values[mask_falling] = (c - x_values[mask_falling]) / denom_falling

        elif mf_type == "trapmf" and len(params) >= 4:
            a, b, c, d = params[0], params[1], params[2], params[3]
            mask_left = x_values <= a
            mask_right = x_values >= d
            mask_plateau = (x_values >= b) & (x_values <= c)
            mask_rising = (x_values > a) & (x_values < b)
            mask_falling = (x_values > c) & (x_values < d)

            y_values[mask_left] = 0.0
            y_values[mask_right] = 0.0
            y_values[mask_plateau] = 1.0

            denom_rising = b - a if b != a else 1e-9
            y_values[mask_rising] = (x_values[mask_rising] - a) / denom_rising

            denom_falling = d - c if d != c else 1e-9
            y_values[mask_falling] = (d - x_values[mask_falling]) / denom_falling

        elif mf_type == "gaussmf" and len(params) >= 2:
            sigma = params[0] if params[0] != 0 else 1e-9
            mu = params[1]
            y_values = np.exp(-0.5 * ((x_values - mu) / sigma) ** 2)

        elif mf_type == "gbellmf" and len(params) >= 3:
            a = params[0] if params[0] != 0 else 1e-9
            b = params[1]
            c = params[2]
            y_values = 1.0 / (1 + np.abs((x_values - c) / a) ** (2 * b))

        elif mf_type == "constant":
            # Sugeno constant type - single value, flat line
            if isinstance(params, (int, float)):
                const_value = float(params)
            elif isinstance(params, (list, tuple)) and len(params) > 0:
                const_value = float(params[0])
            else:
                const_value = 0.5
            # For visualization, show as a flat line at the constant value (clipped to [0,1])
            y_values.fill(float(np.clip(const_value, 0.0, 1.0)))

        elif mf_type == "linear":
            # Sugeno linear type - linear function of inputs
            # For visualization purposes, show as a line from min to max of range
            # In actual Sugeno inference, this would use: p0*x1 + p1*x2 + ... + pn
            if isinstance(params, (list, tuple)) and len(params) > 0:
                # Use first parameter as baseline for visualization
                base_value = float(params[0]) if len(params) > 0 else 0.5
                # Create a simple linear visualization
                y_values = np.linspace(base_value * 0.5, base_value * 1.5, len(x_values))
            else:
                y_values.fill(0.5)
            y_values = np.clip(y_values, 0.0, 1.0)

        elif params:
            y_values.fill(float(params[0]))

        y_values = np.clip(y_values, 0.0, 1.0)
        result = (x_values.tolist(), y_values.tolist())
        self._curve_cache[cache_key] = result
        return result

    def _evaluate_membership(
        self,
        mf_type: str,
        params: Sequence[float],
        value: float | None,
    ) -> float:
        if value is None:
            return 0.0

        mf_type = mf_type.lower()
        try:
            if mf_type == "trimf" and len(params) >= 3:
                a, b, c = params[0], params[1], params[2]
                if value <= a or value >= c:
                    return 0.0
                if a < value < b:
                    denom = b - a if b != a else 1e-9
                    return (value - a) / denom
                if b < value < c:
                    denom = c - b if c != b else 1e-9
                    return (c - value) / denom
                return 1.0

            if mf_type == "trapmf" and len(params) >= 4:
                a, b, c, d = params[0], params[1], params[2], params[3]
                if value <= a or value >= d:
                    return 0.0
                if a < value < b:
                    denom = b - a if b != a else 1e-9
                    return (value - a) / denom
                if b <= value <= c:
                    return 1.0
                if c < value < d:
                    denom = d - c if d != c else 1e-9
                    return (d - value) / denom
                return 0.0

            if mf_type == "gaussmf" and len(params) >= 2:
                sigma = params[0] if params[0] != 0 else 1e-9
                mu = params[1]
                return float(np.exp(-0.5 * ((value - mu) / sigma) ** 2))

            if mf_type == "gbellmf" and len(params) >= 3:
                a = params[0] if params[0] != 0 else 1e-9
                b = params[1]
                c = params[2]
                return float(1.0 / (1 + abs((value - c) / a) ** (2 * b)))

            if mf_type == "constant":
                # Sugeno constant type - always returns the constant value (clipped to [0,1])
                if isinstance(params, (int, float)):
                    return float(np.clip(params, 0.0, 1.0))
                elif isinstance(params, (list, tuple)) and len(params) > 0:
                    return float(np.clip(params[0], 0.0, 1.0))
                return 0.5

            if mf_type == "linear":
                # Sugeno linear type - for visualization, use first parameter
                # In actual inference, this would be: p0*x1 + p1*x2 + ... + pn
                if isinstance(params, (list, tuple)) and len(params) > 0:
                    return float(np.clip(params[0], 0.0, 1.0))
                return 0.5

            if params:
                return float(params[0])

        except Exception:
            return 0.0

        return 0.0

    def _compute_mf_data_hash_from_variables(self) -> int:
        """Compute a hash of MF data from current variables to detect changes."""
        mf_data = []
        for var in self._inputs:
            for mf in var.get("membership_functions", []):
                mf_data.append(
                    (
                        mf.get("type", ""),
                        tuple(mf.get("parameters", [])),
                    )
                )
        for var in self._outputs:
            for mf in var.get("membership_functions", []):
                mf_data.append(
                    (
                        mf.get("type", ""),
                        tuple(mf.get("parameters", [])),
                    )
                )
        return hash(tuple(mf_data))
