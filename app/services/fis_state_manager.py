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
        self._fis_model = FISModel()
        self._fis_type = fis_type
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

    def get_system_status(self) -> Dict[str, Any]:
        """Get the current system status."""
        return {
            "fis_type": self._fis_type,
            "inference_state": self._inference_state,
            "has_inputs": len(self._fis_model._fis.Inputs) > 0,
            "has_outputs": len(self._fis_model._fis.Outputs) > 0,
            "has_rules": len(self._fis_model._fis.Rules) > 0,
            "is_ready": self._is_system_ready_for_inference(),
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

        # Create new Mamdani FIS
        if not self.create_mamdani_fis():
            return False

        # Note: In practice, you might want more sophisticated state preservation
        return True

    def switch_to_sugeno(self) -> bool:
        """Switch to Sugeno FIS system.

        Returns:
            bool: True if successful, False otherwise.
        """
        if self._fis_type == "sugeno":
            return True

        # Create new Sugeno FIS
        if not self.create_sugeno_fis():
            return False

        # Note: In practice, you might want more sophisticated state preservation
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
        # Add a default input variable
        self._fis_model.add_input()
        if self._fis_model._fis.Inputs:
            self._fis_model._fis.Inputs[0].Name = "input1"
            self._fis_model._fis.Inputs[0].Range = [0, 10]

            # Add membership functions to the input variable
            self._add_default_input_membership_functions()

        # Add a default output variable
        self._fis_model.add_output()
        if self._fis_model._fis.Outputs:
            self._fis_model._fis.Outputs[0].Name = "output1"
            self._fis_model._fis.Outputs[0].Range = [0, 10]

            # Add membership functions to the output variable
            self._add_default_output_membership_functions()

    def _add_default_input_membership_functions(self) -> None:
        """Add default membership functions to the input variable."""
        try:
            # Add triangular membership functions using predefined types
            self._fis_model.add_mf("input1", "input", "trojkatna")
            self._fis_model.add_mf("input1", "input", "trojkatna")
            self._fis_model.add_mf("input1", "input", "trojkatna")
        except Exception as e:
            print(f"Error adding input membership functions: {e}")

    def _add_default_output_membership_functions(self) -> None:
        """Add default membership functions to the output variable."""
        try:
            # Add triangular membership functions using predefined types
            self._fis_model.add_mf("output1", "output", "trojkatna")
            self._fis_model.add_mf("output1", "output", "trojkatna")
            self._fis_model.add_mf("output1", "output", "trojkatna")
        except Exception as e:
            print(f"Error adding output membership functions: {e}")
