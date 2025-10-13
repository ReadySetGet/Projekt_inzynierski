from PyQt6 import QtCore, QtWidgets

from app.view_models.mf_editor_view_model import MFEditorViewModel
from app.views.base_view import BaseWidget


class MFPropertiesWidget(BaseWidget):
    """Class inheriting from QWidget.

    Allows user interaction via QPushButton, QLineEdit and QComboBox GUI elements.
    The current membership functions in the system are displayed within the table.

    Methods:
        __init__(QtWidgets.*): create an instance of MFPropertiesWidget and bind it
            to the parent window.
        get_mf_name(): get the name of the mf from the line edit.

    Attributes:
        shape_changed_emit: pyqtSignal which gets emitted to backend when the
            dropdown item has changed.
        remove_mf_clicked: pyqtSignal which gets emitted to backend when
            remove_mf_button is clicked.
        add_mf_clicked: pyqtSignal which gets emitted to backend when
            add_mf_button is clicked.
        default_parameters: default parameters of a new function.
    """

    shape_changed_emit = QtCore.pyqtSignal()
    remove_mf_clicked = QtCore.pyqtSignal()
    add_mf_clicked = QtCore.pyqtSignal()

    def __init__(self, context=None, qss_filename=None, parent=None):
        """Initialize a new class instance.

        Args:
            context (object, optional): The application context. Defaults to
                None.
            qss_filename (str, optional): Optional QSS file for styling.
                Defaults to None.
            parent (QWidget, optional): The parent widget, in this case editor
                tab, to which the widget will be attached. Defaults to None.
        """
        super().__init__(context=context, qss_filename=qss_filename, parent=parent)
        self.setObjectName("mf_properties_tab")

        # Initialize view model with the fuzzy service model
        self.view_model = MFEditorViewModel()
        self.view_model.setParent(self)

        # Set the model if context has fuzzy service
        if hasattr(self.context, "fuzzy_service"):
            fis_model = self.context.fuzzy_service.get_fis_model()
            self.view_model.model = fis_model

        # Connect view model signals
        self._connect_view_model_signals()

        self._setup_ui()
        self._retranslate_ui()

    def _connect_view_model_signals(self):
        """Connect view model signals to view methods."""
        self.view_model.mf_list_updated.connect(self._update_table_from_model)
        self.view_model.mf_added.connect(self._on_mf_added)
        self.view_model.mf_deleted.connect(self._on_mf_deleted)
        self.view_model.variable_selected.connect(self._on_variable_selected_from_model)

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

        # Variable selection
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

        # Initialize the count after all UI elements are created
        self._set_number_of_mf(0)

        # Connect table selection changes
        self.mf_table.itemSelectionChanged.connect(self._on_table_selection_changed)

        self._retranslate_ui()

    def _retranslate_ui(self):
        """Add text to all the respective GUI elements."""
        self.property_editor_label.setText(self.t("Property Editor"))
        self.variable_label.setText(self.t("Variable"))
        self.mf_name_label.setText(self.t("Name"))
        self.mf_range_label.setText(self.t("Range"))
        self.remove_mf_button.setText(self.t("Remove MF"))
        self.add_mf_button.setText(self.t("Add MF"))
        self.number_of_mf_label.setText(self.t("Number of MF:"))
        # Set default values
        self.mf_name_edit.setPlaceholderText(self.t("Enter MF name"))
        self.mf_range_edit.setText(self.view_model.default_parameters)

        # Populate variable dropdown
        self._populate_variable_dropdown()

    def get_mf_name(self) -> str:
        """Get the current name of the membership function via the line edit."""
        return self.mf_name_edit.text()

    def _set_number_of_mf(self, count: int):
        """Update the label text to reflect current mf count."""
        self.number_of_mf_label.setText(f"Number of MF: {count}")

    def _shape_changed(self):
        """Emit the signal that the shape of mf was changed to the backend."""
        self.shape_changed_emit.emit()

    def _remove_mf(self):
        """Remove the selected membership function using the view model."""
        current_row = self.mf_table.currentRow()

        # Delegate all logic to view model
        success = self.view_model.delete_mf_from_selection(current_row)

        if success:
            # Emit signal for UI updates
            self.remove_mf_clicked.emit()

    def _add_mf(self):
        """Add a new membership function using the view model."""
        # Get values from input fields (no validation - that's view model's job)
        mf_name = self.mf_name_edit.text()
        mf_parameters = self.mf_range_edit.text()

        # Delegate all logic to view model
        success = self.view_model.add_mf_from_input(mf_name, mf_parameters)

        if success:
            # Clear input fields after successful addition
            self.mf_name_edit.clear()
            self.mf_range_edit.setText(self.view_model.default_parameters)

            # Emit signal for UI updates
            self.add_mf_clicked.emit()

    def _update_table_from_model(self, mf_list):
        """Update the table based on view model data."""
        self.mf_table.setRowCount(len(mf_list))

        for row, mf_data in enumerate(mf_list):
            # Set name
            self.mf_table.setItem(
                row, 0, QtWidgets.QTableWidgetItem(mf_data["mf_name"])
            )

            # Set type dropdown
            type_dropdown = QtWidgets.QComboBox(parent=self.mf_table)
            type_dropdown.addItems(self.view_model.available_mf_types)
            type_dropdown.setCurrentText(mf_data["mf_type"])
            type_dropdown.currentIndexChanged.connect(self._shape_changed)
            self.mf_table.setCellWidget(row, 1, type_dropdown)

            # Set parameters
            params_str = (
                str(mf_data["parameters"])
                if isinstance(mf_data["parameters"], list)
                else mf_data["parameters"]
            )
            self.mf_table.setItem(row, 2, QtWidgets.QTableWidgetItem(params_str))

        # Update count
        self._set_number_of_mf(len(mf_list))

    def _on_mf_added(self, variable_name, mf_name, mf_index):
        """Handle MF added signal from view model."""
        pass  # Table will be updated via _update_table_from_model

    def _on_mf_deleted(self, variable_name, mf_index):
        """Handle MF deleted signal from view model."""
        pass  # Table will be updated via _update_table_from_model

    def _populate_variable_dropdown(self):
        """Populate the variable dropdown with available variables."""
        self.variable_dropdown.clear()

        # Get variables from view model (delegate all logic)
        variables = self.view_model.get_available_variables()

        # Add variables to dropdown
        for var in variables:
            self.variable_dropdown.addItem(var["display"])

        # If no variables, add a placeholder
        if self.variable_dropdown.count() == 0:
            self.variable_dropdown.addItem("No variables available")
        else:
            # Select the first variable by default
            self.variable_dropdown.setCurrentIndex(0)
            first_var = variables[0]
            self.view_model.select_variable_from_display_text(first_var["display"])

    def _on_variable_selected(self, selected_text):
        """Handle variable selection from dropdown."""
        # Delegate all logic to view model
        self.view_model.select_variable_from_display_text(selected_text)

    def _on_variable_selected_from_model(self, variable_name, variable_type):
        """Handle variable selected signal from view model."""
        # Update UI to reflect selected variable
        pass

    def _on_table_selection_changed(self):
        """Handle table selection changes."""
        pass
