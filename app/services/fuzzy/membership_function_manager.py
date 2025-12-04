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
                        # Normalize constant type parameters to list format
                        params = mf.Parameters
                        if mf.Type == "constant" and isinstance(params, (int, float)):
                            params = [float(params)]
                        elif mf.Type == "constant" and isinstance(params, list) and len(params) == 1:
                            params = params
                        elif mf.Type == "constant":
                            params = [0.5]

                        mfs.append(
                            {
                                "index": i,
                                "name": mf.Name,
                                "type": mf.Type,
                                "parameters": params,
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
                    result = self._fis_model.add_mf(variable_name, variable_type, mf_type)

                    if result == 1:
                        if len(var.MembershipFunctions) > 0:
                            new_mf = var.MembershipFunctions[-1]  # Get the last (newly added) MF
                            new_mf.Name = mf_name
                            # Handle Sugeno constant type - needs single float, not list
                            if new_mf.Type == "constant":
                                if isinstance(parameters, list) and len(parameters) > 0:
                                    new_mf.Parameters = float(parameters[0])
                                elif isinstance(parameters, (int, float)):
                                    new_mf.Parameters = float(parameters)
                                else:
                                    new_mf.Parameters = 0.5  # Default fallback
                            else:
                                new_mf.Parameters = parameters
                        return True
                    return False
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
            result = self._fis_model.delete_mf(variable_name, variable_type, mf_index)
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
            # FIS model expects: io_variable_name, input_or_output, mf_idx, new_mf_type
            result = self._fis_model.change_mf_type(variable_name, variable_type, mf_index, new_type)
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
                        mf = var.MembershipFunctions[mf_index]
                        # Handle Sugeno constant type - needs single float, not list
                        if mf.Type == "constant":
                            if isinstance(new_parameters, list) and len(new_parameters) > 0:
                                mf.Parameters = float(new_parameters[0])
                            elif isinstance(new_parameters, (int, float)):
                                mf.Parameters = float(new_parameters)
                            else:
                                mf.Parameters = 0.5  # Default fallback
                        else:
                            mf.Parameters = new_parameters
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
                        # Normalize constant type parameters to list format
                        params = mf.Parameters
                        if mf.Type == "constant" and isinstance(params, (int, float)):
                            params = [float(params)]
                        elif mf.Type == "constant" and isinstance(params, list) and len(params) == 1:
                            params = params
                        elif mf.Type == "constant":
                            params = [0.5]

                        return {
                            "name": mf.Name,
                            "type": mf.Type,
                            "parameters": params,
                            "variable_name": variable_name,
                            "variable_type": variable_type,
                        }
            return None
        except Exception:
            return None
