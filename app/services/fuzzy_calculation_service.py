"""Service for fuzzy logic calculations and FIS management."""

from typing import Any, Dict, List, Tuple

from app.services.fis_state_manager import FISStateManager
from app.services.fuzzy.fuzzy_inference_engine import FuzzyInferenceEngine
from app.services.fuzzy.membership_function_manager import MembershipFunctionManager
from app.services.fuzzy.rule_manager import RuleManager
from app.services.fuzzy.variable_manager import VariableManager


class FuzzyCalculationService:
    """Service for managing fuzzy inference systems and calculations."""

    def __init__(self, fis_type: str = "mamdani") -> None:
        """Initialize the FuzzyCalculationService.

        Args:
            fis_type: Type of FIS to create ("mamdani" or "sugeno")
        """
        # Initialize the state manager
        self._state_manager = FISStateManager(fis_type)

        # Initialize managers
        self._variable_manager = VariableManager(self._state_manager.fis_model)
        self._mf_manager = MembershipFunctionManager(self._state_manager.fis_model)
        self._rule_manager = RuleManager(self._state_manager.fis_model)
        self._inference_engine = FuzzyInferenceEngine(self._state_manager.fis_model)

    # FIS Model Access
    @property
    def fis_model(self):
        """Get the FIS model."""
        return self._state_manager.fis_model

    def get_fis_model(self):
        """Get the FIS model instance."""
        return self._state_manager.fis_model

    # System Status
    def get_system_status(self) -> Dict[str, Any]:
        """Get the current system status."""
        return self._state_manager.get_system_status()

    def get_inference_state(self) -> str:
        """Get the current inference state."""
        return self._state_manager.inference_state

    def set_inference_state(self, state: str) -> None:
        """Set the inference state."""
        self._state_manager.set_inference_state(state)

    # Variable Management
    def get_input_variables(self) -> List[Dict[str, Any]]:
        """Get list of input variables."""
        return self._variable_manager.get_input_variables()

    def get_output_variables(self) -> List[Dict[str, Any]]:
        """Get list of output variables."""
        return self._variable_manager.get_output_variables()

    def add_input_variable(self, name: str, range_min: float, range_max: float) -> bool:
        """Add a new input variable."""
        return self._variable_manager.add_input_variable(name, range_min, range_max)

    def add_output_variable(self, name: str, range_min: float, range_max: float) -> bool:
        """Add a new output variable."""
        return self._variable_manager.add_output_variable(name, range_min, range_max)

    def delete_input_variable(self, index: int) -> bool:
        """Delete an input variable by index."""
        return self._variable_manager.delete_input_variable(index)

    def delete_output_variable(self, index: int) -> bool:
        """Delete an output variable by index."""
        return self._variable_manager.delete_output_variable(index)

    def update_input_variable_range(self, index: int, range_min: float, range_max: float) -> bool:
        """Update the range of an input variable."""
        return self._variable_manager.update_input_variable_range(index, range_min, range_max)

    def update_output_variable_range(self, index: int, range_min: float, range_max: float) -> bool:
        """Update the range of an output variable."""
        return self._variable_manager.update_output_variable_range(index, range_min, range_max)

    def update_variable_name(self, variable_name: str, new_name: str, variable_type: str) -> bool:
        """Update the name of a variable."""
        return self._variable_manager.update_variable_name(variable_name, new_name, variable_type)

    def update_variable_range(self, variable_name: str, new_range: List[float], variable_type: str) -> bool:
        """Update the range of a variable.

        Args:
            variable_name: Name of the variable to update
            new_range: New range as [min, max]
            variable_type: Type of variable ("input" or "output")

        Returns:
            bool: True if successful, False otherwise
        """
        if len(new_range) != 2:
            return False

        range_min, range_max = new_range[0], new_range[1]

        if variable_type == "input":
            # Find the input variable by name and get its index
            for i, input_var in enumerate(self._state_manager.fis_model._fis.Inputs):
                if input_var.Name == variable_name:
                    return self._variable_manager.update_input_variable_range(i, range_min, range_max)
        else:
            # Find the output variable by name and get its index
            for i, output_var in enumerate(self._state_manager.fis_model._fis.Outputs):
                if output_var.Name == variable_name:
                    return self._variable_manager.update_output_variable_range(i, range_min, range_max)

        return False

    # Membership Function Management
    def get_membership_functions(self, variable_name: str, variable_type: str) -> List[Dict[str, Any]]:
        """Get membership functions for a specific variable."""
        return self._mf_manager.get_membership_functions(variable_name, variable_type)

    def add_membership_function(
        self,
        variable_name: str,
        mf_name: str,
        mf_type: str,
        parameters: List[float],
        variable_type: str,
    ) -> bool:
        """Add a new membership function to a variable."""
        return self._mf_manager.add_membership_function(variable_name, mf_name, mf_type, parameters, variable_type)

    def delete_membership_function(self, variable_name: str, mf_index: int, variable_type: str) -> bool:
        """Delete a membership function from a variable."""
        return self._mf_manager.delete_membership_function(variable_name, mf_index, variable_type)

    def change_membership_function_type(
        self,
        variable_name: str,
        mf_index: int,
        new_type: str,
        variable_type: str,
    ) -> bool:
        """Change the type of a membership function."""
        return self._mf_manager.change_membership_function_type(variable_name, mf_index, new_type, variable_type)

    def update_membership_function_parameters(
        self,
        variable_name: str,
        mf_index: int,
        new_parameters: List[float],
        variable_type: str,
    ) -> bool:
        """Update the parameters of a membership function."""
        return self._mf_manager.update_membership_function_parameters(
            variable_name, mf_index, new_parameters, variable_type
        )

    def update_membership_function_name(
        self,
        variable_name: str,
        mf_index: int,
        new_name: str,
        variable_type: str,
    ) -> bool:
        """Update the name of a membership function."""
        return self._mf_manager.update_membership_function_name(variable_name, mf_index, new_name, variable_type)

    # Rule Management
    def get_rules(self) -> List[Dict[str, Any]]:
        """Get all rules."""
        return self._rule_manager.get_rules()

    def add_rule(
        self,
        rule_name: str = "Rule",
        antecedent: List[int] = None,
        consequent: List[int] = None,
        weight: float = 1.0,
        connection: int = 1,
        is_mf: List[int] = None,
    ) -> bool:
        """Add a new rule."""
        if antecedent is None:
            antecedent = [0] * len(self.get_input_variables())
        if consequent is None:
            consequent = [0] * len(self.get_output_variables())
        return self._rule_manager.add_rule(rule_name, antecedent, consequent, weight, connection, is_mf)

    def delete_rule(self, rule_index: int) -> bool:
        """Delete a rule by index."""
        return self._rule_manager.delete_rule(rule_index)

    def update_rule(
        self,
        rule_index: int,
        new_antecedent: List[int],
        new_consequent: List[int],
        new_weight: float,
        new_connection: int,
        new_is_mf: List[int],
    ) -> bool:
        """Update a rule."""
        return self._rule_manager.update_rule(
            rule_index,
            new_antecedent,
            new_consequent,
            new_weight,
            new_connection,
            new_is_mf,
        )

    def clear_all_rules(self) -> bool:
        """Clear all rules."""
        return self._rule_manager.clear_all_rules()

    def get_rule_text(self, rule_index: int) -> str:
        """Get the text representation of a rule."""
        return self._rule_manager.get_rule_text(rule_index)

    # Inference Operations
    def perform_inference(self, inputs: List[float]) -> Tuple[List[float], bool]:
        """Perform fuzzy inference with given inputs."""
        outputs, success = self._inference_engine.perform_inference(inputs)
        if success:
            self._state_manager.update_inference_results(inputs, outputs)
        return outputs, success

    def get_inference_results(self) -> Dict[str, Any]:
        """Get the last inference results."""
        return {
            "inputs": self._state_manager.last_inference_inputs,
            "outputs": self._state_manager.last_inference_results,
            "success": len(self._state_manager.last_inference_results) > 0,
        }

    def get_inference_statistics(self) -> Dict[str, Any]:
        """Get statistics about the inference system."""
        return self._inference_engine.get_inference_statistics()

    def validate_inputs(self, inputs: List[float]) -> Tuple[bool, str]:
        """Validate input values for inference."""
        return self._inference_engine.validate_inputs(inputs)

    # FIS Type Management
    def get_fis_type(self) -> str:
        """Get the current FIS type."""
        return self._state_manager.fis_type

    def create_mamdani_fis(self, name: str = "mamdani_fis") -> bool:
        """Create a new Mamdani FIS system."""
        return self._state_manager.create_mamdani_fis(name)

    def create_sugeno_fis(self, name: str = "sugeno_fis") -> bool:
        """Create a new Sugeno FIS system."""
        return self._state_manager.create_sugeno_fis(name)

    def switch_to_mamdani(self) -> bool:
        """Switch to Mamdani FIS system."""
        return self._state_manager.switch_to_mamdani()

    def switch_to_sugeno(self) -> bool:
        """Switch to Sugeno FIS system."""
        return self._state_manager.switch_to_sugeno()

    # Legacy compatibility methods
    def get_input_count(self) -> int:
        """Get the number of input variables."""
        return len(self.get_input_variables())

    def get_output_count(self) -> int:
        """Get the number of output variables."""
        return len(self.get_output_variables())

    def get_rule_count(self) -> int:
        """Get the number of rules."""
        return self._rule_manager.get_rule_count()

    def is_system_ready(self) -> bool:
        """Check if the system is ready for inference."""
        return self._state_manager.get_system_status()["is_ready"]

    # Selection Management
    def set_selected_input(self, input_name: str) -> None:
        """Set the selected input variable.

        Args:
            input_name: Name of the input variable to select
        """
        self._state_manager.set_selected_input(input_name)

    def set_selected_output(self, output_name: str) -> None:
        """Set the selected output variable.

        Args:
            output_name: Name of the output variable to select
        """
        self._state_manager.set_selected_output(output_name)

    def clear_selection(self) -> None:
        """Clear all variable selections."""
        self._state_manager.clear_selection()

    def get_selected_input_name(self) -> str:
        """Get the currently selected input name.

        Returns:
            Name of the selected input variable or None
        """
        return self._state_manager.selected_input_name

    def get_selected_output_name(self) -> str:
        """Get the currently selected output name.

        Returns:
            Name of the selected output variable or None
        """
        return self._state_manager.selected_output_name

    def get_selected_variable_info(self) -> Dict[str, Any]:
        """Get information about the currently selected variable.

        Returns:
            Dictionary containing selection information
        """
        return self._state_manager.get_selected_variable_info()

    def get_selected_input_data(self) -> Dict[str, Any]:
        """Get data for the currently selected input variable.

        Returns:
            Dictionary containing input variable data or None if no input selected
        """
        selected_input = self.get_selected_input_name()
        if not selected_input:
            return None

        inputs = self.get_input_variables()
        for input_var in inputs:
            if input_var.get("name") == selected_input:
                return input_var
        return None

    def get_selected_output_data(self) -> Dict[str, Any]:
        """Get data for the currently selected output variable.

        Returns:
            Dictionary containing output variable data or None if no output selected
        """
        selected_output = self.get_selected_output_name()
        if not selected_output:
            return None

        outputs = self.get_output_variables()
        for output_var in outputs:
            if output_var.get("name") == selected_output:
                return output_var
        return None
