"""Variable Manager for managing FIS input and output variables."""

from typing import Dict, List, Optional

from app.models.fis_model import FISModel


class VariableManager:
    """Manages FIS input and output variables."""

    def __init__(self, fis_model: FISModel) -> None:
        """Initialize the Variable Manager.

        Args:
            fis_model: The FIS model to manage variables for.
        """
        self._fis_model = fis_model

    def get_input_variables(self) -> List[Dict[str, any]]:
        """Get all input variables.

        Returns:
            List of dictionaries containing input variable information including membership functions.
        """
        variables = []
        for i, input_var in enumerate(self._fis_model._fis.Inputs):
            # Get membership functions for this variable
            mfs = []
            for j, mf in enumerate(input_var.MembershipFunctions):
                mfs.append(
                    {
                        "index": j,
                        "name": mf.Name,
                        "type": mf.Type,
                        "parameters": mf.Parameters,
                    }
                )

            variables.append(
                {
                    "index": i,
                    "name": input_var.Name,
                    "range": input_var.Range,
                    "mf_count": len(input_var.MembershipFunctions),
                    "membership_functions": mfs,
                }
            )
        return variables

    def get_output_variables(self) -> List[Dict[str, any]]:
        """Get all output variables.

        Returns:
            List of dictionaries containing output variable information including membership functions.
        """
        variables = []
        for i, output_var in enumerate(self._fis_model._fis.Outputs):
            # Get membership functions for this variable
            mfs = []
            for j, mf in enumerate(output_var.MembershipFunctions):
                mfs.append(
                    {
                        "index": j,
                        "name": mf.Name,
                        "type": mf.Type,
                        "parameters": mf.Parameters,
                    }
                )

            variables.append(
                {
                    "index": i,
                    "name": output_var.Name,
                    "range": output_var.Range,
                    "mf_count": len(output_var.MembershipFunctions),
                    "membership_functions": mfs,
                }
            )
        return variables

    def add_input_variable(self, name: str, range_min: float, range_max: float) -> bool:
        """Add a new input variable.

        Args:
            name: Name of the input variable.
            range_min: Minimum value of the range.
            range_max: Maximum value of the range.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            self._fis_model.add_input()
            # Check if input was successfully added
            if self._fis_model._fis.Inputs:
                # Set the name and range for the newly added input
                new_input = self._fis_model._fis.Inputs[-1]
                new_input.Name = name
                new_input.Range = [range_min, range_max]

                # Add default membership functions
                self._add_default_input_membership_functions(name)
                return True
            return False
        except Exception as e:
            print(f"Error adding input variable: {e}")
            return False

    def add_output_variable(self, name: str, range_min: float, range_max: float) -> bool:
        """Add a new output variable.

        Args:
            name: Name of the output variable.
            range_min: Minimum value of the range.
            range_max: Maximum value of the range.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            self._fis_model.add_output()
            # Check if output was successfully added
            if self._fis_model._fis.Outputs:
                # Set the name and range for the newly added output
                new_output = self._fis_model._fis.Outputs[-1]
                new_output.Name = name
                new_output.Range = [range_min, range_max]

                # Add default membership functions
                self._add_default_output_membership_functions(name)
                return True
            return False
        except Exception as e:
            print(f"Error adding output variable: {e}")
            return False

    def _add_default_input_membership_functions(self, variable_name: str) -> None:
        """Add default membership functions to an input variable.

        Args:
            variable_name: Name of the input variable
        """
        try:
            # Add triangular membership functions with different parameters
            # Low: [0, 0, 0.5] -> [0, 0, 5] when scaled to [0, 10]
            self._fis_model.add_mf(variable_name, "input", "trojkatna")
            if self._fis_model._fis.Inputs:
                for var in self._fis_model._fis.Inputs:
                    if var.Name == variable_name and var.MembershipFunctions:
                        var.MembershipFunctions[0].Parameters = [0, 0, 0.5]
                        var.MembershipFunctions[0].Name = "low"
                        break

            # Medium: [0, 0.5, 1] -> [0, 5, 10] when scaled to [0, 10]
            self._fis_model.add_mf(variable_name, "input", "trojkatna")
            if self._fis_model._fis.Inputs:
                for var in self._fis_model._fis.Inputs:
                    if var.Name == variable_name and len(var.MembershipFunctions) >= 2:
                        var.MembershipFunctions[1].Parameters = [0, 0.5, 1]
                        var.MembershipFunctions[1].Name = "medium"
                        break

            # High: [0.5, 1, 1] -> [5, 10, 10] when scaled to [0, 10]
            self._fis_model.add_mf(variable_name, "input", "trojkatna")
            if self._fis_model._fis.Inputs:
                for var in self._fis_model._fis.Inputs:
                    if var.Name == variable_name and len(var.MembershipFunctions) >= 3:
                        var.MembershipFunctions[2].Parameters = [0.5, 1, 1]
                        var.MembershipFunctions[2].Name = "high"
                        break
        except Exception:
            pass

    def _add_default_output_membership_functions(self, variable_name: str) -> None:
        """Add default membership functions to an output variable.

        Args:
            variable_name: Name of the output variable
        """
        try:
            # Add triangular membership functions with different parameters
            # Low: [0, 0, 0.5] -> [0, 0, 5] when scaled to [0, 10]
            self._fis_model.add_mf(variable_name, "output", "trojkatna")
            if self._fis_model._fis.Outputs:
                for var in self._fis_model._fis.Outputs:
                    if var.Name == variable_name and var.MembershipFunctions:
                        var.MembershipFunctions[0].Parameters = [0, 0, 0.5]
                        var.MembershipFunctions[0].Name = "low"
                        break

            # Medium: [0, 0.5, 1] -> [0, 5, 10] when scaled to [0, 10]
            self._fis_model.add_mf(variable_name, "output", "trojkatna")
            if self._fis_model._fis.Outputs:
                for var in self._fis_model._fis.Outputs:
                    if var.Name == variable_name and len(var.MembershipFunctions) >= 2:
                        var.MembershipFunctions[1].Parameters = [0, 0.5, 1]
                        var.MembershipFunctions[1].Name = "medium"
                        break

            # High: [0.5, 1, 1] -> [5, 10, 10] when scaled to [0, 10]
            self._fis_model.add_mf(variable_name, "output", "trojkatna")
            if self._fis_model._fis.Outputs:
                for var in self._fis_model._fis.Outputs:
                    if var.Name == variable_name and len(var.MembershipFunctions) >= 3:
                        var.MembershipFunctions[2].Parameters = [0.5, 1, 1]
                        var.MembershipFunctions[2].Name = "high"
                        break
        except Exception:
            pass

    def delete_input_variable(self, index: int) -> bool:
        """Delete an input variable by index.

        Args:
            index: Index of the input variable to delete.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            result = self._fis_model.delete_input(index)
            return result == 1
        except Exception:
            return False

    def delete_output_variable(self, index: int) -> bool:
        """Delete an output variable by index.

        Args:
            index: Index of the output variable to delete.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            result = self._fis_model.delete_output(index)
            return result == 1
        except Exception:
            return False

    def update_input_variable_range(self, index: int, range_min: float, range_max: float) -> bool:
        """Update the range of an input variable.

        Args:
            index: Index of the input variable.
            range_min: New minimum value of the range.
            range_max: New maximum value of the range.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            if 0 <= index < len(self._fis_model._fis.Inputs):
                self._fis_model._fis.Inputs[index].Range = [range_min, range_max]
                return True
            return False
        except Exception:
            return False

    def update_output_variable_range(self, index: int, range_min: float, range_max: float) -> bool:
        """Update the range of an output variable.

        Args:
            index: Index of the output variable.
            range_min: New minimum value of the range.
            range_max: New maximum value of the range.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            if 0 <= index < len(self._fis_model._fis.Outputs):
                self._fis_model._fis.Outputs[index].Range = [range_min, range_max]
                return True
            return False
        except Exception:
            return False

    def update_variable_name(self, variable_name: str, new_name: str, variable_type: str) -> bool:
        """Update the name of a variable.

        Args:
            variable_name: Current name of the variable.
            new_name: New name for the variable.
            variable_type: Type of variable ("input" or "output").

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            if variable_type == "input":
                for input_var in self._fis_model._fis.Inputs:
                    if input_var.Name == variable_name:
                        input_var.Name = new_name
                        return True
            elif variable_type == "output":
                for output_var in self._fis_model._fis.Outputs:
                    if output_var.Name == variable_name:
                        output_var.Name = new_name
                        return True
            return False
        except Exception:
            return False

    def get_variable_by_name(self, name: str, variable_type: str) -> Optional[object]:
        """Get a variable by name.

        Args:
            name: Name of the variable.
            variable_type: Type of variable ("input" or "output").

        Returns:
            The variable object if found, None otherwise.
        """
        try:
            if variable_type == "input":
                for input_var in self._fis_model._fis.Inputs:
                    if input_var.Name == name:
                        return input_var
            elif variable_type == "output":
                for output_var in self._fis_model._fis.Outputs:
                    if output_var.Name == name:
                        return output_var
            return None
        except Exception:
            return None
