"""FIS Properties tab view with Add Input/Output buttons."""

from PyQt6 import QtWidgets

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

        self.view_model = FisPropertiesViewModel()
        self.view_model.setParent(self)
        self.set_view_model(self.view_model)

        self.view_model._update_system_info()

        self._connect_view_model_signals()

        self._setup_ui()
        self._retranslate_ui()

    def _connect_view_model_signals(self):
        """Connect view model signals to view methods."""
        self.view_model.fis_system_updated.connect(self._on_system_updated)
        self.view_model.input_added.connect(self._on_input_added)
        self.view_model.output_added.connect(self._on_output_added)
        self.view_model.variable_selected.connect(self._on_variable_selected)
        self.view_model.notify_data_changed.connect(self._on_system_updated)

    def _setup_ui(self):
        """Set up all the GUI sub elements."""
        # Main layout
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # Title label
        self.title_label = QtWidgets.QLabel()
        self.title_label.setObjectName("title_label")
        main_layout.addWidget(self.title_label)

        # System name section
        name_layout = QtWidgets.QHBoxLayout()
        self.system_name_label = QtWidgets.QLabel()
        self.system_name_label.setObjectName("system_name_label")
        name_layout.addWidget(self.system_name_label)

        self.system_name_edit = QtWidgets.QLineEdit()
        self.system_name_edit.setObjectName("system_name_edit")
        self.system_name_edit.setText("fis")
        name_layout.addWidget(self.system_name_edit)
        main_layout.addLayout(name_layout)

        # System type section
        type_layout = QtWidgets.QHBoxLayout()
        self.system_type_label = QtWidgets.QLabel()
        self.system_type_label.setObjectName("system_type_label")
        type_layout.addWidget(self.system_type_label)

        self.system_type_combo = QtWidgets.QComboBox()
        self.system_type_combo.setObjectName("system_type_combo")
        # Items will be set in _retranslate_ui with translations
        self.system_type_combo.currentTextChanged.connect(self._on_system_type_changed)
        type_layout.addWidget(self.system_type_combo)
        main_layout.addLayout(type_layout)

        # Defuzzification section
        defuzz_layout = QtWidgets.QHBoxLayout()
        self.defuzzification_label = QtWidgets.QLabel()
        self.defuzzification_label.setObjectName("defuzzification_label")
        defuzz_layout.addWidget(self.defuzzification_label)

        self.defuzzification_combo = QtWidgets.QComboBox()
        self.defuzzification_combo.setObjectName("defuzzification_combo")
        self.defuzzification_combo.currentTextChanged.connect(self._on_defuzzification_changed)
        defuzz_layout.addWidget(self.defuzzification_combo)
        main_layout.addLayout(defuzz_layout)

        # Input variables section
        inputs_group = QtWidgets.QGroupBox()
        inputs_group.setObjectName("inputs_group")
        inputs_layout = QtWidgets.QVBoxLayout(inputs_group)

        self.inputs_label = QtWidgets.QLabel()
        self.inputs_label.setObjectName("inputs_label")
        inputs_layout.addWidget(self.inputs_label)

        input_buttons_layout = QtWidgets.QHBoxLayout()
        self.add_input_button = QtWidgets.QPushButton()
        self.add_input_button.setObjectName("add_input_button")
        self.add_input_button.clicked.connect(self._add_input)
        input_buttons_layout.addWidget(self.add_input_button)

        self.delete_input_button = QtWidgets.QPushButton()
        self.delete_input_button.setObjectName("delete_input_button")
        self.delete_input_button.clicked.connect(self._delete_input)
        input_buttons_layout.addWidget(self.delete_input_button)
        inputs_layout.addLayout(input_buttons_layout)

        self.inputs_list = QtWidgets.QListWidget()
        self.inputs_list.setObjectName("inputs_list")
        self.inputs_list.setMaximumHeight(120)
        inputs_layout.addWidget(self.inputs_list)
        main_layout.addWidget(inputs_group)

        # Output variables section
        outputs_group = QtWidgets.QGroupBox()
        outputs_group.setObjectName("outputs_group")
        outputs_layout = QtWidgets.QVBoxLayout(outputs_group)

        self.outputs_label = QtWidgets.QLabel()
        self.outputs_label.setObjectName("outputs_label")
        outputs_layout.addWidget(self.outputs_label)

        output_buttons_layout = QtWidgets.QHBoxLayout()
        self.add_output_button = QtWidgets.QPushButton()
        self.add_output_button.setObjectName("add_output_button")
        self.add_output_button.clicked.connect(self._add_output)
        output_buttons_layout.addWidget(self.add_output_button)

        self.delete_output_button = QtWidgets.QPushButton()
        self.delete_output_button.setObjectName("delete_output_button")
        self.delete_output_button.clicked.connect(self._delete_output)
        output_buttons_layout.addWidget(self.delete_output_button)
        outputs_layout.addLayout(output_buttons_layout)

        self.outputs_list = QtWidgets.QListWidget()
        self.outputs_list.setObjectName("outputs_list")
        self.outputs_list.setMaximumHeight(120)
        outputs_layout.addWidget(self.outputs_list)
        main_layout.addWidget(outputs_group)

        # Variable info section
        info_group = QtWidgets.QGroupBox()
        info_group.setObjectName("info_group")
        info_layout = QtWidgets.QVBoxLayout(info_group)

        self.variable_info_label = QtWidgets.QLabel()
        self.variable_info_label.setObjectName("variable_info_label")
        info_layout.addWidget(self.variable_info_label)

        self.variable_info_text = QtWidgets.QTextEdit()
        self.variable_info_text.setObjectName("variable_info_text")
        self.variable_info_text.setReadOnly(True)
        self.variable_info_text.setMaximumHeight(150)
        info_layout.addWidget(self.variable_info_text)
        main_layout.addWidget(info_group)

        # Add stretch to push everything to top
        main_layout.addStretch()

        self.inputs_list.itemSelectionChanged.connect(self._on_input_selected)
        self.outputs_list.itemSelectionChanged.connect(self._on_output_selected)

        self._update_ui_from_model()

    def _retranslate_ui(self):
        """Add text to all the respective GUI elements."""
        self.title_label.setText(self.t("FIS_PROPERTIES"))
        self.system_name_label.setText(self.t("SYSTEM_NAME"))
        self.system_type_label.setText(self.t("SYSTEM_TYPE"))
        self.defuzzification_label.setText(self.t("DEFUZZIFICATION_METHOD"))
        self.inputs_label.setText(self.t("INPUT_VARIABLES"))
        self.outputs_label.setText(self.t("OUTPUT_VARIABLES"))
        self.add_input_button.setText(self.t("ADD_INPUT"))
        self.delete_input_button.setText(self.t("DELETE_INPUT"))
        self.add_output_button.setText(self.t("ADD_OUTPUT"))
        self.delete_output_button.setText(self.t("DELETE_OUTPUT"))
        self.variable_info_label.setText(self.t("VARIABLE_INFO"))

        # Update system type combo with translated items
        current_selection = self.system_type_combo.currentText()
        self.system_type_combo.clear()
        self.system_type_combo.addItems([self.t("MAMDANI"), self.t("SUGENO")])

        # Restore selection if possible
        if current_selection:
            # Map old values to new translated values
            if current_selection == "mamfis" or current_selection == self.t("MAMDANI"):
                self.system_type_combo.setCurrentText(self.t("MAMDANI"))
            elif current_selection == "sugfis" or current_selection == self.t("SUGENO"):
                self.system_type_combo.setCurrentText(self.t("SUGENO"))
        else:
            # Set based on current system type
            display_type = self.view_model.get_fis_type_display()
            self.system_type_combo.setCurrentText(self.t(display_type.upper()))

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
        """Handle system type change - convert the system if needed."""
        # Get current system type
        current_type = self.view_model.get_fis_type_display()
        current_type_translated = self.t(current_type.upper())

        # Only convert if the type actually changed
        if system_type != current_type_translated:
            # Convert the system
            success = self.view_model.convert_inference_system()
            if success:
                # Update UI after conversion
                self._update_ui_from_model()
            else:
                # Revert combo box selection if conversion failed
                self.system_type_combo.setCurrentText(current_type_translated)

    def _on_defuzzification_changed(self, method_text):
        """Handle defuzzification method change."""
        method_map = {
            self.t("CENTROID"): "centroid",
            self.t("BISECTOR"): "bisector",
            self.t("MOM"): "mom",
            self.t("SOM"): "som",
            self.t("LOM"): "lom",
            self.t("WTAVER"): "wtaver",
        }
        method = method_map.get(method_text, "centroid")
        self.view_model.set_defuzzification_method(method)

    def _add_input(self):
        """Add a new input variable - matches TopMenu functionality."""
        input_count = self.view_model.fuzzy_service.get_input_count()
        success = self.view_model.fuzzy_service.add_input_variable(f"input{input_count + 1}", 0.0, 1.0)
        if success:
            self.view_model._update_system_info()
            self._update_ui_from_model()
            self.view_model.notify_data_changed.emit()

    def _add_output(self):
        """Add a new output variable - matches TopMenu functionality."""
        output_count = self.view_model.fuzzy_service.get_output_count()
        success = self.view_model.fuzzy_service.add_output_variable(f"output{output_count + 1}", 0.0, 1.0)
        if success:
            self.view_model._update_system_info()
            self._update_ui_from_model()
            self.view_model.notify_data_changed.emit()

    def _delete_input(self):
        """Delete the selected input variable."""
        current_item = self.inputs_list.currentItem()
        if current_item:
            # Extract input name from item text
            item_text = current_item.text()
            input_name = item_text.split(" (")[0]  # Get name before " (Range:..."

            # Find the input index
            inputs = self.view_model.inputs
            for idx, inp in enumerate(inputs):
                if inp["name"] == input_name:
                    self.view_model.delete_input(idx)
                    self._update_ui_from_model()
                    break

    def _delete_output(self):
        """Delete the selected output variable."""
        current_item = self.outputs_list.currentItem()
        if current_item:
            # Extract output name from item text
            item_text = current_item.text()
            output_name = item_text.split(" (")[0]  # Get name before " (Range:..."

            # Find the output index
            outputs = self.view_model.outputs
            for idx, out in enumerate(outputs):
                if out["name"] == output_name:
                    self.view_model.delete_output(idx)
                    self._update_ui_from_model()
                    break

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
        self.system_name_edit.setText(self.view_model.system_name)

        # Update system type combo with translated value
        display_type = self.view_model.get_fis_type_display()
        self.system_type_combo.blockSignals(True)
        self.system_type_combo.setCurrentText(self.t(display_type.upper()))
        self.system_type_combo.blockSignals(False)

        # Update defuzzification combo
        available_methods = self.view_model.get_available_defuzzification_methods()
        current_method = self.view_model.get_defuzzification_method()
        self.defuzzification_combo.blockSignals(True)
        self.defuzzification_combo.clear()
        for method in available_methods:
            self.defuzzification_combo.addItem(self.t(method.upper()))
        if current_method in available_methods:
            self.defuzzification_combo.setCurrentText(self.t(current_method.upper()))
        self.defuzzification_combo.blockSignals(False)

        self._update_inputs_list()
        self._update_outputs_list()

    def _update_inputs_list(self):
        """Update the inputs list."""
        self.inputs_list.clear()
        for input_var in self.view_model.inputs:
            item_text = (
                f"{input_var['name']} ({self.t('RANGE')}: {input_var['range']}, {self.t('MFS')}: "
                f"{input_var['mf_count']})"
            )
            self.inputs_list.addItem(item_text)

    def _update_outputs_list(self):
        """Update the outputs list."""
        self.outputs_list.clear()
        for output_var in self.view_model.outputs:
            item_text = (
                f"{output_var['name']} ({self.t('RANGE')}: {output_var['range']}, {self.t('MFS')}: "
                f"{output_var['mf_count']})"
            )
            self.outputs_list.addItem(item_text)

    def _update_variable_info(self, variable_name, variable_type):
        """Update the variable info text."""
        info = self.view_model.get_variable_info(variable_name, variable_type)
        if info:
            info_text = f"{self.t('NAME')}: {info['name']}\n"
            info_text += f"{self.t('TYPE')}: {variable_type}\n"
            info_text += f"{self.t('RANGE')}: {info['range']}\n"
            info_text += f"{self.t('MEMBERSHIP_FUNCTIONS')}: {info['mf_count']}\n\n"

            if info["membership_functions"]:
                info_text += f"{self.t('MEMBERSHIP_FUNCTIONS')}: \n"
                for mf in info["membership_functions"]:
                    info_text += f" - {mf['name']} ({mf['type']}): {mf['parameters']}\n"

            self.variable_info_text.setText(info_text)
        else:
            self.variable_info_text.setText(self.t("NO_VARIABLE_SELECTED"))
