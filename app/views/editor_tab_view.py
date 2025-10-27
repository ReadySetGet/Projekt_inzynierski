from PyQt6 import QtCore, QtGui, QtWidgets

from app.views.base_tab_view import BaseTabView
from app.views.fis_properties_tab_view import FisPropertiesTabView

# Removed unused import
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
        self._setup_ui()
        self._retranslate_ui()

    def _setup_ui(self):
        self.fis_properties_tab = FisPropertiesTabView(parent=self)
        self.fis_properties_tab.setObjectName("fis_properties_tab")

        self.system_type_label_1 = QtWidgets.QLabel(parent=self.fis_properties_tab)
        self.system_type_label_1.setGeometry(QtCore.QRect(10, 20, 41, 21))
        self.system_type_label_1.setObjectName("system_type_label_1")

        self.system_name_label = QtWidgets.QLabel(parent=self.fis_properties_tab)
        self.system_name_label.setGeometry(QtCore.QRect(10, 70, 55, 16))
        self.system_name_label.setObjectName("system_name_label")

        self.and_method_label = QtWidgets.QLabel(parent=self.fis_properties_tab)
        self.and_method_label.setGeometry(QtCore.QRect(10, 110, 71, 16))
        self.and_method_label.setObjectName("and_method_label")

        self.or_method_label = QtWidgets.QLabel(parent=self.fis_properties_tab)
        self.or_method_label.setGeometry(QtCore.QRect(10, 150, 71, 16))
        self.or_method_label.setObjectName("or_method_label")
        self.implication_method_label = QtWidgets.QLabel(parent=self.fis_properties_tab)
        self.implication_method_label.setGeometry(QtCore.QRect(10, 190, 141, 16))
        self.implication_method_label.setObjectName("implication_method_label")

        self.aggregation_method_label = QtWidgets.QLabel(parent=self.fis_properties_tab)
        self.aggregation_method_label.setGeometry(QtCore.QRect(10, 230, 121, 16))
        self.aggregation_method_label.setObjectName("aggregation_method_label")

        self.defuzzification_method_label = QtWidgets.QLabel(parent=self.fis_properties_tab)
        self.defuzzification_method_label.setGeometry(QtCore.QRect(0, 295, 141, 21))
        self.defuzzification_method_label.setObjectName("defuzzification_method_label")

        """Dropdown allowing the user to choose their preferred defuzzification method.
        """
        self.defuzzification_dropdown = QtWidgets.QComboBox(parent=self.fis_properties_tab)
        self.defuzzification_dropdown.setGeometry(QtCore.QRect(160, 290, 101, 31))
        self.defuzzification_dropdown.setObjectName("defuzzification_dropdown")
        self.defuzzification_dropdown.addItem("")
        self.defuzzification_dropdown.addItem("")
        self.defuzzification_dropdown.currentTextChanged.connect(self.defuzzification_changed)

        self.system_type_label_2 = QtWidgets.QLabel(parent=self.fis_properties_tab)
        self.system_type_label_2.setGeometry(QtCore.QRect(150, 20, 111, 21))
        self.system_type_label_2.setObjectName("system_type_label_2")

        self.addTab(self.fis_properties_tab, "fis_properties_tab")

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
        # Placeholder
        self.mf_range_edit.setText("[0 100]")

        self.mf_table = QtWidgets.QTableWidget(parent=self.editor_frame)
        self.mf_table.setGeometry(QtCore.QRect(10, 230, 281, 421))
        self.mf_table.setObjectName("mf_table")

        """Table displaying all MFs"""
        self.mf_table.setRowCount(2)
        self.mf_table.setColumnCount(3)
        self.mf_table.setColumnWidth(0, 80)
        self.mf_table.setColumnWidth(1, 80)
        self.mf_table.setColumnWidth(2, 100)

        self.shape_select_dropdown = QtWidgets.QComboBox(parent=self.mf_table)
        self.shape_select_dropdown.addItems(["Gauss", "Trapezoid", "Triangle", "Bell"])
        self.shape_select_dropdown.setObjectName("shape_select_dropdown")

        self.mf_table.setHorizontalHeaderLabels(["Name", "Type", "Parameters"])

        self.mf_table.setItem(0, 0, QtWidgets.QTableWidgetItem("Placeholder"))
        self.mf_table.setCellWidget(0, 1, self.shape_select_dropdown)
        self.mf_table.setItem(0, 2, QtWidgets.QTableWidgetItem(self.mf_range_edit.text()))

        self.mf_range_edit.textChanged.connect(self.set_range_table_text)
        self.mf_name_edit.textChanged.connect(self.set_name_table_text)
        self.shape_select_dropdown.currentTextChanged.connect(self.shape_changed)

        self.add_mf_button = QtWidgets.QPushButton(parent=self.editor_frame)
        self.add_mf_button.setGeometry(QtCore.QRect(60, 190, 93, 28))
        self.add_mf_button.setObjectName("add_mf_button")
        self.add_mf_button.clicked.connect(self.add_mf_clicked.emit)

        self.remove_mf_button = QtWidgets.QPushButton(parent=self.editor_frame)
        self.remove_mf_button.setGeometry(QtCore.QRect(160, 190, 93, 28))
        self.remove_mf_button.setObjectName("remove_mf_button")
        self.remove_mf_button.clicked.connect(self.remove_mf_clicked.emit)

        self.number_of_mf_label = QtWidgets.QLabel(parent=self.editor_frame)
        self.number_of_mf_label.setGeometry(QtCore.QRect(20, 150, 151, 16))
        self.number_of_mf_label.setObjectName("number_of_mf_label")

        self.addTab(self.mf_properties_tab, "mf_properties_tab")

        self.rule_editor_tab = RulesEditorTab(parent=self)
        self.rule_editor_tab.setObjectName("rule_editor_tab")

        self.rule_name_label = QtWidgets.QLabel(parent=self.rule_editor_tab)
        self.rule_name_label.setGeometry(QtCore.QRect(10, 50, 55, 16))
        self.rule_name_label.setObjectName("rule_name_label")

        self.rule_weight_edit = QtWidgets.QLineEdit(parent=self.rule_editor_tab)
        self.rule_weight_edit.setGeometry(QtCore.QRect(100, 90, 161, 31))
        self.rule_weight_edit.setObjectName("rule_weight_edit")

        self.rule_weight_label = QtWidgets.QLabel(parent=self.rule_editor_tab)
        self.rule_weight_label.setGeometry(QtCore.QRect(10, 100, 55, 16))
        self.rule_weight_label.setObjectName("rule_weight_label")

        self.rule_name_edit = QtWidgets.QLineEdit(parent=self.rule_editor_tab)
        self.rule_name_edit.setGeometry(QtCore.QRect(100, 40, 161, 31))
        self.rule_name_edit.setObjectName("rule_name_edit")

        self.rule_editor_label = QtWidgets.QLabel(parent=self.rule_editor_tab)
        self.rule_editor_label.setGeometry(QtCore.QRect(0, 0, 121, 31))
        self.rule_editor_label.setObjectName("rule_editor_label")

        self.if_label = QtWidgets.QLabel(parent=self.rule_editor_tab)
        self.if_label.setGeometry(QtCore.QRect(10, 180, 51, 21))
        self.if_label.setObjectName("if_label")

        self.if_line = QtWidgets.QFrame(parent=self.rule_editor_tab)
        self.if_line.setGeometry(QtCore.QRect(10, 200, 241, 20))
        self.if_line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.if_line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.if_line.setObjectName("if_line")

        self.then_line = QtWidgets.QFrame(parent=self.rule_editor_tab)
        self.then_line.setGeometry(QtCore.QRect(10, 440, 241, 20))
        self.then_line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.then_line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.then_line.setObjectName("then_line")

        self.then_label = QtWidgets.QLabel(parent=self.rule_editor_tab)
        self.then_label.setGeometry(QtCore.QRect(10, 420, 51, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.then_label.setFont(font)
        self.then_label.setObjectName("then_label")

        self.first_input_rule_label = QtWidgets.QLabel(parent=self.rule_editor_tab)
        self.first_input_rule_label.setGeometry(QtCore.QRect(10, 240, 51, 16))
        self.first_input_rule_label.setObjectName("first_input_rule_label")

        self.first_input_is_isnt_dropdown = QtWidgets.QComboBox(parent=self.rule_editor_tab)
        self.first_input_is_isnt_dropdown.addItems(["Is", "Isn't"])
        self.first_input_is_isnt_dropdown.setGeometry(QtCore.QRect(70, 230, 71, 31))
        self.first_input_is_isnt_dropdown.setObjectName("first_input_is_isnt_dropdown")
        self.first_input_is_isnt_dropdown.currentTextChanged.connect(self.is_dropdown_changed)

        self.first_input_mf_dropdown = QtWidgets.QComboBox(parent=self.rule_editor_tab)
        self.first_input_mf_dropdown.addItems(["MF1", "MF2", "MF3"])
        self.first_input_mf_dropdown.setGeometry(QtCore.QRect(150, 230, 61, 31))
        self.first_input_mf_dropdown.setObjectName("first_input_mf_dropdown")
        self.first_input_mf_dropdown.currentTextChanged.connect(self.mf_changed)

        self.and_or_label = QtWidgets.QLabel(parent=self.rule_editor_tab)
        self.and_or_label.setGeometry(QtCore.QRect(220, 240, 55, 16))
        self.and_or_label.setObjectName("and_or_label")

        self.final_input_mf_dropdown = QtWidgets.QComboBox(parent=self.rule_editor_tab)
        # input_mf_list will be populated by the view model
        self.final_input_mf_dropdown.setGeometry(QtCore.QRect(150, 270, 61, 31))
        self.final_input_mf_dropdown.setObjectName("final_input_mf_dropdown")
        self.final_input_mf_dropdown.currentTextChanged.connect(self.mf_changed)

        self.final_input_is_isnt_dropdown = QtWidgets.QComboBox(parent=self.rule_editor_tab)
        self.final_input_is_isnt_dropdown.addItems(["Is", "Isn't"])
        self.final_input_is_isnt_dropdown.setGeometry(QtCore.QRect(70, 270, 71, 31))
        self.final_input_is_isnt_dropdown.setObjectName("final_input_is_isnt_dropdown")
        self.final_input_is_isnt_dropdown.currentTextChanged.connect(self.is_dropdown_changed)

        self.final_input_rule_label = QtWidgets.QLabel(parent=self.rule_editor_tab)
        self.final_input_rule_label.setGeometry(QtCore.QRect(10, 280, 51, 16))
        self.final_input_rule_label.setObjectName("final_input_rule_label")

        self.connection_label = QtWidgets.QLabel(parent=self.rule_editor_tab)
        self.connection_label.setGeometry(QtCore.QRect(10, 150, 91, 16))
        self.connection_label.setObjectName("connection_label")

        self.and_radio_button = QtWidgets.QRadioButton(parent=self.rule_editor_tab)
        self.and_radio_button.setGeometry(QtCore.QRect(100, 150, 61, 20))
        self.and_radio_button.setObjectName("and_radio_button")
        self.and_radio_button.clicked.connect(self.radio_button_clicked)

        self.or_radio_button = QtWidgets.QRadioButton(parent=self.rule_editor_tab)
        self.or_radio_button.setGeometry(QtCore.QRect(170, 150, 61, 20))
        self.or_radio_button.setObjectName("or_radio_button")
        self.or_radio_button.clicked.connect(self.radio_button_clicked)

        self.output_rule_label = QtWidgets.QLabel(parent=self.rule_editor_tab)
        self.output_rule_label.setGeometry(QtCore.QRect(10, 470, 51, 16))
        self.output_rule_label.setObjectName("output_rule_label")

        self.output_is_isnt_dropdown = QtWidgets.QComboBox(parent=self.rule_editor_tab)
        self.output_is_isnt_dropdown.addItems(["Is", "Isn't"])
        self.output_is_isnt_dropdown.setGeometry(QtCore.QRect(70, 460, 71, 31))
        self.output_is_isnt_dropdown.setObjectName("output_is_isnt_dropdown")
        self.output_is_isnt_dropdown.currentTextChanged.connect(self.is_dropdown_changed)

        self.output_mf_dropdown = QtWidgets.QComboBox(parent=self.rule_editor_tab)
        # output_mf_list will be populated by the view model
        self.output_mf_dropdown.setGeometry(QtCore.QRect(150, 460, 61, 31))
        self.output_mf_dropdown.setObjectName("output_mf_dropdown")
        self.output_mf_dropdown.currentTextChanged.connect(self.mf_changed)
        self.addTab(self.rule_editor_tab, "rule_editor_tab")

        self._retranslate_ui()

    def _retranslate_ui(self):
        self.system_type_label_1.setText(self.t("TYPE"))
        self.system_name_label.setText(self.t("NAME"))
        self.and_method_label.setText(self.t("AND_METHOD"))
        self.or_method_label.setText(self.t("OR_METHOD"))
        self.implication_method_label.setText(self.t("IMPLICATION_METHOD"))
        self.aggregation_method_label.setText(self.t("AGGREGATION_METHOD"))
        self.defuzzification_method_label.setText(self.t("DEFUZZIFICATION_METHOD"))
        self.defuzzification_dropdown.setItemText(0, self.t("CENTROID"))
        self.defuzzification_dropdown.setItemText(1, self.t("BISECTOR"))
        self.system_type_label_2.setText(self.t("SYSTEM_TYPE"))
        self.setTabText(
            self.indexOf(self.fis_properties_tab),
            self.t("FIS_PROPERTIES_TAB"),
        )
        self.property_editor_label.setText(self.t("PROPERTY_EDITOR"))
        self.mf_name_label.setText(self.t("NAME"))
        self.mf_range_label.setText(self.t("RANGE"))
        self.mf_name_edit.setText(self.t("PLACEHOLDER"))
        self.mf_range_edit.setText(self.t("RANGE_0_100"))
        self.add_mf_button.setText(self.t("ADD_MF"))
        self.remove_mf_button.setText(self.t("REMOVE_MF"))
        self.number_of_mf_label.setText(self.t("NUMBER_OF_MF"))
        self.setTabText(
            self.indexOf(self.mf_properties_tab),
            self.t("MF_PROPERTIES_TAB"),
        )
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
        self.setTabText(
            self.indexOf(self.rule_editor_tab),
            self.t("RULE_PROPERTIES_TAB"),
        )

    def get_mf_name(self) -> str:
        """Get the membership function name from the edit field."""
        return self.mf_name_edit.text()

    def set_number_of_mf(self, count: int):
        """Set the number of membership functions label."""
        self.number_of_mf_label.setText(f"Number of MF: {count}")

    def set_name_table_text(self):
        """Update the MF name in the table."""
        self.mf_table.item(self.row, 0).setText(self.mf_name_edit.text())
        self.status_bar.showMessage("Last action: Edited MF name")

    def set_range_table_text(self):
        """Update the MF range in the table."""
        self.mf_table.item(self.row, 2).setText(self.mf_range_edit.text())
        self.status_bar.showMessage("Last action: Edited MF range")

    def shape_changed(self):
        """Handle membership function shape change."""
        self.status_bar.showMessage("Last action: Edited MF shape")

    def defuzzification_changed(self):
        """Handle defuzzification method change."""
        self.status_bar.showMessage("Last action: Changed defuzzification method.")

    def is_dropdown_changed(self):
        """Handle is/is not dropdown change."""
        self.status_bar.showMessage("Last action: Changed is or is not.")

    def radio_button_clicked(self):
        """Handle and/or radio button click."""
        self.status_bar.showMessage("Last action: And/or radio button clicked.")

    def mf_changed(self):
        """Handle membership function selection change."""
        self.status_bar.showMessage("Last action: Changed selected membership function.")
