from typing import Any, Dict, List, Optional

from PyQt6.QtCore import pyqtSignal

from app.view_models.base_view_model import BaseViewModel


class MFEditorViewModel(BaseViewModel):
    """View model for the membership function editor tab."""

    # Signals for membership function updates
    mf_list_updated = pyqtSignal(list)
    mf_selected = pyqtSignal(str, int)  # variable_name, mf_index
    mf_added = pyqtSignal(str, str, int)  # variable_name, mf_name, mf_index
    mf_deleted = pyqtSignal(str, int)  # variable_name, mf_index
    mf_type_changed = pyqtSignal(str, int, str)  # variable_name, mf_index, new_type

    # Signals for variable selection
    variable_selected = pyqtSignal(str, str)  # variable_name, variable_type

    # Signals for parameter updates
    mf_parameters_changed = pyqtSignal(
        str, int, list
    )  # variable_name, mf_index, new_parameters

    def __init__(self, model: Any = None) -> None:
        """Initialize the MFEditorViewModel.

        Args:
            model (Any): The FIS model instance.
        """
        super().__init__()
        self._model = model
        self._fuzzy_service = self.context.fuzzy_service
        self._selected_variable = None
        self._selected_variable_type = None
        self._selected_mf_index = -1
        self._available_mf_types = ["Triangle", "Trapezoid", "Gauss", "Bell"]
        self._default_parameters = "[0, 0.5, 1]"

    @property
    def model(self) -> Any:
        """Get the FIS model."""
        return self._model

    @model.setter
    def model(self, value: Any) -> None:
        """Set the FIS model and update data."""
        self._model = value
        self._update_mf_list()

    @property
    def selected_variable(self) -> Optional[str]:
        """Get the selected variable name."""
        return self._selected_variable

    @property
    def selected_variable_type(self) -> Optional[str]:
        """Get the selected variable type."""
        return self._selected_variable_type

    @property
    def selected_mf_index(self) -> int:
        """Get the selected membership function index."""
        return self._selected_mf_index

    @property
    def available_mf_types(self) -> List[str]:
        """Get the available membership function types."""
        return self._available_mf_types

    @property
    def default_parameters(self) -> str:
        """Get the default parameters string."""
        return self._default_parameters

    def _update_mf_list(self) -> None:
        """Update the membership function list from the model."""
        if not self._model or not hasattr(self._model, "_fis"):
            self.mf_list_updated.emit([])
            return

        fis = self._model._fis
        mf_list = []

        # Add input membership functions
        for input_var in fis.Inputs:
            for i, mf in enumerate(input_var.MembershipFunctions):
                mf_list.append(
                    {
                        "variable_name": input_var.Name,
                        "variable_type": "input",
                        "mf_index": i,
                        "mf_name": mf.Name,
                        "mf_type": mf.Type,
                        "parameters": mf.Parameters,
                    }
                )

        # Add output membership functions
        for output_var in fis.Outputs:
            for i, mf in enumerate(output_var.MembershipFunctions):
                mf_list.append(
                    {
                        "variable_name": output_var.Name,
                        "variable_type": "output",
                        "mf_index": i,
                        "mf_name": mf.Name,
                        "mf_type": mf.Type,
                        "parameters": mf.Parameters,
                    }
                )

        self.mf_list_updated.emit(mf_list)

    def select_variable(self, variable_name: str, variable_type: str) -> None:
        """Select a variable."""
        self._selected_variable = variable_name
        self._selected_variable_type = variable_type
        self.variable_selected.emit(variable_name, variable_type)
        self._update_mf_list()

    def select_mf(self, variable_name: str, mf_index: int) -> None:
        """Select a membership function."""
        self._selected_mf_index = mf_index
        self.mf_selected.emit(variable_name, mf_index)

    def add_mf(
        self,
        variable_name: str,
        mf_name: str,
        mf_type: str = "Triangle",
        mf_parameters: str = None,
    ) -> bool:
        """Add a new membership function."""
        if not self._selected_variable_type:
            return False

        # Map UI type names to model type names
        type_mapping = {
            "Triangle": "trojkatna",
            "Trapezoid": "trapezoidalna",
            "Gauss": "gaussowska",
            "Bell": "dzwonowa",
        }

        model_type = type_mapping.get(mf_type, "trojkatna")

        # Use the unified add_membership_function method
        # Parse parameters from the user input or use defaults
        if mf_parameters is None:
            mf_parameters = self._default_parameters
        parameters = self._parse_parameters(mf_parameters)

        success = self._fuzzy_service.add_membership_function(
            variable_name, mf_name, model_type, parameters
        )

        if success:
            # Get the index of the newly added MF
            fis = self._fuzzy_service.get_fis_model()._fis
            search_list = (
                fis.Inputs if self._selected_variable_type == "input" else fis.Outputs
            )

            for var in search_list:
                if var.Name == variable_name:
                    new_mf_index = len(var.MembershipFunctions) - 1
                    self.mf_added.emit(variable_name, mf_name, new_mf_index)
                    self._update_mf_list()
                    return True

        return False

    def delete_mf(self, variable_name: str, mf_index: int) -> bool:
        """Delete a membership function."""
        if not self._selected_variable_type:
            return False

        # Use the unified delete_membership_function method
        success = self._fuzzy_service.delete_membership_function(
            variable_name, mf_index
        )

        if success:
            self.mf_deleted.emit(variable_name, mf_index)
            self._update_mf_list()
            return True

        return False

    def change_mf_type(self, variable_name: str, mf_index: int, new_type: str) -> bool:
        """Change the type of a membership function."""
        if not self._selected_variable_type:
            return False

        # Map UI type names to model type names
        type_mapping = {
            "Triangle": "trojkatna",
            "Trapezoid": "trapezoidalna",
            "Gauss": "gaussowska",
            "Bell": "dzwonowa",
        }

        model_type = type_mapping.get(new_type, "trojkatna")

        success, message = self._fuzzy_service.change_membership_function_type(
            variable_name, self._selected_variable_type, mf_index, model_type
        )

        if success:
            self.mf_type_changed.emit(variable_name, mf_index, new_type)
            self._update_mf_list()
            return True

        return False

    def update_mf_parameters(
        self, variable_name: str, mf_index: int, new_parameters: List[float]
    ) -> bool:
        """Update the parameters of a membership function."""
        if not self._model or not hasattr(self._model, "_fis"):
            return False

        fis = self._model._fis
        search_list = (
            fis.Inputs if self._selected_variable_type == "input" else fis.Outputs
        )

        for var in search_list:
            if var.Name == variable_name and 0 <= mf_index < len(
                var.MembershipFunctions
            ):
                var.MembershipFunctions[mf_index].Parameters = new_parameters
                self.mf_parameters_changed.emit(variable_name, mf_index, new_parameters)
                return True

        return False

    def get_mf_info(self, variable_name: str, mf_index: int) -> Optional[Dict]:
        """Get information about a specific membership function."""
        if not self._model or not hasattr(self._model, "_fis"):
            return None

        fis = self._model._fis
        search_list = (
            fis.Inputs if self._selected_variable_type == "input" else fis.Outputs
        )

        for var in search_list:
            if var.Name == variable_name and 0 <= mf_index < len(
                var.MembershipFunctions
            ):
                mf = var.MembershipFunctions[mf_index]
                return {
                    "name": mf.Name,
                    "type": mf.Type,
                    "parameters": mf.Parameters,
                    "variable_name": variable_name,
                    "variable_type": self._selected_variable_type,
                }
        return None

    def get_variable_mfs(self, variable_name: str) -> List[Dict]:
        """Get all membership functions for a specific variable."""
        if not self._model or not hasattr(self._model, "_fis"):
            return []

        fis = self._model._fis
        search_list = (
            fis.Inputs if self._selected_variable_type == "input" else fis.Outputs
        )

        for var in search_list:
            if var.Name == variable_name:
                mfs = []
                for i, mf in enumerate(var.MembershipFunctions):
                    mfs.append(
                        {
                            "index": i,
                            "name": mf.Name,
                            "type": mf.Type,
                            "parameters": mf.Parameters,
                        }
                    )
                return mfs
        return []

    def get_mf_count(self, variable_name: str) -> int:
        """Get the count of membership functions for a variable."""
        mfs = self.get_variable_mfs(variable_name)
        return len(mfs)

    def refresh_data(self) -> None:
        """Refresh all data from the model."""
        self._update_mf_list()

    def add_mf_from_input(self, mf_name: str, mf_parameters: str) -> bool:
        """Add a membership function from user input with validation.

        Args:
            mf_name: The name entered by user (can be empty)
            mf_parameters: The parameters entered by user (can be empty)

        Returns:
            True if successful, False otherwise
        """
        # Validate and set defaults
        if not mf_name.strip():
            mf_name = "New MF"
        else:
            mf_name = mf_name.strip()

        if not mf_parameters.strip():
            mf_parameters = self._default_parameters
        else:
            mf_parameters = mf_parameters.strip()

        # Check if variable is selected
        if not self._selected_variable:
            return False

        # Call the existing add_mf method with parameters
        return self.add_mf(self._selected_variable, mf_name, "Triangle", mf_parameters)

    def delete_mf_from_selection(self, mf_index: int) -> bool:
        """Delete a membership function by index with validation.

        Args:
            mf_index: The index of the MF to delete

        Returns:
            True if successful, False otherwise
        """
        # Validate inputs
        if not self._selected_variable or mf_index < 0:
            return False

        # Call the existing delete_mf method
        return self.delete_mf(self._selected_variable, mf_index)

    def _parse_parameters(self, parameters_str: str) -> List[float]:
        """Parse parameters string into a list of floats.

        Args:
            parameters_str: String like "[0, 0.5, 1]" or "0, 0.5, 1"

        Returns:
            List of float parameters
        """
        try:
            # Remove brackets if present
            clean_str = parameters_str.strip().strip("[]")

            # Split by comma and convert to floats
            params = [float(x.strip()) for x in clean_str.split(",")]

            # Validate parameter count based on MF type
            if len(params) < 2:
                return [0, 0.5, 1]  # Default triangle parameters

            return params

        except (ValueError, AttributeError):
            return [0, 0.5, 1]  # Default triangle parameters

    def get_available_variables(self) -> list:
        """Get list of available variables for selection.

        Returns:
            List of dictionaries with variable info:
            [{"name": str, "type": str, "display": str}, ...]
        """
        variables = []

        if not self._model or not hasattr(self._model, "_fis"):
            return variables

        fis = self._model._fis

        # Add input variables
        for input_var in fis.Inputs:
            variables.append(
                {
                    "name": input_var.Name,
                    "type": "input",
                    "display": f"[Input] {input_var.Name}",
                }
            )

        # Add output variables
        for output_var in fis.Outputs:
            variables.append(
                {
                    "name": output_var.Name,
                    "type": "output",
                    "display": f"[Output] {output_var.Name}",
                }
            )

        return variables

    def select_variable_from_display_text(self, display_text: str) -> bool:
        """Select a variable from display text.

        Args:
            display_text: Display text like "[Input] variable_name" or
                "[Output] variable_name"

        Returns:
            True if selection was successful, False otherwise
        """
        if "No variables available" in display_text:
            return False

        # Parse the display text to get variable name and type
        if "[Input]" in display_text:
            variable_name = display_text.replace("[Input] ", "")
            variable_type = "input"
        elif "[Output]" in display_text:
            variable_name = display_text.replace("[Output] ", "")
            variable_type = "output"
        else:
            return False

        # Use existing select_variable method
        self.select_variable(variable_name, variable_type)
        return True
