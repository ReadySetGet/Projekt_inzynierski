"""Service for fuzzy logic calculations and FIS management."""

from typing import Any, Dict, List, Tuple

import fuzzylab as fl
from PyQt6.QtCore import QObject, pyqtSignal

from app.models.fis_model import FISModel
from app.models.modelsresources.evalfis_ext import evalfis


class FuzzyCalculationService(QObject):
    """Service for managing fuzzy inference systems and calculations."""

    # Signals for system updates
    system_changed = pyqtSignal()
    inference_completed = pyqtSignal(list, list)  # inputs, outputs
    error_occurred = pyqtSignal(str, str)  # error_type, error_message

    def __init__(self, fis_type: str = "mamdani") -> None:
        """Initialize the FuzzyCalculationService.

        Args:
            fis_type: Type of FIS to create ("mamdani" or "sugeno")
        """
        super().__init__()
        self._fis_model = FISModel()
        self._last_inference_results = []
        self._last_inference_inputs = []
        self._inference_state = "idle"  # idle, calculating, error

        # Create the specified FIS type
        if fis_type.lower() == "sugeno":
            self.create_sugeno_fis("default_sugeno_fis")
        else:
            # Default to Mamdani (already created by FISModel())
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

    def get_membership_functions(
        self, variable_name: str, is_input: bool
    ) -> List[Dict[str, Any]]:
        """Get detailed information about membership functions for a variable.

        Args:
            variable_name: Name of the variable
            is_input: True if it's an input variable, False if output

        Returns:
            List of dictionaries containing MF information
        """
        try:
            fis = self._fis_model._fis
            if is_input:
                var = next(var for var in fis.Inputs if var.Name == variable_name)
            else:
                var = next(var for var in fis.Outputs if var.Name == variable_name)

            mfs = []
            for i, mf in enumerate(var.MembershipFunctions):
                mfs.append(
                    {
                        "index": i,
                        "name": mf.Name,
                        "type": mf.Type,
                        "parameters": (
                            mf.Parameters
                            if hasattr(mf.Parameters, "__iter__")
                            else [mf.Parameters]
                        ),
                    }
                )
            return mfs
        except Exception as e:
            self.error_occurred.emit("get_mf_error", str(e))
            return []

    def get_inference_results(self) -> Dict[str, Any]:
        """Get the last inference results with detailed information.

        Returns:
            Dictionary containing inference results and metadata
        """
        return {
            "inputs": self._last_inference_inputs.copy(),
            "outputs": self._last_inference_results.copy(),
            "state": self._inference_state,
            "fis_type": self.get_fis_type(),
            "timestamp": getattr(self, "_last_inference_time", None),
        }

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

    def update_input_variable_range(
        self, index: int, range_min: float, range_max: float
    ) -> bool:
        """Update the range of an input variable.

        Args:
            index: Index of the input variable
            range_min: New minimum value of the range
            range_max: New maximum value of the range

        Returns:
            bool: True if updated successfully, False otherwise
        """
        try:
            if index >= len(self._fis_model._fis.Inputs):
                self.error_occurred.emit("update_input_error", "Invalid input index")
                return False

            self._fis_model._fis.Inputs[index].Range = [range_min, range_max]
            self.system_changed.emit()
            return True
        except Exception as e:
            self.error_occurred.emit("update_input_error", str(e))
            return False

    def update_output_variable_range(
        self, index: int, range_min: float, range_max: float
    ) -> bool:
        """Update the range of an output variable.

        Args:
            index: Index of the output variable
            range_min: New minimum value of the range
            range_max: New maximum value of the range

        Returns:
            bool: True if updated successfully, False otherwise
        """
        try:
            if index >= len(self._fis_model._fis.Outputs):
                self.error_occurred.emit("update_output_error", "Invalid output index")
                return False

            self._fis_model._fis.Outputs[index].Range = [range_min, range_max]
            self.system_changed.emit()
            return True
        except Exception as e:
            self.error_occurred.emit("update_output_error", str(e))
            return False

    def update_variable_name(
        self, variable_name: str, new_name: str, is_input: bool
    ) -> bool:
        """Update the name of a variable.

        Args:
            variable_name: Current name of the variable
            new_name: New name for the variable
            is_input: True if it's an input variable, False if output

        Returns:
            bool: True if updated successfully, False otherwise
        """
        try:
            if is_input:
                variables = self._fis_model._fis.Inputs
            else:
                variables = self._fis_model._fis.Outputs

            for var in variables:
                if var.Name == variable_name:
                    var.Name = new_name
                    self.system_changed.emit()
                    return True

            self.error_occurred.emit("update_name_error", "Variable not found")
            return False
        except Exception as e:
            self.error_occurred.emit("update_name_error", str(e))
            return False

    def add_membership_function(
        self, variable_name: str, mf_name: str, mf_type: str, parameters: List[float]
    ) -> bool:
        """Add a membership function to a variable."""
        try:
            # Determine if it's an input or output variable
            fis = self._fis_model._fis
            is_input = any(var.Name == variable_name for var in fis.Inputs)
            io_type = "input" if is_input else "output"

            # Use the FISModel's add_mf method which handles type validation
            result = self._fis_model.add_mf(variable_name, io_type, mf_type)

            if result == 1:  # Success
                # Update the membership function name and parameters
                if is_input:
                    var = next(var for var in fis.Inputs if var.Name == variable_name)
                else:
                    var = next(var for var in fis.Outputs if var.Name == variable_name)

                # Get the last added membership function
                if var.MembershipFunctions:
                    last_mf = var.MembershipFunctions[-1]
                    last_mf.Name = mf_name
                    # Update parameters if provided
                    if parameters:
                        last_mf.Parameters = parameters

                self.system_changed.emit()
                return True
            else:
                self.error_occurred.emit("add_mf_error", f"Failed to add MF: {result}")
                return False
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

            # Check current MF count before deletion
            if is_input:
                next(var for var in fis.Inputs if var.Name == variable_name)
            else:
                next(var for var in fis.Outputs if var.Name == variable_name)

            result = self._fis_model.delete_mf(variable_name, io_type, mf_index)

            if result == 1:  # Success
                # Check MF count after deletion
                if is_input:
                    next(var for var in fis.Inputs if var.Name == variable_name)
                else:
                    next(var for var in fis.Outputs if var.Name == variable_name)

                self.system_changed.emit()
                return True
            else:
                return False
        except Exception as e:
            self.error_occurred.emit("delete_mf_error", str(e))
            return False

    def change_membership_function_type(
        self, variable_name: str, input_or_output: str, mf_index: int, new_type: str
    ) -> bool:
        """Change the type of a membership function."""
        try:
            result = self._fis_model.change_mf_type(
                variable_name, input_or_output, mf_index, new_type
            )

            if result == 1:  # Success
                self.system_changed.emit()
                return True
            else:
                return False
        except Exception as e:
            self.error_occurred.emit("change_mf_type_error", str(e))
            return False

    def update_membership_function_parameters(
        self, variable_name: str, mf_index: int, new_parameters: List[float]
    ) -> bool:
        """Update the parameters of a membership function.

        Args:
            variable_name: Name of the variable containing the membership function
            mf_index: Index of the membership function
            new_parameters: New parameters for the membership function

        Returns:
            bool: True if updated successfully, False otherwise
        """
        try:
            # Find the variable
            fis = self._fis_model._fis
            is_input = any(var.Name == variable_name for var in fis.Inputs)

            if is_input:
                var = next(var for var in fis.Inputs if var.Name == variable_name)
            else:
                var = next(var for var in fis.Outputs if var.Name == variable_name)

            if mf_index >= len(var.MembershipFunctions):
                self.error_occurred.emit("update_mf_params_error", "Invalid MF index")
                return False

            # Update the parameters
            var.MembershipFunctions[mf_index].Parameters = new_parameters
            self.system_changed.emit()
            return True
        except Exception as e:
            self.error_occurred.emit("update_mf_params_error", str(e))
            return False

    def update_membership_function_name(
        self, variable_name: str, mf_index: int, new_name: str
    ) -> bool:
        """Update the name of a membership function.

        Args:
            variable_name: Name of the variable containing the membership function
            mf_index: Index of the membership function
            new_name: New name for the membership function

        Returns:
            bool: True if updated successfully, False otherwise
        """
        try:
            # Find the variable
            fis = self._fis_model._fis
            is_input = any(var.Name == variable_name for var in fis.Inputs)

            if is_input:
                var = next(var for var in fis.Inputs if var.Name == variable_name)
            else:
                var = next(var for var in fis.Outputs if var.Name == variable_name)

            if mf_index >= len(var.MembershipFunctions):
                self.error_occurred.emit("update_mf_name_error", "Invalid MF index")
                return False

            # Update the name
            var.MembershipFunctions[mf_index].Name = new_name
            self.system_changed.emit()
            return True
        except Exception as e:
            self.error_occurred.emit("update_mf_name_error", str(e))
            return False

    def add_rule(
        self,
        is_mf: List[int] = None,
        rule_data: List[int] = None,
    ) -> bool:
        """Add a fuzzy rule.

        Args:
            is_mf: List of variable to mf mapping behaviours when inferring
                   (1 - use IS, else - use IS NOT). If None, IS values are used.
            rule_data: List in form of [imf1, imf2, ..., omf1, omf2, ..., w, c]
                      where imf* are input mf indices, omf* are output mf indices,
                      w is weight, c is connection (1=AND, else=OR). If None,
                      default values are used.
        """
        try:
            result = self._fis_model.add_rule(is_mf, rule_data)
            if result == 1:  # Success
                self.system_changed.emit()
                return True
            else:
                self.error_occurred.emit(
                    "add_rule_error", f"Failed to add rule: {result}"
                )
                return False
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

    def update_rule(
        self,
        rule_index: int,
        new_rule_is_mf: List[int],
        new_rule_data: List[int],
    ) -> bool:
        """Update a fuzzy rule.

        Args:
            rule_index: Index of the rule to update
            new_rule_is_mf: List of variable to mf mapping behaviours when inferring
                           (1 - use IS, else - use IS NOT)
            new_rule_data: List in form of [imf1, imf2, ..., omf1, omf2, ..., w, c]
                          where imf* are input mf indices, omf* are output mf indices,
                          w is weight, c is connection (1=AND, else=OR)
        """
        try:
            result = self._fis_model.update_rule(
                rule_index, new_rule_is_mf, new_rule_data
            )
            if result == 1:  # Success
                self.system_changed.emit()
                return True
            else:
                self.error_occurred.emit(
                    "update_rule_error", f"Failed to update rule: {result}"
                )
                return False
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

            # Use extended evalfis function from evalfis_ext
            output_values = evalfis(self._fis_model._fis, input_values)

            # Convert numpy types to Python types for signal emission
            if hasattr(output_values, "tolist"):
                output_values = output_values.tolist()
            elif hasattr(output_values, "item"):
                output_values = output_values.item()

            # Ensure output_values is a list for signal emission
            if not isinstance(output_values, list):
                output_values = [output_values]

            self._last_inference_results = output_values
            self._last_inference_inputs = input_values.copy()
            self._last_inference_time = __import__("time").time()
            self.set_inference_state("idle")
            self.inference_completed.emit(input_values, output_values)

            return True, output_values, {"success": True}

        except Exception as e:
            error_msg = f"Inference failed: {str(e)}"
            self.error_occurred.emit("inference_error", error_msg)
            self.set_inference_state("error")
            return False, [], {"error": error_msg}

    def get_fis_type(self) -> str:
        """Get the current FIS type."""
        return self._fis_model._fis.Type

    def create_mamdani_fis(self, name: str = "mamdani_fis") -> bool:
        """Create a new Mamdani type fuzzy inference system.

        Args:
            name: Name for the new FIS system

        Returns:
            bool: True if created successfully, False otherwise
        """
        try:
            new_fis = fl.mamfis(name)
            self._fis_model = FISModel(new_fis)
            self._add_default_variables()
            self.system_changed.emit()
            return True
        except Exception as e:
            self.error_occurred.emit("create_fis_error", str(e))
            return False

    def create_sugeno_fis(self, name: str = "sugeno_fis") -> bool:
        """Create a new Sugeno type fuzzy inference system.

        Args:
            name: Name for the new FIS system

        Returns:
            bool: True if created successfully, False otherwise
        """
        try:
            new_fis = fl.sugfis(name)
            self._fis_model = FISModel(new_fis)
            self._add_default_variables()
            self.system_changed.emit()
            return True
        except Exception as e:
            self.error_occurred.emit("create_fis_error", str(e))
            return False

    def switch_to_mamdani(self) -> bool:
        """Switch the current FIS to Mamdani type.

        Returns:
            bool: True if switched successfully, False otherwise
        """
        if self.get_fis_type() == "mamdani":
            return True  # Already Mamdani type

        try:
            # Save current variables and rules
            current_inputs = self.get_input_variables()
            current_outputs = self.get_output_variables()
            # Create new Mamdani FIS
            new_fis = fl.mamfis("mamdani_fis")
            self._fis_model = FISModel(new_fis)

            # Restore variables
            for input_var in current_inputs:
                self.add_input_variable(
                    input_var["name"],
                    input_var["range"][0],
                    input_var["range"][1],
                )

            for output_var in current_outputs:
                self.add_output_variable(
                    output_var["name"],
                    output_var["range"][0],
                    output_var["range"][1],
                )

            # Note: Rules will need to be recreated as they may have different
            # structures between Mamdani and Sugeno systems

            self.system_changed.emit()
            return True
        except Exception as e:
            self.error_occurred.emit("switch_fis_error", str(e))
            return False

    def switch_to_sugeno(self) -> bool:
        """Switch the current FIS to Sugeno type.

        Returns:
            bool: True if switched successfully, False otherwise
        """
        if self.get_fis_type() == "sugeno":
            return True  # Already Sugeno type

        try:
            # Save current variables and rules
            current_inputs = self.get_input_variables()
            current_outputs = self.get_output_variables()
            # Create new Sugeno FIS
            new_fis = fl.sugfis("sugeno_fis")
            self._fis_model = FISModel(new_fis)

            # Restore variables
            for input_var in current_inputs:
                self.add_input_variable(
                    input_var["name"],
                    input_var["range"][0],
                    input_var["range"][1],
                )

            for output_var in current_outputs:
                self.add_output_variable(
                    output_var["name"],
                    output_var["range"][0],
                    output_var["range"][1],
                )

            # Note: Rules will need to be recreated as they may have different
            # structures between Mamdani and Sugeno systems

            self.system_changed.emit()
            return True
        except Exception as e:
            self.error_occurred.emit("switch_fis_error", str(e))
            return False

    def _add_default_variables(self) -> None:
        """Add default input and output variables to make the system usable."""
        # Add a default input variable
        self.add_input_variable("Input1", 0, 10)

        # Add a default output variable
        self.add_output_variable("Output1", 0, 10)
