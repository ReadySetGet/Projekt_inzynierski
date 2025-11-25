import re

from PyQt6 import QtCore, QtWidgets

from app.views.base_tab_view import BaseTabView
from app.views.fis_properties_tab_view import FisPropertiesTabView
from app.views.rules_editor_tab import RulesEditorTab


class EditorTabWidget(BaseTabView):
    """Class responsible for the editor tab on the right side of the main window.

    The class allows selecting shape of mfs, their range, defuzzification method
    as well as properties of rules.
    """

    add_mf_clicked = QtCore.pyqtSignal()
    remove_mf_clicked = QtCore.pyqtSignal()
    row = 0
    column = 2

    def __init__(self, parent=None, status_bar=None):
        """Initialize the EditorTabWidget.

        Args:
            parent: Parent widget.
            status_bar: Status bar widget for displaying messages.
        """
        super().__init__(parent=parent)
        self.setObjectName("editorTab")
        self.status_bar = status_bar
        self._updating_mf = False  # Flag to prevent recursive updates
        self._setup_ui()
        self._retranslate_ui()

    def _setup_ui(self):
        self.fis_properties_tab = FisPropertiesTabView(parent=self)
        self.fis_properties_tab.setObjectName("fis_properties_tab")
        self.addTab(self.fis_properties_tab, "")

        self.mf_properties_tab = QtWidgets.QWidget()
        self.mf_properties_tab.setObjectName("fis_properties_tab")

        self.editor_frame = QtWidgets.QFrame(parent=self.mf_properties_tab)
        self.editor_frame.setGeometry(QtCore.QRect(-10, 0, 291, 641))
        self.editor_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.editor_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.editor_frame.setObjectName("editor_frame")

        self.property_editor_label = QtWidgets.QLabel(parent=self.editor_frame)
        self.property_editor_label.setGeometry(QtCore.QRect(10, 0, 121, 31))
        self.property_editor_label.setObjectName("property_editor_label")

        self.mf_name_label = QtWidgets.QLabel(parent=self.editor_frame)
        self.mf_name_label.setGeometry(QtCore.QRect(20, 50, 55, 16))
        self.mf_name_label.setObjectName("mf_name_label")

        self.mf_range_label = QtWidgets.QLabel(parent=self.editor_frame)
        self.mf_range_label.setGeometry(QtCore.QRect(20, 100, 55, 16))
        self.mf_range_label.setObjectName("mf_range_label")

        self.mf_name_edit = QtWidgets.QLineEdit(parent=self.editor_frame)
        self.mf_name_edit.setGeometry(QtCore.QRect(110, 40, 161, 31))
        self.mf_name_edit.setObjectName("mf_name_edit")

        self.mf_range_edit = QtWidgets.QLineEdit(parent=self.editor_frame)
        self.mf_range_edit.setGeometry(QtCore.QRect(110, 90, 161, 31))
        self.mf_range_edit.setObjectName("mf_range_edit")

        self.mf_table = QtWidgets.QTableWidget(parent=self.editor_frame)
        self.mf_table.setGeometry(QtCore.QRect(10, 230, 281, 421))
        self.mf_table.setObjectName("mf_table")

        """Table displaying all MFs"""
        self.mf_table.setRowCount(0)  # Start with empty table
        self.mf_table.setColumnCount(3)
        self.mf_table.setColumnWidth(0, 80)
        self.mf_table.setColumnWidth(1, 80)
        self.mf_table.setColumnWidth(2, 100)
        self.mf_table.setEditTriggers(
            QtWidgets.QAbstractItemView.EditTrigger.DoubleClicked
            | QtWidgets.QAbstractItemView.EditTrigger.EditKeyPressed
        )
        self.mf_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectItems)

        self.mf_table.setHorizontalHeaderLabels(["Name", "Type", "Parameters"])
        self.mf_table.setRowCount(0)
        self.mf_name_edit.editingFinished.connect(self._on_variable_name_changed)
        self.mf_range_edit.editingFinished.connect(self._on_variable_range_changed)
        self.mf_table.itemChanged.connect(self._on_mf_table_item_changed)

        self.add_mf_button = QtWidgets.QPushButton(parent=self.editor_frame)
        self.add_mf_button.setGeometry(QtCore.QRect(60, 190, 93, 28))
        self.add_mf_button.setObjectName("add_mf_button")
        self.add_mf_button.clicked.connect(self._on_add_mf_clicked)

        self.remove_mf_button = QtWidgets.QPushButton(parent=self.editor_frame)
        self.remove_mf_button.setGeometry(QtCore.QRect(160, 190, 93, 28))
        self.remove_mf_button.setObjectName("remove_mf_button")
        self.remove_mf_button.clicked.connect(self._on_remove_mf_clicked)

        self.number_of_mf_label = QtWidgets.QLabel(parent=self.editor_frame)
        self.number_of_mf_label.setGeometry(QtCore.QRect(20, 150, 151, 16))
        self.number_of_mf_label.setObjectName("number_of_mf_label")

        self.addTab(self.mf_properties_tab, "")

        self.rule_editor_tab = RulesEditorTab(parent=self)
        self.rule_editor_tab.setObjectName("rule_editor_tab")
        self.addTab(self.rule_editor_tab, "")

    def set_view_model(self, view_model) -> None:
        """Set the view model and initialize Property Editor."""
        super().set_view_model(view_model)
        self.update_property_editor()

    def refresh_ui(self) -> None:
        """Refresh the UI elements."""
        super().refresh_ui()
        self.update_property_editor()

        self._retranslate_ui()

    def _retranslate_ui(self):
        self.setTabText(
            self.indexOf(self.fis_properties_tab),
            self.t("FIS_PROPERTIES_TAB"),
        )
        self.property_editor_label.setText(self.t("PROPERTY_EDITOR"))
        self.mf_name_label.setText(self.t("NAME"))
        self.mf_range_label.setText(self.t("RANGE"))
        self.add_mf_button.setText(self.t("ADD_MF"))
        self.remove_mf_button.setText(self.t("REMOVE_MF"))
        # Update number of MF label - preserve count if available
        self._update_number_of_mf_label()
        self.setTabText(
            self.indexOf(self.mf_properties_tab),
            self.t("MF_PROPERTIES_TAB"),
        )
        self.setTabText(
            self.indexOf(self.rule_editor_tab),
            self.t("RULE_PROPERTIES_TAB"),
        )

    def get_mf_name(self) -> str:
        """Get the membership function name from the edit field."""
        return self.mf_name_edit.text()

    def set_number_of_mf(self, count: int):
        """Set the number of membership functions label."""
        base_text = self.t("NUMBER_OF_MF")
        self.number_of_mf_label.setText(f"{base_text} {count}")

    def _update_number_of_mf_label(self):
        """Update the number of MF label, preserving the count if available."""
        # Try to get current count from label text
        current_text = self.number_of_mf_label.text()
        count = 0

        # Try to extract count from current text (format: "Number of MF: X" or "NUMBER_OF_MF X")
        if current_text:
            # Look for a number at the end
            match = re.search(r"(\d+)$", current_text.strip())
            if match:
                count = int(match.group(1))
            else:
                # If no count found, try to get it from the table
                count = self.mf_table.rowCount()
        else:
            # If label is empty, get count from table
            count = self.mf_table.rowCount()

        # Update with base text and count
        base_text = self.t("NUMBER_OF_MF")
        self.number_of_mf_label.setText(f"{base_text} {count}")

    def set_name_table_text(self):
        """Update the MF name in the table."""
        self.mf_table.item(self.row, 0).setText(self.mf_name_edit.text())
        self.status_bar.showMessage("Last action: Edited MF name")

    def set_range_table_text(self):
        """Update the MF range in the table."""
        self.mf_table.item(self.row, 2).setText(self.mf_range_edit.text())
        self.status_bar.showMessage("Last action: Edited MF range")

    def update_property_editor(self):
        """Update the Property Editor based on the currently selected variable."""
        if not hasattr(self, "view_model") or not self.view_model or self._updating_mf:
            return

        selected_var_info = self.view_model.get_selected_variable_info()

        if not selected_var_info:
            self._clear_property_editor()
            return

        self._update_variable_display(selected_var_info)
        self._update_membership_functions_table(selected_var_info)

    def _clear_property_editor(self):
        """Clear the property editor when no variable is selected."""
        self.mf_name_edit.setText("")
        self.mf_range_edit.setText("")
        self.mf_table.setRowCount(0)
        base_text = self.t("NUMBER_OF_MF")
        self.number_of_mf_label.setText(f"{base_text} 0")

    def _update_variable_display(self, var_info):
        """Update the variable name and range display."""
        var_data = var_info.get("data") or {}
        var_name = var_info.get("name", "Unknown")
        var_range = var_data.get("range", [0, 100])

        self.mf_name_edit.setText(var_name)
        range_str = f"[{var_range[0]} {var_range[1]}]"
        self.mf_range_edit.setText(range_str)

    def _update_membership_functions_table(self, var_info):
        """Update the membership functions table with the selected variable's MFs."""
        self.mf_table.itemChanged.disconnect(self._on_mf_table_item_changed)

        try:
            var_data = var_info.get("data") or {}
            mfs = var_data.get("membership_functions", [])

            base_text = self.t("NUMBER_OF_MF")
            self.number_of_mf_label.setText(f"{base_text} {len(mfs)}")
            self.mf_table.setRowCount(len(mfs))
            type_mapping = {
                "gaussmf": "Gauss",
                "trapmf": "Trapezoid",
                "trimf": "Triangle",
                "gbellmf": "Bell",
            }

            for i, mf in enumerate(mfs):
                self.mf_table.setItem(i, 0, QtWidgets.QTableWidgetItem(mf.get("name", "")))

                type_dropdown = QtWidgets.QComboBox()
                type_dropdown.addItems(["Gauss", "Trapezoid", "Triangle", "Bell"])

                fuzzy_type = mf.get("type", "trimf")
                english_type = type_mapping.get(fuzzy_type, "Triangle")

                # Block signals while setting initial value
                type_dropdown.blockSignals(True)
                type_dropdown.setCurrentText(english_type)
                type_dropdown.blockSignals(False)

                # Use currentIndexChanged and capture dropdown reference
                type_dropdown.currentIndexChanged.connect(
                    lambda index, idx=i, dropdown=type_dropdown: self._on_mf_type_changed(idx, dropdown.currentText())
                )

                self.mf_table.setCellWidget(i, 1, type_dropdown)

                params = mf.get("parameters", [])
                params_str = str(params).replace(" ", "")
                self.mf_table.setItem(i, 2, QtWidgets.QTableWidgetItem(params_str))
        finally:
            self.mf_table.itemChanged.connect(self._on_mf_table_item_changed)

    def _on_variable_name_changed(self):
        """Handle variable name change."""
        if not hasattr(self, "view_model") or not self.view_model:
            return

        selected_var_info = self.view_model.get_selected_variable_info()
        if not selected_var_info:
            return

        new_name = self.mf_name_edit.text().strip()
        if not new_name:
            return

        var_type = selected_var_info.get("type")
        old_name = selected_var_info.get("name")

        if new_name != old_name:
            if var_type == "input":
                success = self.view_model.fuzzy_service.update_variable_name(old_name, new_name, "input")
            else:
                success = self.view_model.fuzzy_service.update_variable_name(old_name, new_name, "output")

            if success:
                self.view_model.notify_data_changed.emit()
                if hasattr(self, "status_bar") and self.status_bar:
                    self.status_bar.showMessage(f"Variable name changed to: {new_name}")
            else:
                self.mf_name_edit.setText(old_name)
                if hasattr(self, "status_bar") and self.status_bar:
                    self.status_bar.showMessage("Failed to change variable name")

    def _on_variable_range_changed(self):
        """Handle variable range change."""
        if not hasattr(self, "view_model") or not self.view_model:
            return

        selected_var_info = self.view_model.get_selected_variable_info()
        if not selected_var_info:
            return

        range_text = self.mf_range_edit.text().strip()
        var_type = selected_var_info.get("type")
        var_name = selected_var_info.get("name")

        try:
            range_clean = range_text.strip("[]")
            if "," in range_clean:
                range_parts = range_clean.split(",")
            else:
                range_parts = range_clean.split()

            if len(range_parts) != 2:
                raise ValueError("Invalid range format")

            min_val = float(range_parts[0].strip())
            max_val = float(range_parts[1].strip())

            if min_val >= max_val:
                raise ValueError("Min value must be less than max value")

            new_range = [min_val, max_val]

            if var_type == "input":
                success = self.view_model.fuzzy_service.update_variable_range(var_name, new_range, "input")
            else:
                success = self.view_model.fuzzy_service.update_variable_range(var_name, new_range, "output")

            if success:
                self.view_model.notify_data_changed.emit()
                if hasattr(self, "status_bar") and self.status_bar:
                    self.status_bar.showMessage(f"Variable range changed to: {new_range}")
            else:
                var_data = selected_var_info.get("data", {})
                old_range = var_data.get("range", [0, 100])
                range_str = f"[{old_range[0]} {old_range[1]}]"
                self.mf_range_edit.setText(range_str)
                if hasattr(self, "status_bar") and self.status_bar:
                    self.status_bar.showMessage("Failed to change variable range")

        except (ValueError, IndexError) as e:
            var_data = selected_var_info.get("data", {})
            old_range = var_data.get("range", [0, 100])
            range_str = f"[{old_range[0]} {old_range[1]}]"
            self.mf_range_edit.setText(range_str)
            if hasattr(self, "status_bar") and self.status_bar:
                self.status_bar.showMessage(f"Invalid range format: {e}")

    def _on_mf_table_item_changed(self, item):
        """Handle MF table item changes (name and parameters)."""
        if not hasattr(self, "view_model") or not self.view_model:
            return

        row = item.row()
        column = item.column()

        if column == 0:  # Name column
            self._on_mf_name_changed(row, item.text())
        elif column == 2:  # Parameters column
            self._on_mf_parameters_changed(row, item.text())

    def _on_mf_name_changed(self, mf_index, new_name):
        """Handle MF name change."""
        if not new_name.strip() or self._updating_mf:
            return

        self._updating_mf = True
        try:
            selected_var_info = self.view_model.get_selected_variable_info()
            if not selected_var_info:
                return

            var_name = selected_var_info.get("name")
            var_type = selected_var_info.get("type")

            success = self.view_model.fuzzy_service.update_membership_function_name(
                var_name, mf_index, new_name.strip(), var_type
            )

            if success:
                self.update_property_editor()
                # Also trigger a global refresh to update plots
                self.view_model.notify_data_changed.emit()
                if hasattr(self, "status_bar") and self.status_bar:
                    self.status_bar.showMessage(f"MF name changed to: {new_name.strip()}")
            else:
                var_data = selected_var_info.get("data", {})
                mfs = var_data.get("membership_functions", [])
                if mf_index < len(mfs):
                    old_name = mfs[mf_index].get("name", "")
                    self.mf_table.setItem(mf_index, 0, QtWidgets.QTableWidgetItem(old_name))
                if hasattr(self, "status_bar") and self.status_bar:
                    self.status_bar.showMessage("Failed to change MF name")
        finally:
            self._updating_mf = False

    def _on_mf_parameters_changed(self, mf_index, new_params_text):
        """Handle MF parameters change."""
        if not new_params_text.strip() or self._updating_mf:
            return

        self._updating_mf = True
        try:
            try:
                params_clean = new_params_text.strip("[]")
                if "," in params_clean:
                    params_parts = params_clean.split(",")
                else:
                    params_parts = params_clean.split()

                if not params_parts:
                    raise ValueError("No parameters provided")

                new_params = [float(param.strip()) for param in params_parts if param.strip()]

                if not new_params:
                    raise ValueError("No valid parameters provided")

            except (ValueError, IndexError) as e:
                selected_var_info = self.view_model.get_selected_variable_info()
                if selected_var_info:
                    var_data = selected_var_info.get("data", {})
                    mfs = var_data.get("membership_functions", [])
                    if mf_index < len(mfs):
                        old_params = mfs[mf_index].get("parameters", [])
                        params_str = str(old_params).replace(" ", "")
                        self.mf_table.setItem(mf_index, 2, QtWidgets.QTableWidgetItem(params_str))
                if hasattr(self, "status_bar") and self.status_bar:
                    self.status_bar.showMessage(f"Invalid parameters format: {e}")
                return

            selected_var_info = self.view_model.get_selected_variable_info()
            if not selected_var_info:
                return

            var_name = selected_var_info.get("name")
            var_type = selected_var_info.get("type")

            success = self.view_model.fuzzy_service.update_membership_function_parameters(
                var_name, mf_index, new_params, var_type
            )

            if success:
                self.update_property_editor()
                # Also trigger a global refresh to update plots
                self.view_model.notify_data_changed.emit()
                if hasattr(self, "status_bar") and self.status_bar:
                    self.status_bar.showMessage(f"MF parameters updated: {new_params}")
            else:
                var_data = selected_var_info.get("data", {})
                mfs = var_data.get("membership_functions", [])
                if mf_index < len(mfs):
                    old_params = mfs[mf_index].get("parameters", [])
                    params_str = str(old_params).replace(" ", "")
                    self.mf_table.setItem(mf_index, 2, QtWidgets.QTableWidgetItem(params_str))
                if hasattr(self, "status_bar") and self.status_bar:
                    self.status_bar.showMessage("Failed to change MF parameters")
        finally:
            self._updating_mf = False

    def _on_mf_type_changed(self, mf_index, new_type):
        """Handle MF type change."""
        if self._updating_mf:
            return

        self._updating_mf = True
        try:
            selected_var_info = self.view_model.get_selected_variable_info()
            if not selected_var_info:
                return

            var_name = selected_var_info.get("name")
            var_type = selected_var_info.get("type")

            type_mapping = {
                "Gauss": "gaussowska",
                "Trapezoid": "trapezoidalna",
                "Triangle": "trojkatna",
                "Bell": "dzwonowa",
            }

            fuzzy_type = type_mapping.get(new_type, "trojkatna")

            success = self.view_model.fuzzy_service.change_membership_function_type(
                var_name, mf_index, fuzzy_type, var_type
            )

            if success:
                var_data = selected_var_info.get("data", {})
                var_range = var_data.get("range", [0, 1])
                range_min, range_max = var_range[0], var_range[1]
                range_span = range_max - range_min

                if new_type == "Triangle":
                    new_params = [range_min, range_min + 0.5 * range_span, range_max]
                elif new_type == "Trapezoid":
                    new_params = [
                        range_min,
                        range_min + 0.3 * range_span,
                        range_min + 0.7 * range_span,
                        range_max,
                    ]
                elif new_type == "Gauss":
                    new_params = [
                        0.2 * range_span,
                        range_min + 0.5 * range_span,
                    ]  # [sigma, mu]
                elif new_type == "Bell":
                    new_params = [
                        0.2 * range_span,
                        3,
                        range_min + 0.5 * range_span,
                    ]  # [a, b, c]
                else:
                    new_params = [range_min, range_min + 0.5 * range_span, range_max]

                # Round to 2 decimal places
                new_params = [round(p, 2) for p in new_params]

                self.view_model.fuzzy_service.update_membership_function_parameters(
                    var_name, mf_index, new_params, var_type
                )

                self._updating_mf = False

                self.update_property_editor()

                self.view_model.notify_data_changed.emit()

                if hasattr(self, "status_bar") and self.status_bar:
                    self.status_bar.showMessage(f"MF type changed to: {new_type}")

                self._updating_mf = True
            else:
                var_data = selected_var_info.get("data", {})
                mfs = var_data.get("membership_functions", [])
                if mf_index < len(mfs):
                    old_fuzzy_type = mfs[mf_index].get("type", "trimf")
                    reverse_mapping = {v: k for k, v in type_mapping.items()}
                    old_english_type = reverse_mapping.get(old_fuzzy_type, "Triangle")
                    dropdown = self.mf_table.cellWidget(mf_index, 1)
                    if dropdown:
                        dropdown.setCurrentText(old_english_type)
                if hasattr(self, "status_bar") and self.status_bar:
                    self.status_bar.showMessage("Failed to change MF type")
        finally:
            self._updating_mf = False

    def _on_add_mf_clicked(self):
        """Handle add MF button click."""
        selected_var_info = self.view_model.get_selected_variable_info()

        if not selected_var_info:
            if hasattr(self, "status_bar") and self.status_bar:
                self.status_bar.showMessage("No variable selected")
            return

        var_name = selected_var_info.get("name")
        var_type = selected_var_info.get("type")
        var_data = selected_var_info.get("data", {})
        mfs = var_data.get("membership_functions", [])

        new_mf_name = f"mf{len(mfs) + 1}"

        var_range = var_data.get("range", [0, 10])
        range_min, range_max = var_range[0], var_range[1]

        # Default parameters for triangle (scaled to range)
        default_params = [range_min, (range_min + range_max) / 2, range_max]

        success = self.view_model.fuzzy_service.add_membership_function(
            var_name, new_mf_name, "trojkatna", default_params, var_type
        )

        if success:
            self.update_property_editor()
            self.view_model.notify_data_changed.emit()
            if hasattr(self, "status_bar") and self.status_bar:
                self.status_bar.showMessage(f"Added MF: {new_mf_name}")
        else:
            if hasattr(self, "status_bar") and self.status_bar:
                self.status_bar.showMessage("Failed to add MF")

    def _on_remove_mf_clicked(self):
        """Handle remove MF button click."""
        selected_var_info = self.view_model.get_selected_variable_info()

        if not selected_var_info:
            if hasattr(self, "status_bar") and self.status_bar:
                self.status_bar.showMessage("No variable selected")
            return

        current_row = self.mf_table.currentRow()
        if current_row < 0:
            if hasattr(self, "status_bar") and self.status_bar:
                self.status_bar.showMessage("No MF selected")
            return

        var_name = selected_var_info.get("name")
        var_type = selected_var_info.get("type")

        var_data = selected_var_info.get("data", {})
        mfs = var_data.get("membership_functions", [])
        mf_name = mfs[current_row].get("name", f"MF{current_row}") if current_row < len(mfs) else "MF"

        # Delete the MF using fuzzy service
        success = self.view_model.fuzzy_service.delete_membership_function(var_name, current_row, var_type)

        if success:
            self.update_property_editor()
            self.view_model.notify_data_changed.emit()
            if hasattr(self, "status_bar") and self.status_bar:
                self.status_bar.showMessage(f"Deleted MF: {mf_name}")
        else:
            if hasattr(self, "status_bar") and self.status_bar:
                self.status_bar.showMessage("Failed to delete MF")
