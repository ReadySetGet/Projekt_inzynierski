from PyQt6 import QtCore, QtWidgets

from app.view_models.mf_editor_view_model import MFEditorViewModel
from app.views.base_widget_view import BaseWidgetView


class MFPropertiesWidget(BaseWidgetView):
    """Class inheriting from QWidget.

    Allows user interaction via QPushButton, QLineEdit and QComboBox GUI elements.
    The current membership functions in the system are displayed within the table.

    Methods:
        __init__(QtWidgets.*): create an instance of MFPropertiesWidget and bind it
            to the parent window.

    Attributes:
        remove_mf_clicked: pyqtSignal which gets emitted to backend when
            remove_mf_button is clicked.
        add_mf_clicked: pyqtSignal which gets emitted to backend when
            add_mf_button is clicked.
        default_parameters: default parameters of a new function.
    """

    remove_mf_clicked = QtCore.pyqtSignal()
    add_mf_clicked = QtCore.pyqtSignal()

    def __init__(self, qss_filename=None, parent=None):
        """Initialize a new class instance.

        Args:
            qss_filename (str, optional): Optional QSS file for styling.
                Defaults to None.
            parent (QWidget, optional): The parent widget, in this case editor
                tab, to which the widget will be attached. Defaults to None.
        """
        super().__init__(qss_filename=qss_filename, parent=parent)
        self.setObjectName("mf_properties_tab")

        self._updating_type = False
        self._desired_types = {}

        self.view_model = MFEditorViewModel()
        self.view_model.setParent(self)
        self.set_view_model(self.view_model)

        self.fuzzy_service = self.view_model.fuzzy_service
        fis_model = self.fuzzy_service.get_fis_model()
        self.view_model.model = fis_model

        self.view_model.set_fuzzy_service(self.fuzzy_service)
        self._connect_view_model_signals()
        self._connect_fuzzy_service_signals()

        self._setup_ui()
        self._retranslate_ui()

    def _connect_view_model_signals(self):
        """Connect view model signals to view methods."""
        self.view_model.mf_list_updated.connect(self._update_table_from_model)
        self.view_model.variable_selected.connect(self._on_variable_selected_from_model)
        self.add_mf_clicked.connect(self.view_model.refresh_data)
        self.remove_mf_clicked.connect(self.view_model.refresh_data)

    def _connect_fuzzy_service_signals(self):
        """Connect fuzzy service signals for real-time updates."""
        if hasattr(self, "fuzzy_service"):
            self.fuzzy_service.system_changed.connect(self._on_system_changed)

    def get_fuzzy_service(self):
        """Get the fuzzy calculation service."""
        return self.fuzzy_service

    def _on_system_changed(self):
        """Handle system changes from fuzzy service."""
        if hasattr(self, "fuzzy_service"):
            fis_model = self.fuzzy_service.get_fis_model()
            self.view_model.model = fis_model
            self.view_model.refresh_data()

    def refresh_ui(self) -> None:
        """Refresh the UI elements."""
        if hasattr(self, "view_model") and self.view_model:
            self.view_model.refresh_data()

    def update_ui(self) -> None:
        """Update UI elements."""
        pass

    def handle_global_update(self) -> None:
        """Handle global update request."""
        pass

    def _setup_ui(self):
        """Set up all the GUI sub elements."""
        self.editor_frame = QtWidgets.QFrame(parent=self)
        self.editor_frame.setGeometry(QtCore.QRect(-10, 0, 291, 641))
        self.editor_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.editor_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.editor_frame.setObjectName("editor_frame")

        self.property_editor_label = QtWidgets.QLabel(parent=self.editor_frame)
        self.property_editor_label.setGeometry(QtCore.QRect(10, 0, 121, 31))
        self.property_editor_label.setObjectName("property_editor_label")

        self.variable_label = QtWidgets.QLabel(parent=self.editor_frame)
        self.variable_label.setGeometry(QtCore.QRect(20, 30, 55, 16))
        self.variable_label.setObjectName("variable_label")

        self.variable_dropdown = QtWidgets.QComboBox(parent=self.editor_frame)
        self.variable_dropdown.setGeometry(QtCore.QRect(110, 25, 161, 31))
        self.variable_dropdown.setObjectName("variable_dropdown")
        self.variable_dropdown.currentTextChanged.connect(self._on_variable_selected)

        self.mf_name_label = QtWidgets.QLabel(parent=self.editor_frame)
        self.mf_name_label.setGeometry(QtCore.QRect(20, 70, 55, 16))
        self.mf_name_label.setObjectName("mf_name_label")

        self.mf_range_label = QtWidgets.QLabel(parent=self.editor_frame)
        self.mf_range_label.setGeometry(QtCore.QRect(20, 115, 55, 18))
        self.mf_range_label.setObjectName("mf_range_label")

        self.mf_name_edit = QtWidgets.QLineEdit(parent=self.editor_frame)
        self.mf_name_edit.setGeometry(QtCore.QRect(110, 60, 161, 31))
        self.mf_name_edit.setObjectName("mf_name_edit")

        self.mf_range_edit = QtWidgets.QLineEdit(parent=self.editor_frame)
        self.mf_range_edit.setGeometry(QtCore.QRect(110, 110, 161, 31))
        self.mf_range_edit.setObjectName("mf_range_edit")
        self.mf_range_edit.setText(self.view_model.default_parameters)

        # Connect to update label when variable changes
        self.view_model.variable_selected.connect(self._update_parameter_label)

        self.mf_table = QtWidgets.QTableWidget(parent=self.editor_frame)
        self.mf_table.setGeometry(QtCore.QRect(10, 238, 281, 421))
        self.mf_table.setObjectName("mf_table")

        self.mf_table.setRowCount(0)  # Start with empty table
        # Column count will be set dynamically in _update_table_from_model based on FIS type
        self.mf_table.setColumnCount(3)
        self.mf_table.setColumnWidth(0, 80)
        self.mf_table.setColumnWidth(1, 80)
        self.mf_table.setColumnWidth(2, 100)

        self.mf_table.setHorizontalHeaderLabels([self.t("NAME"), self.t("TYPE"), self.t("PARAMETERS")])

        self.add_mf_button = QtWidgets.QPushButton(parent=self.editor_frame)
        self.add_mf_button.setGeometry(QtCore.QRect(60, 210, 93, 28))
        self.add_mf_button.setObjectName("add_mf_button")
        self.add_mf_button.clicked.connect(self._add_mf)

        self.number_of_mf_label = QtWidgets.QLabel(parent=self.editor_frame)
        self.number_of_mf_label.setGeometry(QtCore.QRect(20, 170, 151, 16))
        self.number_of_mf_label.setObjectName("number_of_mf_label")

        self.remove_mf_button = QtWidgets.QPushButton(parent=self.editor_frame)
        self.remove_mf_button.setGeometry(QtCore.QRect(160, 210, 93, 28))
        self.remove_mf_button.setObjectName("remove_mf_button")
        self.remove_mf_button.clicked.connect(self._remove_mf)

        self.mf_table.itemSelectionChanged.connect(self._on_mf_selected)

        self._set_number_of_mf(0)

        self.mf_table.itemSelectionChanged.connect(self._on_table_selection_changed)

        self.mf_range_edit.editingFinished.connect(self._on_parameters_changed)

        self.mf_table.itemChanged.connect(self._on_table_item_changed)

        self._retranslate_ui()

    def _retranslate_ui(self):
        """Add text to all the respective GUI elements."""
        self.property_editor_label.setText(self.t("PROPERTY_EDITOR"))
        self.variable_label.setText(self.t("VARIABLE"))
        self.mf_name_label.setText(self.t("NAME"))
        self.mf_range_label.setText(self.t("RANGE"))
        self.remove_mf_button.setText(self.t("REMOVE_MF"))
        self.add_mf_button.setText(self.t("ADD_MF"))
        self.number_of_mf_label.setText(self.t("NUMBER_OF_MF"))
        self.mf_name_edit.setPlaceholderText(self.t("ENTER_MF_NAME"))
        default_params = getattr(self.view_model, "default_parameters", "[0, 0.5, 1]")
        self.mf_range_edit.setText(default_params)

        is_sugeno_output = False
        if self.view_model._model and hasattr(self.view_model._model, "_fis"):
            from fuzzylab import sugfis

            if isinstance(self.view_model._model._fis, sugfis) and self.view_model.selected_variable_type == "output":
                is_sugeno_output = True

        if is_sugeno_output:
            self.mf_table.setHorizontalHeaderLabels([self.t("NAME"), self.t("PARAMETERS")])
        else:
            self.mf_table.setHorizontalHeaderLabels([self.t("NAME"), self.t("TYPE"), self.t("PARAMETERS")])

        self._populate_variable_dropdown()
        self._update_parameter_label()

    def _set_number_of_mf(self, count: int):
        """Update the label text to reflect current mf count."""
        base_text = self.t("NUMBER_OF_MF")
        self.number_of_mf_label.setText(f"{base_text} {count}")

    def _remove_mf(self):
        """Remove the selected membership function using the view model."""
        current_row = self.mf_table.currentRow()

        if current_row < 0:
            return

        success = self.view_model.delete_mf_from_selection(current_row)

        if success:
            self.remove_mf_clicked.emit()
            if self.mf_table.rowCount() > 0:
                if current_row >= self.mf_table.rowCount():
                    self.mf_table.setCurrentCell(self.mf_table.rowCount() - 1, 0)
                else:
                    self.mf_table.setCurrentCell(current_row, 0)

    def _add_mf(self):
        """Add a new membership function using the view model."""
        mf_name = self.mf_name_edit.text()
        mf_parameters = self.mf_range_edit.text()

        success = self.view_model.add_mf_from_input(mf_name, mf_parameters)

        if success:
            self.mf_name_edit.clear()
            self.mf_range_edit.setText(self.view_model.default_parameters)

            self.add_mf_clicked.emit()
        else:
            pass

    def _update_table_from_model(self, mf_list):
        """Update the table based on view model data."""
        # Check if this is a Sugeno output
        is_sugeno_output = False
        if self.view_model._model and hasattr(self.view_model._model, "_fis"):
            from fuzzylab import sugfis

            if isinstance(self.view_model._model._fis, sugfis) and self.view_model.selected_variable_type == "output":
                is_sugeno_output = True

        # Clear existing widgets first to avoid conflicts
        for row in range(self.mf_table.rowCount()):
            widget = self.mf_table.cellWidget(row, 1)
            if widget:
                widget.setParent(None)

        # Set column count and headers based on system type
        if is_sugeno_output:
            self.mf_table.setColumnCount(2)
            self.mf_table.setColumnWidth(0, 120)
            self.mf_table.setColumnWidth(1, 150)
            self.mf_table.setHorizontalHeaderLabels([self.t("NAME"), self.t("PARAMETERS")])
        else:
            self.mf_table.setColumnCount(3)
            self.mf_table.setColumnWidth(0, 80)
            self.mf_table.setColumnWidth(1, 80)
            self.mf_table.setColumnWidth(2, 100)
            self.mf_table.setHorizontalHeaderLabels([self.t("NAME"), self.t("TYPE"), self.t("PARAMETERS")])

        current_selections = {}
        if not self._updating_type:
            reverse_type_map = {
                self.t("TRIANGLE"): "Triangle",
                self.t("TRAPEZOID"): "Trapezoid",
                self.t("GAUSS"): "Gauss",
                self.t("BELL"): "Bell",
                self.t("CONSTANT"): "Constant",
                self.t("LINEAR"): "Linear",
            }
            for row in range(self.mf_table.rowCount()):
                dropdown = self.mf_table.cellWidget(row, 1)
                if dropdown and isinstance(dropdown, QtWidgets.QComboBox):
                    translated_text = dropdown.currentText()
                    actual_type = reverse_type_map.get(translated_text, translated_text)
                    current_selections[row] = actual_type

        self.mf_table.setRowCount(len(mf_list))

        for row, mf_data in enumerate(mf_list):
            self.mf_table.setItem(row, 0, QtWidgets.QTableWidgetItem(mf_data["mf_name"]))

            # Only show Type column for non-Sugeno outputs
            if not is_sugeno_output:
                type_dropdown = QtWidgets.QComboBox(parent=self.mf_table)
                mf_types = self.view_model.available_mf_types
                translated_types = []
                type_map = {
                    "Triangle": self.t("TRIANGLE"),
                    "Trapezoid": self.t("TRAPEZOID"),
                    "Gauss": self.t("GAUSS"),
                    "Bell": self.t("BELL"),
                    "Constant": self.t("CONSTANT"),
                    "Linear": self.t("LINEAR"),
                }
                reverse_type_map = {v: k for k, v in type_map.items()}
                for mf_type in mf_types:
                    translated_types.append(type_map.get(mf_type, mf_type))
                type_dropdown.addItems(translated_types)

                # Block signals while setting initial value to avoid triggering change handler
                type_dropdown.blockSignals(True)
                if row in self._desired_types:
                    desired = self._desired_types[row]
                    translated_desired = type_map.get(desired, desired)
                    type_dropdown.setCurrentText(translated_desired)
                elif row in current_selections and not self._updating_type:
                    current = current_selections[row]
                    translated_current = type_map.get(current, current)
                    type_dropdown.setCurrentText(translated_current)
                else:
                    actual_type = mf_data["mf_type"]
                    translated_type = type_map.get(actual_type, actual_type)
                    type_dropdown.setCurrentText(translated_type)
                type_dropdown.blockSignals(False)

                def make_type_change_handler(row_num, dropdown_ref):
                    def handler(index):
                        print(f"DEBUG: Signal fired! index={index}, row={row_num}")
                        new_text = dropdown_ref.currentText()
                        print(f"DEBUG: Current text: {new_text}")
                        self._on_mf_type_changed(row_num, new_text)

                    return handler

                handler = make_type_change_handler(row, type_dropdown)
                type_dropdown.currentIndexChanged.connect(handler)

                self.mf_table.setCellWidget(row, 1, type_dropdown)

            # Format parameters display - for constant type, show just the value
            params = mf_data["parameters"]
            mf_type = mf_data.get("mf_type", "")

            if mf_type == "Constant" and isinstance(params, list) and len(params) == 1:
                params_str = str(params[0])
            elif mf_type == "Constant" and isinstance(params, (int, float)):
                params_str = str(params)
            else:
                params_str = str(params) if isinstance(params, list) else str(params)

            params_item = QtWidgets.QTableWidgetItem(params_str)
            params_item.setFlags(params_item.flags() | QtCore.Qt.ItemFlag.ItemIsEditable)
            # Parameters column index depends on whether Type column is shown
            params_col = 1 if is_sugeno_output else 2
            self.mf_table.setItem(row, params_col, params_item)

        self._set_number_of_mf(len(mf_list))

        if not self._updating_type:
            self._desired_types.clear()

    def _populate_variable_dropdown(self):
        """Populate the variable dropdown with available variables."""
        self.variable_dropdown.clear()

        variables = self.view_model.get_available_variables()

        for var in variables:
            self.variable_dropdown.addItem(var["display"])

        if self.variable_dropdown.count() == 0:
            self.variable_dropdown.addItem(self.t("NO_VARIABLES_AVAILABLE"))
        else:
            self.variable_dropdown.setCurrentIndex(0)
            first_var = variables[0]
            self.view_model.select_variable_from_display_text(first_var["display"])

    def _on_variable_selected(self, selected_text):
        """Handle variable selection from dropdown."""
        self.view_model.select_variable_from_display_text(selected_text)

    def _on_variable_selected_from_model(self, variable_name, variable_type):
        """Handle variable selected signal from view model."""
        # When variable changes, force table update to redraw with correct columns
        # Clear the table first to ensure clean redraw
        self.mf_table.setRowCount(0)
        # Trigger MF list update which will redraw the table with correct columns
        self.view_model._update_mf_list()

    def _on_mf_selected(self):
        """Handle membership function selection from table."""
        current_row = self.mf_table.currentRow()
        if current_row >= 0:
            mf_info = self.view_model.get_mf_info(self.view_model.selected_variable, current_row)
            if mf_info:
                # For Sugeno constant type, show just the value, not as a list
                params = mf_info["parameters"]
                mf_type = mf_info.get("type", "")

                if mf_type == "Constant" and isinstance(params, list) and len(params) == 1:
                    params_str = str(params[0])
                elif mf_type == "Constant" and isinstance(params, (int, float)):
                    params_str = str(params)
                else:
                    params_str = str(params).replace(" ", "")

                self.mf_range_edit.setText(params_str)
                self._update_parameter_label()

    def _on_mf_type_changed(self, row, new_type):
        """Handle membership function type change."""
        print(f"DEBUG: _on_mf_type_changed called - row={row}, new_type={new_type}")
        print(f"DEBUG: selected_variable={self.view_model.selected_variable}")

        type_map = {
            self.t("TRIANGLE"): "Triangle",
            self.t("TRAPEZOID"): "Trapezoid",
            self.t("GAUSS"): "Gauss",
            self.t("BELL"): "Bell",
            self.t("CONSTANT"): "Constant",
            self.t("LINEAR"): "Linear",
        }
        actual_type = type_map.get(new_type, new_type)
        self._desired_types[row] = actual_type

        self._updating_type = True

        try:
            success = self.view_model.change_mf_type(self.view_model.selected_variable, row, actual_type)

            print(f"DEBUG: change_mf_type returned success={success}")

            if success:
                mf_info = self.view_model.get_mf_info(self.view_model.selected_variable, row)
                if mf_info:
                    params_str = str(mf_info["parameters"]).replace(" ", "")
                    self.mf_range_edit.setText(params_str)
                    print(f"DEBUG: Updated params to {params_str}")
            else:
                print("DEBUG: change_mf_type failed!")
                if row in self._desired_types:
                    del self._desired_types[row]
        finally:
            self._updating_type = False

    def _on_parameters_changed(self):
        """Handle parameter field changes."""
        current_row = self.mf_table.currentRow()
        if current_row < 0:
            return  # No row selected

        params_text = self.mf_range_edit.text().strip()
        if not params_text:
            return  # Empty parameters

        try:
            # Check if this is a Sugeno constant type
            mf_info = self.view_model.get_mf_info(self.view_model.selected_variable, current_row)
            is_constant = mf_info and mf_info.get("type") == "Constant"

            if is_constant:
                # For constant, parse as single value
                try:
                    params = [float(params_text)]
                except ValueError:
                    return
            else:
                params = self.view_model._parse_parameters(params_text)

            success = self.view_model.update_mf_parameters(self.view_model.selected_variable, current_row, params)

            if success:
                self.view_model.refresh_data()
        except Exception:
            pass

    def _update_parameter_label(self):
        """Update the parameter label based on selected variable and MF type."""
        # Check if this is a Sugeno output
        is_sugeno_output = False
        if self.view_model._model and hasattr(self.view_model._model, "_fis"):
            from fuzzylab import sugfis

            if isinstance(self.view_model._model._fis, sugfis) and self.view_model.selected_variable_type == "output":
                is_sugeno_output = True

        if is_sugeno_output:
            # Check current MF type
            current_row = self.mf_table.currentRow()
            if current_row >= 0:
                mf_info = self.view_model.get_mf_info(self.view_model.selected_variable, current_row)
                if mf_info:
                    mf_type = mf_info.get("type", "")
                    if mf_type == "Constant":
                        self.mf_range_label.setText(self.t("VALUE"))
                    elif mf_type == "Linear":
                        self.mf_range_label.setText(self.t("COEFFICIENTS"))
                    else:
                        self.mf_range_label.setText(self.t("RANGE"))
                else:
                    self.mf_range_label.setText(self.t("RANGE"))
            else:
                self.mf_range_label.setText(self.t("RANGE"))
        else:
            self.mf_range_label.setText(self.t("RANGE"))

    def _on_table_item_changed(self, item):
        """Handle table item changes (for inline editing)."""
        # Check if this is a Sugeno output to determine parameter column index
        is_sugeno_output = False
        if self.view_model._model and hasattr(self.view_model._model, "_fis"):
            from fuzzylab import sugfis

            if isinstance(self.view_model._model._fis, sugfis) and self.view_model.selected_variable_type == "output":
                is_sugeno_output = True

        # Parameter column index depends on whether Type column is shown
        params_col = 1 if is_sugeno_output else 2
        if item.column() != params_col:
            return

        row = item.row()
        params_text = item.text().strip()

        if not params_text:
            return

        try:
            # Check if this is a Sugeno constant type
            mf_info = self.view_model.get_mf_info(self.view_model.selected_variable, row)
            is_constant = mf_info and mf_info.get("type") == "Constant"

            if is_constant:
                # For constant, parse as single value
                try:
                    params = [float(params_text)]
                except ValueError:
                    # Restore original value
                    current_params = mf_info.get("parameters", [0.5])
                    if isinstance(current_params, list) and len(current_params) == 1:
                        item.setText(str(current_params[0]))
                    else:
                        item.setText(str(current_params))
                    return
            else:
                params = self.view_model._parse_parameters(params_text)

            success = self.view_model.update_mf_parameters(self.view_model.selected_variable, row, params)

            if success:
                self.mf_range_edit.setText(params_text)
                self._update_parameter_label()
        except Exception:
            try:
                mf_info = self.view_model.get_mf_info(self.view_model.selected_variable, row)
                if mf_info:
                    current_params = mf_info.get("parameters", [])
                    mf_type = mf_info.get("type", "")
                    # Format for display
                    if mf_type == "Constant" and isinstance(current_params, list) and len(current_params) == 1:
                        item.setText(str(current_params[0]))
                    elif mf_type == "Constant" and isinstance(current_params, (int, float)):
                        item.setText(str(current_params))
                    else:
                        item.setText(str(current_params))
            except Exception:
                item.setText("")
