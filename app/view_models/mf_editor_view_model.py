from typing import Dict, List, Optional

from PyQt6.QtCore import pyqtSignal

from app.view_models.base_view_model import BaseViewModel


class MFEditorViewModel(BaseViewModel):
    """View model for the membership function editor tab."""

    mf_list_updated = pyqtSignal(list)
    mf_selected = pyqtSignal(str, int)  # variable_name, mf_index
    mf_added = pyqtSignal(str, str, int)  # variable_name, mf_name, mf_index
    mf_deleted = pyqtSignal(str, int)  # variable_name, mf_index
    mf_type_changed = pyqtSignal(str, int, str)  # variable_name, mf_index, new_type

    variable_selected = pyqtSignal(str, str)  # variable_name, variable_type

    mf_parameters_changed = pyqtSignal(str, int, list)  # variable_name, mf_index, new_parameters

    def __init__(self) -> None:
        """Initialize the MFEditorViewModel."""
        super().__init__()
        self._fuzzy_service = None
        self._selected_variable = None
        self._selected_variable_type = None
        self._selected_mf_index = -1
        self._available_mf_types = ["Triangle", "Trapezoid", "Gauss", "Bell"]
        self._default_parameters = "[0, 0.5, 1]"
        self._updating = False

    def set_fuzzy_service(self, fuzzy_service) -> None:
        """Set the fuzzy calculation service."""
        self._fuzzy_service = fuzzy_service

    def _emit_system_changed(self) -> None:
        """Emit notify_data_changed signal to notify other components."""
        if self._updating:
            return
        self._updating = True
        try:
            self.notify_data_changed.emit()
        finally:
            self._updating = False

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
        # Check if this is a Sugeno system output
        is_sugeno_output = False
        if self._model and hasattr(self._model, "_fis"):
            from fuzzylab import sugfis

            if isinstance(self._model._fis, sugfis) and self._selected_variable_type == "output":
                is_sugeno_output = True

        if is_sugeno_output:
            return ["Constant", "Linear"]
        return self._available_mf_types

    @property
    def default_parameters(self) -> str:
        """Get the default parameters string."""
        # Check if this is a Sugeno system output
        is_sugeno_output = False
        if self._model and hasattr(self._model, "_fis"):
            from fuzzylab import sugfis

            if isinstance(self._model._fis, sugfis) and self._selected_variable_type == "output":
                is_sugeno_output = True

        if is_sugeno_output:
            return "0.5"  # Default constant value for Sugeno
        return self._default_parameters

    def _update_mf_list(self) -> None:
        """Update the membership function list from the model."""
        if not self._model or not hasattr(self._model, "_fis"):
            self.mf_list_updated.emit([])
            return

        if not self._selected_variable or not self._selected_variable_type:
            self.mf_list_updated.emit([])
            return

        fis = self._model._fis
        mf_list = []

        if self._selected_variable_type == "input":
            var_list = fis.Inputs
        else:
            var_list = fis.Outputs

        selected_var = None
        for var in var_list:
            if var.Name == self._selected_variable:
                selected_var = var
                break

        if selected_var:
            # Check if this is a Sugeno system output
            is_sugeno_output = False
            if self._model and hasattr(self._model, "_fis"):
                from fuzzylab import sugfis

                if isinstance(self._model._fis, sugfis) and self._selected_variable_type == "output":
                    is_sugeno_output = True

            library_to_ui_mapping = {
                "trimf": "Triangle",
                "trapmf": "Trapezoid",
                "gaussmf": "Gauss",
                "gbellmf": "Bell",
            }

            # Sugeno output MF types
            if is_sugeno_output:
                library_to_ui_mapping.update(
                    {
                        "constant": "Constant",
                        "linear": "Linear",
                    }
                )

            for i, mf in enumerate(selected_var.MembershipFunctions):
                ui_type = library_to_ui_mapping.get(mf.Type, "Triangle")
                # Handle constant type - parameters might be a single float
                params = mf.Parameters
                if mf.Type == "constant" and isinstance(params, (int, float)):
                    params = [float(params)]  # Convert to list for consistency
                elif mf.Type == "constant" and isinstance(params, list) and len(params) == 1:
                    params = params  # Already a list
                elif mf.Type == "constant":
                    params = [0.5]  # Default fallback

                mf_list.append(
                    {
                        "variable_name": selected_var.Name,
                        "variable_type": self._selected_variable_type,
                        "mf_index": i,
                        "mf_name": mf.Name,
                        "mf_type": ui_type,
                        "parameters": params,
                    }
                )

        self.mf_list_updated.emit(mf_list)

    def select_variable(self, variable_name: str, variable_type: str) -> None:
        """Select a variable."""
        self._selected_variable = variable_name
        self._selected_variable_type = variable_type
        self.variable_selected.emit(variable_name, variable_type)
        # Update MF list after variable selection to ensure table is redrawn
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

        # Check if this is a Sugeno system output
        is_sugeno_output = False
        if self._model and hasattr(self._model, "_fis"):
            from fuzzylab import sugfis

            if isinstance(self._model._fis, sugfis) and self._selected_variable_type == "output":
                is_sugeno_output = True

        if is_sugeno_output:
            type_mapping = {
                "Constant": "stala",
                "Linear": "liniowa",
            }
            model_type = type_mapping.get(mf_type, "stala")
        else:
            type_mapping = {
                "Triangle": "trojkatna",
                "Trapezoid": "trapezoidalna",
                "Gauss": "gaussowska",
                "Bell": "dzwonowa",
            }
            model_type = type_mapping.get(mf_type, "trojkatna")

        if mf_parameters is None:
            mf_parameters = self._default_parameters
        parameters = self._parse_parameters(mf_parameters)

        success = self._fuzzy_service.add_membership_function(variable_name, mf_name, model_type, parameters)

        if success:
            fis = self._fuzzy_service.get_fis_model()._fis
            search_list = fis.Inputs if self._selected_variable_type == "input" else fis.Outputs

            for var in search_list:
                if var.Name == variable_name:
                    new_mf_index = len(var.MembershipFunctions) - 1
                    self.mf_added.emit(variable_name, mf_name, new_mf_index)
                    self._update_mf_list()
                    # Notify other components of data change
                    self.notify_data_changed.emit()
                    return True

        return False

    def delete_mf(self, variable_name: str, mf_index: int) -> bool:
        """Delete a membership function."""
        if not self._selected_variable_type:
            return False

        success = self._fuzzy_service.delete_membership_function(variable_name, mf_index, self._selected_variable_type)

        if success:
            if self._fuzzy_service and hasattr(self._fuzzy_service, "get_fis_model"):
                self._model = self._fuzzy_service.get_fis_model()
            self.mf_deleted.emit(variable_name, mf_index)
            self._update_mf_list()
            self.notify_data_changed.emit()
            return True

        return False

    def change_mf_type(self, variable_name: str, mf_index: int, new_type: str) -> bool:
        """Change the type of a membership function."""
        if not self._selected_variable_type:
            return False

        mf_info = self.get_mf_info(variable_name, mf_index)
        if mf_info and mf_info["type"] == new_type:
            # If already the correct type, check if parameters need updating
            expected_params = self.get_default_parameters_for_type(new_type)
            current_params = mf_info["parameters"]
            # Always update to ensure parameters are properly scaled to variable range
            if len(current_params) != len(expected_params):
                # Parameter count changed, definitely update
                self.update_mf_parameters(variable_name, mf_index, expected_params)
                self._update_mf_list()
                self._emit_system_changed()
            return True

        # Check if this is a Sugeno system output
        is_sugeno_output = False
        if self._model and hasattr(self._model, "_fis"):
            from fuzzylab import sugfis

            if isinstance(self._model._fis, sugfis) and self._selected_variable_type == "output":
                is_sugeno_output = True

        if is_sugeno_output:
            type_mapping = {
                "Constant": "stala",
                "Linear": "liniowa",
            }
            model_type = type_mapping.get(new_type, "stala")
        else:
            type_mapping = {
                "Triangle": "trojkatna",
                "Trapezoid": "trapezoidalna",
                "Gauss": "gaussowska",
                "Bell": "dzwonowa",
            }
            model_type = type_mapping.get(new_type, "trojkatna")

        success = self._fuzzy_service.change_membership_function_type(
            variable_name, self._selected_variable_type, mf_index, model_type
        )

        if success:
            expected_params = self.get_default_parameters_for_type(new_type)
            self.update_mf_parameters(variable_name, mf_index, expected_params)

            self.mf_type_changed.emit(variable_name, mf_index, new_type)
            self._update_mf_list()
            self._emit_system_changed()
            return True

        return False

    def update_mf_parameters(self, variable_name: str, mf_index: int, new_parameters: List[float]) -> bool:
        """Update the parameters of a membership function."""
        if not self._model or not hasattr(self._model, "_fis"):
            return False

        fis = self._model._fis
        search_list = fis.Inputs if self._selected_variable_type == "input" else fis.Outputs

        for var in search_list:
            if var.Name == variable_name and 0 <= mf_index < len(var.MembershipFunctions):
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

                self.mf_parameters_changed.emit(variable_name, mf_index, new_parameters)
                self._emit_system_changed()
                # Notify other components of data change
                self.notify_data_changed.emit()
                return True

        return False

    def get_mf_info(self, variable_name: str, mf_index: int) -> Optional[Dict]:
        """Get information about a specific membership function."""
        if not self._model or not hasattr(self._model, "_fis"):
            return None

        fis = self._model._fis
        search_list = fis.Inputs if self._selected_variable_type == "input" else fis.Outputs

        for var in search_list:
            if var.Name == variable_name and 0 <= mf_index < len(var.MembershipFunctions):
                mf = var.MembershipFunctions[mf_index]

                # Check if this is a Sugeno system output
                is_sugeno_output = False
                if hasattr(fis, "__class__"):
                    from fuzzylab import sugfis

                    if isinstance(fis, sugfis) and self._selected_variable_type == "output":
                        is_sugeno_output = True

                library_to_ui_mapping = {
                    "trimf": "Triangle",
                    "trapmf": "Trapezoid",
                    "gaussmf": "Gauss",
                    "gbellmf": "Bell",
                }

                if is_sugeno_output:
                    library_to_ui_mapping.update(
                        {
                            "constant": "Constant",
                            "linear": "Linear",
                        }
                    )

                ui_type = library_to_ui_mapping.get(mf.Type, "Triangle")

                # Handle constant type - parameters might be a single float
                params = mf.Parameters
                if mf.Type == "constant" and isinstance(params, (int, float)):
                    params = [float(params)]  # Convert to list for consistency
                elif mf.Type == "constant" and isinstance(params, list) and len(params) == 1:
                    params = params  # Already a list
                elif mf.Type == "constant":
                    params = [0.5]  # Default fallback

                return {
                    "name": mf.Name,
                    "type": ui_type,
                    "parameters": params,
                    "variable_name": variable_name,
                    "variable_type": self._selected_variable_type,
                }
        return None

    def get_variable_mfs(self, variable_name: str) -> List[Dict]:
        """Get all membership functions for a specific variable."""
        if not self._model or not hasattr(self._model, "_fis"):
            return []

        fis = self._model._fis
        search_list = fis.Inputs if self._selected_variable_type == "input" else fis.Outputs

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
        """Refresh all data from the model - only updates logic, no signal emission."""
        self._update_mf_list()

    def add_mf_from_input(self, mf_name: str, mf_parameters: str) -> bool:
        """Add a membership function from user input with validation.

        Args:
            mf_name: The name entered by user (can be empty)
            mf_parameters: The parameters entered by user (can be empty)

        Returns:
            True if successful, False otherwise
        """
        if not mf_name.strip():
            mf_name = "New MF"
        else:
            mf_name = mf_name.strip()

        if not mf_parameters.strip():
            mf_parameters = self._default_parameters
        else:
            mf_parameters = mf_parameters.strip()

        if not self._selected_variable:
            return False

        return self.add_mf(self._selected_variable, mf_name, "Triangle", mf_parameters)

    def delete_mf_from_selection(self, mf_index: int) -> bool:
        """Delete a membership function by index with validation.

        Args:
            mf_index: The index of the MF to delete

        Returns:
            True if successful, False otherwise
        """
        if not self._selected_variable or mf_index < 0:
            return False

        return self.delete_mf(self._selected_variable, mf_index)

    def get_default_parameters_for_type(self, mf_type: str) -> List[float]:
        """Get appropriate default parameters for a membership function type.

        Args:
            mf_type: The membership function type (UI name)

        Returns:
            List of default parameters for the type, scaled to variable range
        """
        var_range = self._get_current_variable_range()
        if not var_range:
            var_range = [0, 1]

        range_min, range_max = var_range[0], var_range[1]
        range_span = range_max - range_min

        # Check if this is a Sugeno system output
        is_sugeno_output = False
        if self._model and hasattr(self._model, "_fis"):
            from fuzzylab import sugfis

            if isinstance(self._model._fis, sugfis) and self._selected_variable_type == "output":
                is_sugeno_output = True

        # Default parameters in normalized [0, 1] space
        defaults_normalized = {
            "Triangle": [0, 0.5, 1],  # 3 parameters: a, b, c
            "Trapezoid": [0, 0.3, 0.7, 1],  # 4 parameters: a, b, c, d
            "Gauss": [0.2, 0.5],  # 2 parameters: sigma, mu (order matters!)
            "Bell": [0.2, 3, 0.5],  # 3 parameters: a (width), b (slope), c (center)
        }

        # Sugeno output types
        if is_sugeno_output:
            if mf_type == "Constant":
                # Constant type: single float value
                return [0.5]  # Return as list for consistency
            elif mf_type == "Linear":
                # Linear type: coefficients for inputs + constant term
                # For n inputs: [coeff1, coeff2, ..., coeffn, constant]
                input_count = len(self._model._fis.Inputs) if self._model and hasattr(self._model, "_fis") else 2
                # Default: all coefficients 0, constant 0.5
                return [0.0] * input_count + [0.5]

        normalized = defaults_normalized.get(mf_type, [0, 0.5, 1])

        # Scale parameters to actual variable range
        # For Gauss and Bell: only scale position parameters, not shape parameters
        if mf_type == "Gauss":
            # sigma (width) scales with range span, mu (center) scales to range
            return [
                round(normalized[0] * range_span, 2),  # sigma
                round(range_min + normalized[1] * range_span, 2),  # mu
            ]
        elif mf_type == "Bell":
            # a (width) scales with range span, b (slope) stays constant, c (center) scales to range
            return [
                round(normalized[0] * range_span, 2),  # a (width)
                normalized[1],  # b (slope) - dimensionless
                round(range_min + normalized[2] * range_span, 2),  # c (center)
            ]
        else:
            # Triangle and Trapezoid: all parameters are positions, scale to range
            return [round(range_min + p * range_span, 2) for p in normalized]

    def _get_current_variable_range(self) -> Optional[List[float]]:
        """Get the range of the currently selected variable.

        Returns:
            [min, max] or None if no variable selected
        """
        if not self._model or not hasattr(self._model, "_fis"):
            return None

        if not self._selected_variable or not self._selected_variable_type:
            return None

        fis = self._model._fis
        search_list = fis.Inputs if self._selected_variable_type == "input" else fis.Outputs

        for var in search_list:
            if var.Name == self._selected_variable:
                return var.Range

        return None

    def _parse_parameters(self, parameters_str: str) -> List[float]:
        """Parse parameters string into a list of floats.

        Args:
            parameters_str: String like "[0, 0.5, 1]" or "0, 0.5, 1"

        Returns:
            List of float parameters
        """
        try:
            clean_str = parameters_str.strip().strip("[]")

            params = [float(x.strip()) for x in clean_str.split(",")]

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

        for input_var in fis.Inputs:
            variables.append(
                {
                    "name": input_var.Name,
                    "type": "input",
                    "display": f"[Input] {input_var.Name}",
                }
            )

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

        if "[Input]" in display_text:
            variable_name = display_text.replace("[Input] ", "")
            variable_type = "input"
        elif "[Output]" in display_text:
            variable_name = display_text.replace("[Output] ", "")
            variable_type = "output"
        else:
            return False

        self.select_variable(variable_name, variable_type)
        return True
