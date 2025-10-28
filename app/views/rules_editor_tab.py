"""Create a tab GUI object to insert into editor tab on the right of main window.

Classes:
    RulesEditorTab: button area element inheriting from QTabWidget.
"""

from PyQt6 import QtCore, QtGui, QtWidgets

from app.view_models.rules_editor_view_model import RulesEditorViewModel
from app.views.base_widget_view import BaseWidgetView


class RulesEditorTab(BaseWidgetView):
    """Class inheriting from QWidget.

    Allows user interaction via QPushButton, QLineEdit and QComboBox GUI elements.
    The class allows to change the parameters of the rules interference logic.

    Methods:
        __init__(parent): create an instance of RulesEditorTab and bind it to the
            parent window.

    Attributes:
        is_or_radio_changed: pyqtSignal which gets emitted to backend whenever one
            of the is or radio buttons gets clicked.
        is_dropdown_changed: pyqtSignal which gets emitted to backend whenever is
            or isn't condition gets changed.
        mf_changed: pyqtSignal which gets emitted to backend whenever a chosen mf
            gets changed.
    """

    is_or_radio_changed = QtCore.pyqtSignal()
    is_dropdown_changed = QtCore.pyqtSignal()
    mf_changed = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        """Initialize a new class instance.

        Args:
            parent (QWidget, optional): The parent widget, in this case editor
                tab, to which the widget will be attached. Defaults to None.
        """
        super().__init__(parent=parent)
        self.setObjectName("rules_properties_tab")

        self.view_model = RulesEditorViewModel()
        self.view_model.setParent(self)
        self.set_view_model(self.view_model)

        self._connect_view_model_signals()

        self._setup_ui()
        self._retranslate_ui()

    def _connect_view_model_signals(self):
        """Connect view model signals to view methods."""
        self.view_model.rules_updated.connect(self._update_rules_list)
        self.view_model.input_mf_options_updated.connect(self._update_input_mf_dropdowns)
        self.view_model.output_mf_options_updated.connect(self._update_output_mf_dropdowns)
        self.view_model.data_changed.connect(self._on_data_changed)

    def _on_data_changed(self):
        """Handle data changed signal from view model."""
        self.refresh_ui()

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
        input_mf_list = (
            self.view_model.input_mf_options if self.view_model.input_mf_options else ["No input MFs available"]
        )
        output_mf_list = (
            self.view_model.output_mf_options if self.view_model.output_mf_options else ["No output MFs available"]
        )

        self.rule_name_label = QtWidgets.QLabel(parent=self)
        self.rule_name_label.setGeometry(QtCore.QRect(10, 50, 55, 16))
        self.rule_name_label.setObjectName("rule_name_label")

        self.rule_weight_edit = QtWidgets.QLineEdit(parent=self)
        self.rule_weight_edit.setGeometry(QtCore.QRect(100, 90, 161, 31))
        self.rule_weight_edit.setObjectName("rule_weight_edit")

        self.rule_weight_label = QtWidgets.QLabel(parent=self)
        self.rule_weight_label.setGeometry(QtCore.QRect(10, 100, 55, 18))
        self.rule_weight_label.setObjectName("rule_weight_label")

        self.rule_name_edit = QtWidgets.QLineEdit(parent=self)
        self.rule_name_edit.setGeometry(QtCore.QRect(100, 40, 161, 31))
        self.rule_name_edit.setObjectName("rule_name_edit")

        self.rule_editor_label = QtWidgets.QLabel(parent=self)
        self.rule_editor_label.setGeometry(QtCore.QRect(0, 0, 121, 31))
        self.rule_editor_label.setObjectName("rule_editor_label")

        self.if_label = QtWidgets.QLabel(parent=self)
        self.if_label.setGeometry(QtCore.QRect(10, 180, 51, 21))
        self.if_label.setObjectName("if_label")

        self.if_line = QtWidgets.QFrame(parent=self)
        self.if_line.setGeometry(QtCore.QRect(10, 200, 241, 20))
        self.if_line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.if_line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.if_line.setObjectName("if_line")

        self.then_line = QtWidgets.QFrame(parent=self)
        self.then_line.setGeometry(QtCore.QRect(10, 440, 241, 20))
        self.then_line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.then_line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.then_line.setObjectName("then_line")

        self.then_label = QtWidgets.QLabel(parent=self)
        self.then_label.setGeometry(QtCore.QRect(10, 420, 51, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.then_label.setFont(font)
        self.then_label.setObjectName("then_label")

        self.first_input_rule_label = QtWidgets.QLabel(parent=self)
        self.first_input_rule_label.setGeometry(QtCore.QRect(10, 240, 51, 16))
        self.first_input_rule_label.setObjectName("first_input_rule_label")

        self.first_input_is_isnt_dropdown = QtWidgets.QComboBox(parent=self)
        self.first_input_is_isnt_dropdown.addItems(["Is", "Isn't"])
        self.first_input_is_isnt_dropdown.setGeometry(QtCore.QRect(70, 230, 71, 31))
        self.first_input_is_isnt_dropdown.setObjectName("first_input_is_isnt_dropdown")
        self.first_input_is_isnt_dropdown.currentTextChanged.connect(self.is_dropdown_changed)

        self.first_input_mf_dropdown = QtWidgets.QComboBox(parent=self)
        self.first_input_mf_dropdown.addItems(input_mf_list)
        self.first_input_mf_dropdown.setGeometry(QtCore.QRect(150, 230, 61, 31))
        self.first_input_mf_dropdown.setObjectName("first_input_mf_dropdown")
        self.first_input_mf_dropdown.currentTextChanged.connect(self.mf_changed)

        self.and_or_label = QtWidgets.QLabel(parent=self)
        self.and_or_label.setGeometry(QtCore.QRect(220, 240, 55, 16))
        self.and_or_label.setObjectName("and_or_label")

        self.final_input_mf_dropdown = QtWidgets.QComboBox(parent=self)
        self.final_input_mf_dropdown.addItems(input_mf_list)
        self.final_input_mf_dropdown.setGeometry(QtCore.QRect(150, 270, 61, 31))
        self.final_input_mf_dropdown.setObjectName("final_input_mf_dropdown")
        self.final_input_mf_dropdown.currentTextChanged.connect(self.mf_changed)

        self.final_input_is_isnt_dropdown = QtWidgets.QComboBox(parent=self)
        self.final_input_is_isnt_dropdown.addItems(["Is", "Isn't"])
        self.final_input_is_isnt_dropdown.setGeometry(QtCore.QRect(70, 270, 71, 31))
        self.final_input_is_isnt_dropdown.setObjectName("final_input_is_isnt_dropdown")
        self.final_input_is_isnt_dropdown.currentTextChanged.connect(self.is_dropdown_changed)

        self.final_input_rule_label = QtWidgets.QLabel(parent=self)
        self.final_input_rule_label.setGeometry(QtCore.QRect(10, 280, 51, 16))
        self.final_input_rule_label.setObjectName("final_input_rule_label")

        self.connection_label = QtWidgets.QLabel(parent=self)
        self.connection_label.setGeometry(QtCore.QRect(10, 150, 91, 16))
        self.connection_label.setObjectName("connection_label")

        self.and_radio_button = QtWidgets.QRadioButton(parent=self)
        self.and_radio_button.setGeometry(QtCore.QRect(100, 150, 61, 20))
        self.and_radio_button.setObjectName("and_radio_button")
        self.and_radio_button.clicked.connect(self._radio_button_clicked)

        self.or_radio_button = QtWidgets.QRadioButton(parent=self)
        self.or_radio_button.setGeometry(QtCore.QRect(170, 150, 61, 20))
        self.or_radio_button.setObjectName("or_radio_button")
        self.or_radio_button.clicked.connect(self._radio_button_clicked)

        self.output_rule_label = QtWidgets.QLabel(parent=self)
        self.output_rule_label.setGeometry(QtCore.QRect(10, 470, 51, 16))
        self.output_rule_label.setObjectName("output_rule_label")

        self.output_is_isnt_dropdown = QtWidgets.QComboBox(parent=self)
        self.output_is_isnt_dropdown.addItems(["Is", "Isn't"])
        self.output_is_isnt_dropdown.setGeometry(QtCore.QRect(70, 460, 71, 31))
        self.output_is_isnt_dropdown.setObjectName("output_is_isnt_dropdown")
        self.output_is_isnt_dropdown.currentTextChanged.connect(self._is_dropdown_changed_func)

        self.output_mf_dropdown = QtWidgets.QComboBox(parent=self)
        self.output_mf_dropdown.addItems(output_mf_list)
        self.output_mf_dropdown.setGeometry(QtCore.QRect(150, 460, 61, 31))
        self.output_mf_dropdown.setObjectName("output_mf_dropdown")
        self.output_mf_dropdown.currentTextChanged.connect(self._mf_changed_func)

    def _update_rules_list(self, rules_list):
        """Update the rules list from view model."""
        # This method will be implemented when rules list UI is added
        pass

    def _update_input_mf_dropdowns(self, input_mf_options):
        """Update input MF dropdowns with new options."""
        if hasattr(self, "first_input_mf_dropdown"):
            self.first_input_mf_dropdown.clear()
            self.first_input_mf_dropdown.addItems(input_mf_options)

        if hasattr(self, "final_input_mf_dropdown"):
            self.final_input_mf_dropdown.clear()
            self.final_input_mf_dropdown.addItems(input_mf_options)

    def _update_output_mf_dropdowns(self, output_mf_options):
        """Update output MF dropdowns with new options."""
        if hasattr(self, "output_mf_dropdown"):
            self.output_mf_dropdown.clear()
            self.output_mf_dropdown.addItems(output_mf_options)

    def _retranslate_ui(self):
        """Add text to all the respective GUI elements."""
        self.rule_name_label.setText(self.t("NAME"))
        self.rule_weight_edit.setText(self.t("ONE"))
        self.rule_weight_label.setText(self.t("WEIGHT"))
        self.rule_name_edit.setText(self.t("PLACEHOLDER"))
        self.rule_editor_label.setText(self.t("RULE_EDITOR"))
        self.if_label.setText(self.t("IF"))
        self.then_label.setText(self.t("THEN"))
        self.first_input_rule_label.setText(self.t("RULE_1"))
        self.and_or_label.setText(self.t("AND_OR"))
        self.final_input_rule_label.setText(self.t("RULE_2"))
        self.connection_label.setText(self.t("CONNECTION"))
        self.and_radio_button.setText(self.t("AND"))
        self.or_radio_button.setText(self.t("OR"))
        self.output_rule_label.setText(self.t("RULE_1"))

    def _is_dropdown_changed_func(self):
        """Emit the signal that chosen condition logic was changed to the backend."""
        self.is_dropdown_changed.emit()

    def _radio_button_clicked(self):
        """Emit the signal that chosen connection was changed to the backend."""
        self.is_or_radio_changed.emit()

    def _mf_changed_func(self):
        """Emit the signal that chosen mf was changed to the backend."""
        self.mf_changed.emit()
