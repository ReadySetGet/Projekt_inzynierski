from typing import Dict, List, Optional

from PyQt6.QtCore import pyqtSignal

from app.view_models.base_view_model import BaseViewModel


class FisPropertiesViewModel(BaseViewModel):
    """View model for the FIS properties tab view."""

    # Signals for FIS system updates
    fis_system_updated = pyqtSignal()
    system_name_changed = pyqtSignal(str)
    system_type_changed = pyqtSignal(str)

    # Signals for input/output management
    input_added = pyqtSignal(str, int)  # input_name, input_index
    input_deleted = pyqtSignal(int)  # input_index
    output_added = pyqtSignal(str, int)  # output_name, output_index
    output_deleted = pyqtSignal(int)  # output_index

    # Signals for variable selection
    variable_selected = pyqtSignal(str, str)  # variable_name, variable_type

    def __init__(self) -> None:
        """Initialize the FisPropertiesViewModel."""
        super().__init__()
        self._system_name = "fis"
        self._system_type = "mamfis"  # mamfis or sugfis
        self._selected_variable = None
        self._selected_variable_type = None

    @property
    def system_name(self) -> str:
        """Get the system name."""
        return self._system_name

    @system_name.setter
    def system_name(self, value: str) -> None:
        """Set the system name."""
        if self._system_name != value:
            self._system_name = value
            self.system_name_changed.emit(value)

    @property
    def system_type(self) -> str:
        """Get the system type."""
        return self._system_type

    @system_type.setter
    def system_type(self, value: str) -> None:
        """Set the system type."""
        if self._system_type != value:
            self._system_type = value
            self.system_type_changed.emit(value)

    @property
    def inputs(self) -> List[Dict]:
        """Get the input variables."""
        fis_model = self.fuzzy_service.get_fis_model()
        if not fis_model or not hasattr(fis_model, "_fis"):
            return []

        inputs = []
        for i, input_var in enumerate(fis_model._fis.Inputs):
            inputs.append(
                {
                    "index": i,
                    "name": input_var.Name,
                    "range": input_var.Range,
                    "mf_count": len(input_var.MembershipFunctions),
                }
            )
        return inputs

    @property
    def outputs(self) -> List[Dict]:
        """Get the output variables."""
        fis_model = self.fuzzy_service.get_fis_model()
        if not fis_model or not hasattr(fis_model, "_fis"):
            return []

        outputs = []
        for i, output_var in enumerate(fis_model._fis.Outputs):
            outputs.append(
                {
                    "index": i,
                    "name": output_var.Name,
                    "range": output_var.Range,
                    "mf_count": len(output_var.MembershipFunctions),
                }
            )
        return outputs

    @property
    def selected_variable(self) -> Optional[str]:
        """Get the selected variable name."""
        return self._selected_variable

    @property
    def selected_variable_type(self) -> Optional[str]:
        """Get the selected variable type."""
        return self._selected_variable_type

    def _update_system_info(self) -> None:
        """Update system information from the fuzzy service."""
        fis_model = self.fuzzy_service.get_fis_model()
        if not fis_model or not hasattr(fis_model, "_fis"):
            return

        fis = fis_model._fis

        if hasattr(fis, "Name") and fis.Name:
            self.system_name = fis.Name

        if hasattr(fis, "__class__"):
            if "mamfis" in str(fis.__class__).lower():
                self.system_type = "mamfis"
            elif "sugfis" in str(fis.__class__).lower():
                self.system_type = "sugfis"

        self.fis_system_updated.emit()

    def add_input(self) -> None:
        """Add a new input variable."""
        # Use fuzzy_service method to match TopMenu functionality
        input_count = self.fuzzy_service.get_input_count()
        success = self.fuzzy_service.add_input_variable(f"input{input_count + 1}", 0.0, 1.0)
        if success:
            self._update_system_info()
            fis_model = self.fuzzy_service.get_fis_model()
            if fis_model and fis_model._fis.Inputs:
                new_input = fis_model._fis.Inputs[-1]
                self.input_added.emit(new_input.Name, len(fis_model._fis.Inputs) - 1)
            self.notify_data_changed.emit()

    def delete_input(self, input_index: int) -> None:
        """Delete an input variable."""
        fis_model = self.fuzzy_service.get_fis_model()
        if fis_model and 0 <= input_index < len(fis_model._fis.Inputs):
            result = fis_model.delete_input(input_index)
            if result == 1:  # Success
                self.input_deleted.emit(input_index)
                self._update_system_info()
                # Notify other components of data change
                self.notify_data_changed.emit()

    def add_output(self) -> None:
        """Add a new output variable."""
        # Use fuzzy_service method to match TopMenu functionality
        output_count = self.fuzzy_service.get_output_count()
        success = self.fuzzy_service.add_output_variable(f"output{output_count + 1}", 0.0, 1.0)
        if success:
            self._update_system_info()
            fis_model = self.fuzzy_service.get_fis_model()
            if fis_model and fis_model._fis.Outputs:
                new_output = fis_model._fis.Outputs[-1]
                self.output_added.emit(new_output.Name, len(fis_model._fis.Outputs) - 1)
            self.notify_data_changed.emit()

    def delete_output(self, output_index: int) -> None:
        """Delete an output variable."""
        fis_model = self.fuzzy_service.get_fis_model()
        if fis_model and 0 <= output_index < len(fis_model._fis.Outputs):
            result = fis_model.delete_output(output_index)
            if result == 1:  # Success
                self.output_deleted.emit(output_index)
                self._update_system_info()
                # Notify other components of data change
                self.notify_data_changed.emit()

    def select_variable(self, variable_name: str, variable_type: str) -> None:
        """Select a variable."""
        self._selected_variable = variable_name
        self._selected_variable_type = variable_type
        self.variable_selected.emit(variable_name, variable_type)

    def get_variable_info(self, variable_name: str, variable_type: str) -> Optional[Dict]:
        """Get information about a specific variable."""
        fis_model = self.fuzzy_service.get_fis_model()
        if not fis_model or not hasattr(fis_model, "_fis"):
            return None

        fis = fis_model._fis
        search_list = fis.Inputs if variable_type == "input" else fis.Outputs

        for var in search_list:
            if var.Name == variable_name:
                return {
                    "name": var.Name,
                    "range": var.Range,
                    "mf_count": len(var.MembershipFunctions),
                    "membership_functions": [
                        {"name": mf.Name, "type": mf.Type, "parameters": mf.Parameters}
                        for mf in var.MembershipFunctions
                    ],
                }
        return None

    def update_variable_range(self, variable_name: str, variable_type: str, new_range: List[float]) -> bool:
        """Update the range of a variable."""
        fis_model = self.fuzzy_service.get_fis_model()
        if not fis_model or not hasattr(fis_model, "_fis"):
            return False

        fis = fis_model._fis
        search_list = fis.Inputs if variable_type == "input" else fis.Outputs

        for var in search_list:
            if var.Name == variable_name:
                var.Range = new_range
                self._update_system_info()
                return True
        return False

    def refresh_data(self) -> None:
        """Refresh all data from the model."""
        self._update_system_info()

    def convert_inference_system(self) -> bool:
        """Convert the FIS system from Mamdani to Sugeno or vice versa."""
        success = self.fuzzy_service.convert_inference_system()
        if success:
            self._update_system_info()
            self.notify_data_changed.emit()
        return success

    def get_fis_type_display(self) -> str:
        """Get the current FIS type for display (Mamdani or Sugeno)."""
        fis_type = self.fuzzy_service.get_fis_type()
        if fis_type == "mamdani":
            return "Mamdani"
        elif fis_type == "sugeno":
            return "Sugeno"
        return "Mamdani"  # Default

    def get_defuzzification_method(self) -> str:
        """Get the current defuzzification method."""
        return self.fuzzy_service.get_defuzzification_method()

    def set_defuzzification_method(self, method: str) -> bool:
        """Set the defuzzification method."""
        success = self.fuzzy_service.set_defuzzification_method(method)
        if success:
            self.notify_data_changed.emit()
        return success

    def get_available_defuzzification_methods(self) -> List[str]:
        """Get available defuzzification methods based on FIS type."""
        fis_type = self.fuzzy_service.get_fis_type()
        if fis_type == "sugeno":
            return ["wtaver"]
        return ["centroid", "bisector", "mom", "som", "lom"]
