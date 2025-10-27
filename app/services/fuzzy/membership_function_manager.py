"""Membership Function Manager for managing FIS membership functions."""

from typing import Dict, List, Optional

from app.models.fis_model import FISModel


class MembershipFunctionManager:
    """Manages FIS membership functions."""

    def __init__(self, fis_model: FISModel) -> None:
        """Initialize the Membership Function Manager.

        Args:
            fis_model: The FIS model to manage membership functions for.
        """
        self._fis_model = fis_model

    def get_membership_functions(self, variable_name: str, variable_type: str) -> List[Dict[str, any]]:
        """Get membership functions for a specific variable.

        Args:
            variable_name: Name of the variable.
            variable_type: Type of variable ("input" or "output").

        Returns:
            List of dictionaries containing membership function information.
        """
        mfs = []
        try:
            if variable_type == "input":
                var_list = self._fis_model._fis.Inputs
            else:
                var_list = self._fis_model._fis.Outputs

            for var in var_list:
                if var.Name == variable_name:
                    for i, mf in enumerate(var.MembershipFunctions):
                        mfs.append(
                            {
                                "index": i,
                                "name": mf.Name,
                                "type": mf.Type,
                                "parameters": mf.Parameters,
                            }
                        )
                    break
        except Exception:
            pass
        return mfs

    def add_membership_function(
        self,
        variable_name: str,
        mf_name: str,
        mf_type: str,
        parameters: List[float],
        variable_type: str,
    ) -> bool:
        """Add a new membership function to a variable.

        Args:
            variable_name: Name of the variable.
            mf_name: Name of the membership function.
            mf_type: Type of membership function.
            parameters: Parameters for the membership function.
            variable_type: Type of variable ("input" or "output").

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            if variable_type == "input":
                var_list = self._fis_model._fis.Inputs
            else:
                var_list = self._fis_model._fis.Outputs

            for var in var_list:
                if var.Name == variable_name:
                    # Add the membership function using the FIS model
                    result = self._fis_model.add_mf(variable_name, mf_name, mf_type, parameters, variable_type)
                    return result == 1
            return False
        except Exception:
            return False

    def delete_membership_function(self, variable_name: str, mf_index: int, variable_type: str) -> bool:
        """Delete a membership function from a variable.

        Args:
            variable_name: Name of the variable.
            mf_index: Index of the membership function to delete.
            variable_type: Type of variable ("input" or "output").

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            result = self._fis_model.delete_mf(variable_name, mf_index, variable_type)
            return result == 1
        except Exception:
            return False

    def change_membership_function_type(
        self,
        variable_name: str,
        mf_index: int,
        new_type: str,
        variable_type: str,
    ) -> bool:
        """Change the type of a membership function.

        Args:
            variable_name: Name of the variable.
            mf_index: Index of the membership function.
            new_type: New type for the membership function.
            variable_type: Type of variable ("input" or "output").

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            result = self._fis_model.change_mf_type(variable_name, mf_index, new_type, variable_type)
            return result == 1
        except Exception:
            return False

    def update_membership_function_parameters(
        self,
        variable_name: str,
        mf_index: int,
        new_parameters: List[float],
        variable_type: str,
    ) -> bool:
        """Update the parameters of a membership function.

        Args:
            variable_name: Name of the variable.
            mf_index: Index of the membership function.
            new_parameters: New parameters for the membership function.
            variable_type: Type of variable ("input" or "output").

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            if variable_type == "input":
                var_list = self._fis_model._fis.Inputs
            else:
                var_list = self._fis_model._fis.Outputs

            for var in var_list:
                if var.Name == variable_name:
                    if 0 <= mf_index < len(var.MembershipFunctions):
                        var.MembershipFunctions[mf_index].Parameters = new_parameters
                        return True
            return False
        except Exception:
            return False

    def update_membership_function_name(
        self,
        variable_name: str,
        mf_index: int,
        new_name: str,
        variable_type: str,
    ) -> bool:
        """Update the name of a membership function.

        Args:
            variable_name: Name of the variable.
            mf_index: Index of the membership function.
            new_name: New name for the membership function.
            variable_type: Type of variable ("input" or "output").

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            if variable_type == "input":
                var_list = self._fis_model._fis.Inputs
            else:
                var_list = self._fis_model._fis.Outputs

            for var in var_list:
                if var.Name == variable_name:
                    if 0 <= mf_index < len(var.MembershipFunctions):
                        var.MembershipFunctions[mf_index].Name = new_name
                        return True
            return False
        except Exception:
            return False

    def get_membership_function_info(
        self,
        variable_name: str,
        mf_index: int,
        variable_type: str,
    ) -> Optional[Dict[str, any]]:
        """Get information about a specific membership function.

        Args:
            variable_name: Name of the variable.
            mf_index: Index of the membership function.
            variable_type: Type of variable ("input" or "output").

        Returns:
            Dictionary containing membership function information, or None if not found.
        """
        try:
            if variable_type == "input":
                var_list = self._fis_model._fis.Inputs
            else:
                var_list = self._fis_model._fis.Outputs

            for var in var_list:
                if var.Name == variable_name:
                    if 0 <= mf_index < len(var.MembershipFunctions):
                        mf = var.MembershipFunctions[mf_index]
                        return {
                            "name": mf.Name,
                            "type": mf.Type,
                            "parameters": mf.Parameters,
                            "variable_name": variable_name,
                            "variable_type": variable_type,
                        }
            return None
        except Exception:
            return None
