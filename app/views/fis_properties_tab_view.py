"""FIS Properties tab view with Add Input/Output buttons."""

from PyQt6 import QtCore, QtWidgets

from app.view_models.fis_properties_view_model import FisPropertiesViewModel
from app.views.base_widget_view import BaseWidgetView


class FisPropertiesTabView(BaseWidgetView):
    """FIS Properties tab view with Add Input/Output buttons."""

    def __init__(self, qss_filename=None, parent=None):
        """Initialize the FIS Properties tab view.

        Args:
            qss_filename: Optional QSS file for styling
            parent: The parent widget
        """
        super().__init__(qss_filename=qss_filename, parent=parent)
        self.setObjectName("fis_properties_tab")

        # Initialize view model
        self.view_model = FisPropertiesViewModel()
        self.view_model.setParent(self)
        self.set_view_model(self.view_model)

        # Initialize the system info from the fuzzy service
        self.view_model._update_system_info()

        # Connect view model signals
        self._connect_view_model_signals()

        self._setup_ui()
        self._retranslate_ui()

    def _connect_view_model_signals(self):
        """Connect view model signals to view methods."""
        self.view_model.fis_system_updated.connect(self._on_system_updated)
        self.view_model.input_added.connect(self._on_input_added)
        self.view_model.output_added.connect(self._on_output_added)
        self.view_model.variable_selected.connect(self._on_variable_selected)

    def _setup_ui(self):
        """Set up all the GUI sub elements."""
        # Main frame
        self.main_frame = QtWidgets.QFrame(parent=self)
        self.main_frame.setGeometry(QtCore.QRect(0, 0, 281, 641))
        self.main_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.main_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.main_frame.setObjectName("main_frame")

        # Title label
        self.title_label = QtWidgets.QLabel(parent=self.main_frame)
        self.title_label.setGeometry(QtCore.QRect(10, 10, 261, 31))
        self.title_label.setObjectName("title_label")

        # System name section
        self.system_name_label = QtWidgets.QLabel(parent=self.main_frame)
        self.system_name_label.setGeometry(QtCore.QRect(20, 50, 100, 16))
        self.system_name_label.setObjectName("system_name_label")

        self.system_name_edit = QtWidgets.QLineEdit(parent=self.main_frame)
        self.system_name_edit.setGeometry(QtCore.QRect(130, 45, 131, 31))
        self.system_name_edit.setObjectName("system_name_edit")
        self.system_name_edit.setText("fis")

        # System type section
        self.system_type_label = QtWidgets.QLabel(parent=self.main_frame)
        self.system_type_label.setGeometry(QtCore.QRect(20, 90, 100, 16))
        self.system_type_label.setObjectName("system_type_label")

        self.system_type_combo = QtWidgets.QComboBox(parent=self.main_frame)
        self.system_type_combo.setGeometry(QtCore.QRect(130, 85, 131, 31))
        self.system_type_combo.setObjectName("system_type_combo")
        self.system_type_combo.addItems(["mamfis", "sugfis"])
        self.system_type_combo.currentTextChanged.connect(self._on_system_type_changed)

        # Input variables section
        self.inputs_label = QtWidgets.QLabel(parent=self.main_frame)
        self.inputs_label.setGeometry(QtCore.QRect(20, 130, 100, 16))
        self.inputs_label.setObjectName("inputs_label")

        self.add_input_button = QtWidgets.QPushButton(parent=self.main_frame)
        self.add_input_button.setGeometry(QtCore.QRect(20, 150, 100, 28))
        self.add_input_button.setObjectName("add_input_button")
        self.add_input_button.clicked.connect(self._add_input)

        self.inputs_list = QtWidgets.QListWidget(parent=self.main_frame)
        self.inputs_list.setGeometry(QtCore.QRect(20, 185, 241, 100))
        self.inputs_list.setObjectName("inputs_list")

        # Output variables section
        self.outputs_label = QtWidgets.QLabel(parent=self.main_frame)
        self.outputs_label.setGeometry(QtCore.QRect(20, 295, 100, 16))
        self.outputs_label.setObjectName("outputs_label")

        self.add_output_button = QtWidgets.QPushButton(parent=self.main_frame)
        self.add_output_button.setGeometry(QtCore.QRect(20, 315, 100, 28))
        self.add_output_button.setObjectName("add_output_button")
        self.add_output_button.clicked.connect(self._add_output)

        self.outputs_list = QtWidgets.QListWidget(parent=self.main_frame)
        self.outputs_list.setGeometry(QtCore.QRect(20, 350, 241, 100))
        self.outputs_list.setObjectName("outputs_list")

        # Variable info section
        self.variable_info_label = QtWidgets.QLabel(parent=self.main_frame)
        self.variable_info_label.setGeometry(QtCore.QRect(20, 460, 100, 16))
        self.variable_info_label.setObjectName("variable_info_label")

        self.variable_info_text = QtWidgets.QTextEdit(parent=self.main_frame)
        self.variable_info_text.setGeometry(QtCore.QRect(20, 480, 241, 100))
        self.variable_info_text.setObjectName("variable_info_text")
        self.variable_info_text.setReadOnly(True)

        # Connect list selection changes
        self.inputs_list.itemSelectionChanged.connect(self._on_input_selected)
        self.outputs_list.itemSelectionChanged.connect(self._on_output_selected)

        # Update the UI with current data
        self._update_ui_from_model()

    def _retranslate_ui(self):
        """Add text to all the respective GUI elements."""
        self.title_label.setText(self.t("FIS_PROPERTIES"))
        self.system_name_label.setText(self.t("SYSTEM_NAME"))
        self.system_type_label.setText(self.t("SYSTEM_TYPE"))
        self.inputs_label.setText(self.t("INPUT_VARIABLES"))
        self.outputs_label.setText(self.t("OUTPUT_VARIABLES"))
        self.add_input_button.setText(self.t("ADD_INPUT"))
        self.add_output_button.setText(self.t("ADD_OUTPUT"))
        self.variable_info_label.setText(self.t("VARIABLE_INFO"))

    def _on_system_updated(self):
        """Handle system update from view model."""
        self._update_ui_from_model()

    def _on_input_added(self, input_name, input_index):
        """Handle input added signal."""
        self._update_inputs_list()

    def _on_output_added(self, output_name, output_index):
        """Handle output added signal."""
        self._update_outputs_list()

    def _on_variable_selected(self, variable_name, variable_type):
        """Handle variable selection."""
        self._update_variable_info(variable_name, variable_type)

    def _on_system_type_changed(self, system_type):
        """Handle system type change."""
        self.view_model.system_type = system_type

    def _add_input(self):
        """Add a new input variable."""
        self.view_model.add_input()

    def _add_output(self):
        """Add a new output variable."""
        self.view_model.add_output()

    def _on_input_selected(self):
        """Handle input selection."""
        current_item = self.inputs_list.currentItem()
        if current_item:
            input_name = current_item.text()
            self.view_model.select_variable(input_name, "input")

    def _on_output_selected(self):
        """Handle output selection."""
        current_item = self.outputs_list.currentItem()
        if current_item:
            output_name = current_item.text()
            self.view_model.select_variable(output_name, "output")

    def _update_ui_from_model(self):
        """Update UI elements from the model."""
        # Update system name
        self.system_name_edit.setText(self.view_model.system_name)

        # Update system type
        self.system_type_combo.setCurrentText(self.view_model.system_type)

        # Update lists
        self._update_inputs_list()
        self._update_outputs_list()

    def _update_inputs_list(self):
        """Update the inputs list."""
        self.inputs_list.clear()
        for input_var in self.view_model.inputs:
            item_text = f"{input_var['name']} (Range: {input_var['range']}, MFs: {input_var['mf_count']})"
            self.inputs_list.addItem(item_text)

    def _update_outputs_list(self):
        """Update the outputs list."""
        self.outputs_list.clear()
        for output_var in self.view_model.outputs:
            item_text = f"{output_var['name']} (Range: {output_var['range']}, MFs: {output_var['mf_count']})"
            self.outputs_list.addItem(item_text)

    def _update_variable_info(self, variable_name, variable_type):
        """Update the variable info text."""
        info = self.view_model.get_variable_info(variable_name, variable_type)
        if info:
            info_text = f"Name: {info['name']}\n"
            info_text += f"Type: {variable_type}\n"
            info_text += f"Range: {info['range']}\n"
            info_text += f"Membership Functions: {info['mf_count']}\n\n"

            if info["membership_functions"]:
                info_text += "Membership Functions:\n"
                for mf in info["membership_functions"]:
                    info_text += f" - {mf['name']} ({mf['type']}): {mf['parameters']}\n"

            self.variable_info_text.setText(info_text)
        else:
            self.variable_info_text.setText("No variable selected")
