"""FIS State Manager for managing FIS model state and configuration."""

from typing import Any, Dict

from app.models.fis_model import FISModel


class FISStateManager:
    """Manages FIS model state and configuration."""

    def __init__(self, fis_type: str = "mamdani") -> None:
        """Initialize the FIS State Manager.

        Args:
            fis_type: Type of FIS to create ("mamdani" or "sugeno")
        """
        if fis_type.lower() == "sugeno":
            self._fis_model = FISModel(fis_type="sugeno", fis_name="empty_sugeno")
            self._fis_type = "sugeno"
        else:
            self._fis_model = FISModel(fis_type="mamdani", fis_name="empty_mamdani")
            self._fis_type = "mamdani"

        self._last_inference_results = []
        self._last_inference_inputs = []
        self._inference_state = "idle"

        self._selected_input_name: str = None
        self._selected_output_name: str = None

    @property
    def fis_model(self) -> FISModel:
        """Get the FIS model."""
        return self._fis_model

    @property
    def fis_type(self) -> str:
        """Get the current FIS type."""
        return self._fis_type

    @property
    def inference_state(self) -> str:
        """Get the current inference state."""
        return self._inference_state

    @property
    def last_inference_results(self) -> list:
        """Get the last inference results."""
        return self._last_inference_results

    @property
    def last_inference_inputs(self) -> list:
        """Get the last inference inputs."""
        return self._last_inference_inputs

    @property
    def selected_input_name(self) -> str:
        """Get the currently selected input name."""
        return self._selected_input_name

    @property
    def selected_output_name(self) -> str:
        """Get the currently selected output name."""
        return self._selected_output_name

    def set_selected_input(self, input_name: str) -> None:
        """Set the selected input variable.

        Args:
            input_name: Name of the input variable to select
        """
        self._selected_input_name = input_name
        self._selected_output_name = None

    def set_selected_output(self, output_name: str) -> None:
        """Set the selected output variable.

        Args:
            output_name: Name of the output variable to select
        """
        self._selected_output_name = output_name
        self._selected_input_name = None

    def clear_selection(self) -> None:
        """Clear all selections."""
        self._selected_input_name = None
        self._selected_output_name = None

    def set_fis_model(self, fis_model: FISModel) -> None:
        """Replace the current FIS model with a new one."""
        self._fis_model = fis_model
        self._selected_input_name = None
        self._selected_output_name = None
        self._last_inference_results = []
        self._last_inference_inputs = []
        try:
            fis_type_name = type(self._fis_model._fis).__name__.lower()
            if "sug" in fis_type_name:
                self._fis_type = "sugeno"
            else:
                self._fis_type = "mamdani"
        except Exception:
            pass

    def get_selected_variable_info(self) -> Dict[str, Any]:
        """Get information about the currently selected variable.

        Returns:
            Dictionary containing selection information
        """
        return {
            "selected_input": self._selected_input_name,
            "selected_output": self._selected_output_name,
            "has_selection": self._selected_input_name is not None or self._selected_output_name is not None,
        }

    def get_system_status(self) -> Dict[str, Any]:
        """Get the current system status."""
        return {
            "fis_type": self._fis_type,
            "inference_state": self._inference_state,
            "has_inputs": len(self._fis_model._fis.Inputs) > 0,
            "has_outputs": len(self._fis_model._fis.Outputs) > 0,
            "has_rules": len(self._fis_model._fis.Rules) > 0,
            "is_ready": self._is_system_ready_for_inference(),
            "selected_input": self._selected_input_name,
            "selected_output": self._selected_output_name,
        }

    def set_inference_state(self, state: str) -> None:
        """Set the inference state."""
        self._inference_state = state

    def update_inference_results(self, inputs: list, outputs: list) -> None:
        """Update the last inference results."""
        self._last_inference_inputs = inputs
        self._last_inference_results = outputs

    def create_mamdani_fis(self, name: str = "mamdani_fis") -> bool:
        """Create a new Mamdani FIS system.

        Args:
            name: Name for the FIS system.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            self._fis_model = FISModel()
            self._fis_type = "mamdani"
            self._selected_input_name = None
            self._selected_output_name = None
            self._add_default_variables()
            return True
        except Exception:
            return False

    def create_sugeno_fis(self, name: str = "sugeno_fis") -> bool:
        """Create a new Sugeno FIS system.

        Args:
            name: Name for the FIS system.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            self._fis_model = FISModel()
            self._fis_type = "sugeno"
            self._selected_input_name = None
            self._selected_output_name = None
            self._add_default_variables()
            return True
        except Exception:
            return False

    def switch_to_mamdani(self) -> bool:
        """Switch to Mamdani FIS system.

        Returns:
            bool: True if successful, False otherwise.
        """
        if self._fis_type == "mamdani":
            return True

        if not self.create_mamdani_fis():
            return False

        return True

    def switch_to_sugeno(self) -> bool:
        """Switch to Sugeno FIS system.

        Returns:
            bool: True if successful, False otherwise.
        """
        if self._fis_type == "sugeno":
            return True

        if not self.create_sugeno_fis():
            return False

        return True

    def _is_system_ready_for_inference(self) -> bool:
        """Check if the system is ready for inference."""
        return (
            len(self._fis_model._fis.Inputs) > 0
            and len(self._fis_model._fis.Outputs) > 0
            and len(self._fis_model._fis.Rules) > 0
        )

    def _add_default_variables(self) -> None:
        """Add default variables to the FIS system."""
        self._fis_model.add_input()
        if self._fis_model._fis.Inputs:
            self._fis_model._fis.Inputs[0].Name = "input1"
            self._fis_model._fis.Inputs[0].Range = [0, 1]

        self._fis_model.add_input()
        if len(self._fis_model._fis.Inputs) > 1:
            self._fis_model._fis.Inputs[1].Name = "input2"
            self._fis_model._fis.Inputs[1].Range = [0, 1]

        self._add_default_input_membership_functions()

        self._fis_model.add_output()
        if self._fis_model._fis.Outputs:
            self._fis_model._fis.Outputs[0].Name = "output1"
            self._fis_model._fis.Outputs[0].Range = [0, 1]

            self._add_default_output_membership_functions()

        if self._fis_model._fis.Inputs:
            self._selected_input_name = self._fis_model._fis.Inputs[0].Name

    def _add_default_input_membership_functions(self) -> None:
        """Add default membership functions to all input variables."""
        try:
            for input_idx, input_var in enumerate(self._fis_model._fis.Inputs):
                input_name = input_var.Name
                input_range = input_var.Range if input_var.Range else [0, 1]
                range_min, range_max = input_range[0], input_range[1]

                self._fis_model.add_mf(input_name, "input", "trojkatna")
                if input_var.MembershipFunctions:
                    input_var.MembershipFunctions[0].Parameters = [
                        range_min,
                        range_min,
                        (range_min + range_max) / 2,
                    ]
                    input_var.MembershipFunctions[0].Name = "low"

                self._fis_model.add_mf(input_name, "input", "trojkatna")
                if input_var.MembershipFunctions and len(input_var.MembershipFunctions) > 1:
                    input_var.MembershipFunctions[1].Parameters = [
                        range_min,
                        (range_min + range_max) / 2,
                        range_max,
                    ]
                    input_var.MembershipFunctions[1].Name = "medium"

                self._fis_model.add_mf(input_name, "input", "trojkatna")
                if input_var.MembershipFunctions and len(input_var.MembershipFunctions) > 2:
                    input_var.MembershipFunctions[2].Parameters = [
                        (range_min + range_max) / 2,
                        range_max,
                        range_max,
                    ]
                    input_var.MembershipFunctions[2].Name = "high"
        except Exception:
            pass

    def _add_default_output_membership_functions(self) -> None:
        """Add default membership functions to the output variable."""
        try:
            output_range = self._fis_model._fis.Outputs[0].Range if self._fis_model._fis.Outputs else [0, 1]
            range_min, range_max = output_range[0], output_range[1]

            self._fis_model.add_mf("output1", "output", "trojkatna")
            if self._fis_model._fis.Outputs and self._fis_model._fis.Outputs[0].MembershipFunctions:
                self._fis_model._fis.Outputs[0].MembershipFunctions[0].Parameters = [
                    range_min,
                    range_min,
                    (range_min + range_max) / 2,
                ]
                self._fis_model._fis.Outputs[0].MembershipFunctions[0].Name = "low"

            self._fis_model.add_mf("output1", "output", "trojkatna")
            if self._fis_model._fis.Outputs and self._fis_model._fis.Outputs[0].MembershipFunctions:
                self._fis_model._fis.Outputs[0].MembershipFunctions[1].Parameters = [
                    range_min,
                    (range_min + range_max) / 2,
                    range_max,
                ]
                self._fis_model._fis.Outputs[0].MembershipFunctions[1].Name = "medium"

            self._fis_model.add_mf("output1", "output", "trojkatna")
            if self._fis_model._fis.Outputs and self._fis_model._fis.Outputs[0].MembershipFunctions:
                self._fis_model._fis.Outputs[0].MembershipFunctions[2].Parameters = [
                    (range_min + range_max) / 2,
                    range_max,
                    range_max,
                ]
                self._fis_model._fis.Outputs[0].MembershipFunctions[2].Name = "high"
        except Exception:
            pass
