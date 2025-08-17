from PyQt6 import QtCore, QtGui, QtWidgets


class EditorTabWidget(QtWidgets.QTabWidget):
    add_mf_clicked = QtCore.pyqtSignal()
    remove_mf_clicked = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("editorTab")
        self._setup_ui()
        self._retranslate_ui()

    def _setup_ui(self):
        input_mf_list = ['Placeholder Input MF']
        output_mf_list = ['Placeholder Output MF']

        self.fis_properties_tab = QtWidgets.QWidget()
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

        self.defuzzification_dropdown = QtWidgets.QComboBox(parent=self.fis_properties_tab)
        self.defuzzification_dropdown.setGeometry(QtCore.QRect(160, 290, 101, 31))
        self.defuzzification_dropdown.setObjectName("defuzzification_dropdown")
        self.defuzzification_dropdown.addItem("")
        self.defuzzification_dropdown.addItem("")

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
        #Placeholder
        self.mf_range_edit.setText("[0 100]")

        self.mf_table = QtWidgets.QTableWidget(parent=self.editor_frame)
        self.mf_table.setGeometry(QtCore.QRect(10, 230, 281, 421))
        self.mf_table.setObjectName("mf_table")

        self.mf_table.setRowCount(2)
        self.mf_table.setColumnCount(3)
        self.mf_table.setColumnWidth(0, 80)
        self.mf_table.setColumnWidth(1, 80)
        self.mf_table.setColumnWidth(2, 100)

        self.shape_select_dropdown = QtWidgets.QComboBox(parent=self.mf_table)
        self.shape_select_dropdown.addItems(['Gauss', 'Trapezoid', 'Triangle', 'Bell'])
        self.shape_select_dropdown.setObjectName("shape_select_dropdown")

        self.mf_table.setItem(0, 0, QtWidgets.QTableWidgetItem("Name"))
        self.mf_table.setItem(0, 1, QtWidgets.QTableWidgetItem("Type"))
        self.mf_table.setItem(0, 2, QtWidgets.QTableWidgetItem("Parameters"))

        self.mf_table.setItem(1, 0, QtWidgets.QTableWidgetItem("Placeholder"))
        self.mf_table.setCellWidget(1, 1, self.shape_select_dropdown)
        self.mf_table.setItem(1, 2, QtWidgets.QTableWidgetItem(self.mf_range_edit.text()))

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

        self.rule_editor_tab = QtWidgets.QWidget()
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
        self.first_input_is_isnt_dropdown.addItems(['Is', 'Isn\'t'])
        self.first_input_is_isnt_dropdown.setGeometry(QtCore.QRect(70, 230, 71, 31))
        self.first_input_is_isnt_dropdown.setObjectName("first_input_is_isnt_dropdown")

        self.first_input_mf_dropdown = QtWidgets.QComboBox(parent=self.rule_editor_tab)
        self.first_input_mf_dropdown.addItems(input_mf_list)
        self.first_input_mf_dropdown.setGeometry(QtCore.QRect(150, 230, 61, 31))
        self.first_input_mf_dropdown.setObjectName("first_input_mf_dropdown")

        self.and_or_label = QtWidgets.QLabel(parent=self.rule_editor_tab)
        self.and_or_label.setGeometry(QtCore.QRect(220, 240, 55, 16))
        self.and_or_label.setObjectName("and_or_label")

        self.final_input_mf_dropdown = QtWidgets.QComboBox(parent=self.rule_editor_tab)
        self.final_input_mf_dropdown.addItems(input_mf_list)
        self.final_input_mf_dropdown.setGeometry(QtCore.QRect(150, 270, 61, 31))
        self.final_input_mf_dropdown.setObjectName("final_input_mf_dropdown")

        self.final_input_is_isnt_dropdown = QtWidgets.QComboBox(parent=self.rule_editor_tab)
        self.final_input_is_isnt_dropdown.addItems(['Is', 'Isn\'t'])
        self.final_input_is_isnt_dropdown.setGeometry(QtCore.QRect(70, 270, 71, 31))
        self.final_input_is_isnt_dropdown.setObjectName("final_input_is_isnt_dropdown")

        self.final_input_rule_label = QtWidgets.QLabel(parent=self.rule_editor_tab)
        self.final_input_rule_label.setGeometry(QtCore.QRect(10, 280, 51, 16))
        self.final_input_rule_label.setObjectName("final_input_rule_label")

        self.connection_label = QtWidgets.QLabel(parent=self.rule_editor_tab)
        self.connection_label.setGeometry(QtCore.QRect(10, 150, 91, 16))
        self.connection_label.setObjectName("connection_label")

        self.and_radio_button = QtWidgets.QRadioButton(parent=self.rule_editor_tab)
        self.and_radio_button.setGeometry(QtCore.QRect(100, 150, 61, 20))
        self.and_radio_button.setObjectName("and_radio_button")

        self.or_radio_button = QtWidgets.QRadioButton(parent=self.rule_editor_tab)
        self.or_radio_button.setGeometry(QtCore.QRect(170, 150, 61, 20))
        self.or_radio_button.setObjectName("or_radio_button")

        self.output_rule_label = QtWidgets.QLabel(parent=self.rule_editor_tab)
        self.output_rule_label.setGeometry(QtCore.QRect(10, 470, 51, 16))
        self.output_rule_label.setObjectName("output_rule_label")

        self.output_is_isnt_dropdown = QtWidgets.QComboBox(parent=self.rule_editor_tab)
        self.output_is_isnt_dropdown.addItems(['Is', 'Isn\'t'])
        self.output_is_isnt_dropdown.setGeometry(QtCore.QRect(70, 460, 71, 31))
        self.output_is_isnt_dropdown.setObjectName("output_is_isnt_dropdown")

        self.output_mf_dropdown = QtWidgets.QComboBox(parent=self.rule_editor_tab)
        self.output_mf_dropdown.addItems(output_mf_list)
        self.output_mf_dropdown.setGeometry(QtCore.QRect(150, 460, 61, 31))
        self.output_mf_dropdown.setObjectName("output_mf_dropdown")

        self.addTab(self.rule_editor_tab, "rule_editor_tab")

        self._retranslate_ui()

    def _retranslate_ui(self):
        _translate = QtCore.QCoreApplication.translate

        self.system_type_label_1.setText(_translate("MainWindow", "Type:"))
        self.system_name_label.setText(_translate("MainWindow", "Name"))
        self.and_method_label.setText(_translate("MainWindow", "And method"))
        self.or_method_label.setText(_translate("MainWindow", "Or method"))
        self.implication_method_label.setText(_translate("MainWindow", "Implication method"))
        self.aggregation_method_label.setText(_translate("MainWindow", "Aggregation method"))
        self.defuzzification_method_label.setText(_translate("MainWindow", "Defuzzification method"))
        self.defuzzification_dropdown.setItemText(0, _translate("MainWindow", "centroid"))
        self.defuzzification_dropdown.setItemText(1, _translate("MainWindow", "bisector"))
        self.system_type_label_2.setText(_translate("MainWindow", "System_type"))
        self.setTabText(self.indexOf(self.fis_properties_tab), _translate("MainWindow", "fisPropertiesTab"))
        self.property_editor_label.setText(_translate("MainWindow", "Property Editor"))
        self.mf_name_label.setText(_translate("MainWindow", "Name"))
        self.mf_range_label.setText(_translate("MainWindow", "Range"))
        self.mf_name_edit.setText(_translate("MainWindow", "Placeholder"))
        self.mf_range_edit.setText(_translate("MainWindow", "[0 100]"))
        self.add_mf_button.setText(_translate("MainWindow", "Add MF"))
        self.remove_mf_button.setText(_translate("MainWindow", "Remove MF"))
        self.number_of_mf_label.setText(_translate("MainWindow", "Number of MF:"))
        self.setTabText(self.indexOf(self.mf_properties_tab), _translate("MainWindow", "mfPropertiesTab"))
        self.rule_name_label.setText(_translate("MainWindow", "Name"))
        self.rule_weight_edit.setText(_translate("MainWindow", "1"))
        self.rule_weight_label.setText(_translate("MainWindow", "Weight"))
        self.rule_name_edit.setText(_translate("MainWindow", "Placeholder"))
        self.rule_editor_label.setText(_translate("MainWindow", "Rule Editor"))
        self.if_label.setText(_translate("MainWindow", "If"))
        self.then_label.setText(_translate("MainWindow", "Then"))
        self.first_input_rule_label.setText(_translate("MainWindow", "Rule 1"))
        self.and_or_label.setText(_translate("MainWindow", "and/or"))
        self.final_input_rule_label.setText(_translate("MainWindow", "Rule 2"))
        self.connection_label.setText(_translate("MainWindow", "Connection"))
        self.and_radio_button.setText(_translate("MainWindow", "And"))
        self.or_radio_button.setText(_translate("MainWindow", "Or"))
        self.output_rule_label.setText(_translate("MainWindow", "Rule 1"))
        self.setTabText(self.indexOf(self.rule_editor_tab), _translate("MainWindow", "rulePropertiesTab"))

    def get_mf_name(self) -> str:
        return self.mf_name_edit.text()

    def set_number_of_mf(self, count: int):
        self.number_of_mf_label.setText(f"Number of MF: {count}")
