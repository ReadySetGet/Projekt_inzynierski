"""Service for fuzzy logic calculations and FIS management."""

from typing import Any, Dict, List, Tuple

import fuzzylab as fl
from PyQt6.QtCore import QObject, pyqtSignal

from app.models.fis_model import FISModel


class FuzzyCalculationService(QObject):
    """Service for managing fuzzy inference systems and calculations."""

    # Signals for system updates
    system_changed = pyqtSignal()
    inference_completed = pyqtSignal(list, list)  # inputs, outputs
    error_occurred = pyqtSignal(str, str)  # error_type, error_message

    def __init__(self) -> None:
        """Initialize the FuzzyCalculationService."""
        super().__init__()
        self._fis_model = FISModel()
        self._last_inference_results = []
        self._last_inference_inputs = []
        self._inference_state = "idle"  # idle, calculating, error

        # Add default variables to make the system usable
        self._add_default_variables()

    @property
    def fis_model(self) -> FISModel:
        """Get the FIS model."""
        return self._fis_model

    def get_fis_model(self) -> FISModel:
        """Get the FIS model instance."""
        return self._fis_model

    def get_system_status(self) -> Dict[str, Any]:
        """Get the current system status."""
        return {
            "inputs_count": len(self._fis_model._fis.Inputs),
            "outputs_count": len(self._fis_model._fis.Outputs),
            "rules_count": len(self._fis_model._fis.Rules),
            "inference_state": self._inference_state,
            "last_inference_inputs": self._last_inference_inputs.copy(),
            "last_inference_results": self._last_inference_results.copy(),
        }

    def get_input_variables(self) -> List[Dict[str, Any]]:
        """Get list of input variables."""
        variables = []
        for i, input_var in enumerate(self._fis_model._fis.Inputs):
            variables.append(
                {
                    "index": i,
                    "name": input_var.Name,
                    "range": input_var.Range,
                    "mf_count": len(input_var.MembershipFunctions),
                }
            )
        return variables

    def get_output_variables(self) -> List[Dict[str, Any]]:
        """Get list of output variables."""
        variables = []
        for i, output_var in enumerate(self._fis_model._fis.Outputs):
            variables.append(
                {
                    "index": i,
                    "name": output_var.Name,
                    "range": output_var.Range,
                    "mf_count": len(output_var.MembershipFunctions),
                }
            )
        return variables

    def add_input_variable(self, name: str, range_min: float, range_max: float) -> bool:
        """Add a new input variable."""
        try:
            # Use the FISModel's add_input method which creates default variables
            self._fis_model.add_input()
            # Then rename the last added input
            if len(self._fis_model._fis.Inputs) > 0:
                last_input = self._fis_model._fis.Inputs[-1]
                last_input.Name = name
                last_input.Range = [range_min, range_max]
            self.system_changed.emit()
            return True
        except Exception as e:
            self.error_occurred.emit("add_input_error", str(e))
            return False

    def add_output_variable(
        self, name: str, range_min: float, range_max: float
    ) -> bool:
        """Add a new output variable."""
        try:
            # Use the FISModel's add_output method which creates default variables
            self._fis_model.add_output()
            # Then rename the last added output
            if len(self._fis_model._fis.Outputs) > 0:
                last_output = self._fis_model._fis.Outputs[-1]
                last_output.Name = name
                last_output.Range = [range_min, range_max]
            self.system_changed.emit()
            return True
        except Exception as e:
            self.error_occurred.emit("add_output_error", str(e))
            return False

    def delete_input_variable(self, index: int) -> bool:
        """Delete an input variable by index."""
        try:
            self._fis_model.delete_input(index)
            self.system_changed.emit()
            return True
        except Exception as e:
            self.error_occurred.emit("delete_input_error", str(e))
            return False

    def delete_output_variable(self, index: int) -> bool:
        """Delete an output variable by index."""
        try:
            self._fis_model.delete_output(index)
            self.system_changed.emit()
            return True
        except Exception as e:
            self.error_occurred.emit("delete_output_error", str(e))
            return False

    def add_membership_function(
        self, variable_name: str, mf_name: str, mf_type: str, parameters: List[float]
    ) -> bool:
        """Add a membership function to a variable."""
        try:
            # Determine if it's an input or output variable
            fis = self._fis_model._fis

            # Map MF type names to fuzzylab function names
            type_mapping = {
                "trojkatna": "trimf",
                "trapezoidalna": "trapmf",
                "gaussowska": "gaussmf",
                "dzwonowa": "gbellmf",
            }

            fuzzylab_function = type_mapping.get(mf_type, "trimf")

            # Use fuzzylab's addMF directly with custom parameters
            fis.addMF(variable_name, fuzzylab_function, parameters, Name=mf_name)

            self.system_changed.emit()
            return True
        except Exception as e:
            self.error_occurred.emit("add_mf_error", str(e))
            return False

    def delete_membership_function(self, variable_name: str, mf_index: int) -> bool:
        """Delete a membership function from a variable."""
        try:
            # Determine if it's an input or output variable
            fis = self._fis_model._fis
            is_input = any(var.Name == variable_name for var in fis.Inputs)
            io_type = "input" if is_input else "output"

            result = self._fis_model.delete_mf(variable_name, io_type, mf_index)

            if result == 1:  # Success
                self.system_changed.emit()
                return True
            else:
                return False
        except Exception as e:
            self.error_occurred.emit("delete_mf_error", str(e))
            return False

    def change_membership_function_type(
        self, variable_name: str, mf_index: int, new_type: str
    ) -> bool:
        """Change the type of a membership function."""
        try:
            self._fis_model.change_membership_function_type(
                variable_name, mf_index, new_type
            )
            self.system_changed.emit()
            return True
        except Exception as e:
            self.error_occurred.emit("change_mf_type_error", str(e))
            return False

    def add_rule(self, rule_text: str) -> bool:
        """Add a fuzzy rule."""
        try:
            self._fis_model.add_rule(rule_text)
            self.system_changed.emit()
            return True
        except Exception as e:
            self.error_occurred.emit("add_rule_error", str(e))
            return False

    def delete_rule(self, rule_index: int) -> bool:
        """Delete a fuzzy rule."""
        try:
            self._fis_model.delete_rule(rule_index)
            self.system_changed.emit()
            return True
        except Exception as e:
            self.error_occurred.emit("delete_rule_error", str(e))
            return False

    def update_rule(self, rule_index: int, new_rule_text: str) -> bool:
        """Update a fuzzy rule."""
        try:
            self._fis_model.update_rule(rule_index, new_rule_text)
            self.system_changed.emit()
            return True
        except Exception as e:
            self.error_occurred.emit("update_rule_error", str(e))
            return False

    def clear_all_rules(self) -> bool:
        """Clear all fuzzy rules."""
        try:
            self._fis_model.clear_all_rules()
            self.system_changed.emit()
            return True
        except Exception as e:
            self.error_occurred.emit("clear_rules_error", str(e))
            return False

    def set_inference_state(self, state: str) -> None:
        """Set the inference state."""
        self._inference_state = state

    def get_inference_state(self) -> str:
        """Get the current inference state."""
        return self._inference_state

    def _is_system_ready_for_inference(self) -> bool:
        """Check if the system is ready for inference."""
        return (
            len(self._fis_model._fis.Inputs) > 0
            and len(self._fis_model._fis.Outputs) > 0
            and len(self._fis_model._fis.Rules) > 0
        )

    def perform_inference(
        self, input_values: List[float]
    ) -> Tuple[bool, List[float], Dict[str, Any]]:
        """Perform fuzzy inference with given input values."""
        try:
            self.set_inference_state("calculating")

            if len(input_values) != len(self._fis_model._fis.Inputs):
                error_msg = (
                    f"Expected {len(self._fis_model._fis.Inputs)} input values, "
                    f"got {len(input_values)}"
                )
                self.error_occurred.emit("inference_error", error_msg)
                self.set_inference_state("error")
                return False, [], {"error": error_msg}

            if not self._is_system_ready_for_inference():
                error_msg = (
                    "System not ready for inference - missing variables or "
                    "membership functions"
                )
                self.error_occurred.emit("inference_error", error_msg)
                self.set_inference_state("error")
                return False, [], {"error": error_msg}

            # Use fuzzylab's evalfis function directly
            output_values = fl.evalfis(self._fis_model._fis, input_values)

            self._last_inference_results = output_values
            self._last_inference_inputs = input_values.copy()
            self.set_inference_state("idle")
            self.inference_completed.emit(input_values, output_values)

            return True, output_values, {"success": True}

        except Exception as e:
            error_msg = f"Inference failed: {str(e)}"
            self.error_occurred.emit("inference_error", error_msg)
            self.set_inference_state("error")
            return False, [], {"error": error_msg}

    def _add_default_variables(self) -> None:
        """Add default input and output variables to make the system usable."""
        # Add a default input variable
        self.add_input_variable("Input1", 0, 10)

        # Add a default output variable
        self.add_output_variable("Output1", 0, 10)
