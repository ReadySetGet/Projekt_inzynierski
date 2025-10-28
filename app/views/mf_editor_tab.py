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

        self.mf_table = QtWidgets.QTableWidget(parent=self.editor_frame)
        self.mf_table.setGeometry(QtCore.QRect(10, 238, 281, 421))
        self.mf_table.setObjectName("mf_table")

        self.mf_table.setRowCount(0)  # Start with empty table
        self.mf_table.setColumnCount(3)
        self.mf_table.setColumnWidth(0, 80)
        self.mf_table.setColumnWidth(1, 80)
        self.mf_table.setColumnWidth(2, 100)

        self.mf_table.setHorizontalHeaderLabels(["Name", "Type", "Parameters"])

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
        self.mf_range_edit.setText(self.view_model.default_parameters)

        self._populate_variable_dropdown()

    def _set_number_of_mf(self, count: int):
        """Update the label text to reflect current mf count."""
        self.number_of_mf_label.setText(f"Number of MF: {count}")

    def _remove_mf(self):
        """Remove the selected membership function using the view model."""
        current_row = self.mf_table.currentRow()

        success = self.view_model.delete_mf_from_selection(current_row)

        if success:
            self.remove_mf_clicked.emit()
        else:
            pass

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
        current_selections = {}
        if not self._updating_type:
            for row in range(self.mf_table.rowCount()):
                dropdown = self.mf_table.cellWidget(row, 1)
                if dropdown and isinstance(dropdown, QtWidgets.QComboBox):
                    current_selections[row] = dropdown.currentText()

        self.mf_table.setRowCount(len(mf_list))

        for row, mf_data in enumerate(mf_list):
            self.mf_table.setItem(row, 0, QtWidgets.QTableWidgetItem(mf_data["mf_name"]))

            type_dropdown = QtWidgets.QComboBox(parent=self.mf_table)
            type_dropdown.addItems(self.view_model.available_mf_types)

            # Block signals while setting initial value to avoid triggering change handler
            type_dropdown.blockSignals(True)
            if row in self._desired_types:
                type_dropdown.setCurrentText(self._desired_types[row])
            elif row in current_selections and not self._updating_type:
                type_dropdown.setCurrentText(current_selections[row])
            else:
                type_dropdown.setCurrentText(mf_data["mf_type"])
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
            print(f"DEBUG: Connected handler for row {row}, current text: {type_dropdown.currentText()}")

            self.mf_table.setCellWidget(row, 1, type_dropdown)

            params_str = (
                str(mf_data["parameters"]) if isinstance(mf_data["parameters"], list) else mf_data["parameters"]
            )
            params_item = QtWidgets.QTableWidgetItem(params_str)
            params_item.setFlags(params_item.flags() | QtCore.Qt.ItemFlag.ItemIsEditable)
            self.mf_table.setItem(row, 2, params_item)

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
            self.variable_dropdown.addItem("No variables available")
        else:
            self.variable_dropdown.setCurrentIndex(0)
            first_var = variables[0]
            self.view_model.select_variable_from_display_text(first_var["display"])

    def _on_variable_selected(self, selected_text):
        """Handle variable selection from dropdown."""
        self.view_model.select_variable_from_display_text(selected_text)

    def _on_variable_selected_from_model(self, variable_name, variable_type):
        """Handle variable selected signal from view model."""
        pass

    def _on_mf_selected(self):
        """Handle membership function selection from table."""
        current_row = self.mf_table.currentRow()
        if current_row >= 0:
            mf_info = self.view_model.get_mf_info(self.view_model.selected_variable, current_row)
            if mf_info:
                params_str = str(mf_info["parameters"]).replace(" ", "")
                self.mf_range_edit.setText(params_str)

    def _on_mf_type_changed(self, row, new_type):
        """Handle membership function type change."""
        print(f"DEBUG: _on_mf_type_changed called - row={row}, new_type={new_type}")
        print(f"DEBUG: selected_variable={self.view_model.selected_variable}")

        self._desired_types[row] = new_type

        self._updating_type = True

        try:
            success = self.view_model.change_mf_type(self.view_model.selected_variable, row, new_type)

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
            params = self.view_model._parse_parameters(params_text)

            success = self.view_model.update_mf_parameters(self.view_model.selected_variable, current_row, params)

            if success:
                self.view_model.refresh_data()
        except Exception:
            pass

    def _on_table_item_changed(self, item):
        """Handle table item changes (for inline editing)."""
        # Handle table item changes

        # Only handle parameter column (column 2)
        if item.column() != 2:
            return

        row = item.row()
        params_text = item.text().strip()
        # Handle inline parameter edit

        if not params_text:
            return

        try:
            params = self.view_model._parse_parameters(params_text)

            success = self.view_model.update_mf_parameters(self.view_model.selected_variable, row, params)

            if success:
                self.mf_range_edit.setText(params_text)
        except Exception:
            try:
                mf_info = self.view_model.get_mf_info(self.view_model.selected_variable, row)
                if mf_info:
                    current_params = mf_info.get("parameters", [])
                    item.setText(str(current_params))
            except Exception:
                item.setText("")
