from PyQt6 import QtCore, QtGui, QtWidgets


class RulesEditorTab(QtWidgets.QWidget):
    defuzzification_dropdown_changed = QtCore.pyqtSignal()
    is_or_radio_changed = QtCore.pyqtSignal()
    is_dropdown_changed = QtCore.pyqtSignal()
    mf_changed = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("rules_properties_tab")
        self._setup_ui()
        self._retranslate_ui()

    def _setup_ui(self):
        input_mf_list = ['Placeholder Input MF']
        output_mf_list = ['Placeholder Output MF']

        self.rule_name_label = QtWidgets.QLabel(parent=self)
        self.rule_name_label.setGeometry(QtCore.QRect(10, 50, 55, 16))
        self.rule_name_label.setObjectName("rule_name_label")

        self.rule_weight_edit = QtWidgets.QLineEdit(parent=self)
        self.rule_weight_edit.setGeometry(QtCore.QRect(100, 90, 161, 31))
        self.rule_weight_edit.setObjectName("rule_weight_edit")

        self.rule_weight_label = QtWidgets.QLabel(parent=self)
        self.rule_weight_label.setGeometry(QtCore.QRect(10, 100, 55, 16))
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
        self.first_input_is_isnt_dropdown.addItems(['Is', 'Isn\'t'])
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
        self.final_input_is_isnt_dropdown.addItems(['Is', 'Isn\'t'])
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
        self.and_radio_button.clicked.connect(self.radio_button_clicked)

        self.or_radio_button = QtWidgets.QRadioButton(parent=self)
        self.or_radio_button.setGeometry(QtCore.QRect(170, 150, 61, 20))
        self.or_radio_button.setObjectName("or_radio_button")
        self.or_radio_button.clicked.connect(self.radio_button_clicked)

        self.output_rule_label = QtWidgets.QLabel(parent=self)
        self.output_rule_label.setGeometry(QtCore.QRect(10, 470, 51, 16))
        self.output_rule_label.setObjectName("output_rule_label")

        self.output_is_isnt_dropdown = QtWidgets.QComboBox(parent=self)
        self.output_is_isnt_dropdown.addItems(['Is', 'Isn\'t'])
        self.output_is_isnt_dropdown.setGeometry(QtCore.QRect(70, 460, 71, 31))
        self.output_is_isnt_dropdown.setObjectName("output_is_isnt_dropdown")
        self.output_is_isnt_dropdown.currentTextChanged.connect(self.is_dropdown_changed_func)

        self.output_mf_dropdown = QtWidgets.QComboBox(parent=self)
        self.output_mf_dropdown.addItems(output_mf_list)
        self.output_mf_dropdown.setGeometry(QtCore.QRect(150, 460, 61, 31))
        self.output_mf_dropdown.setObjectName("output_mf_dropdown")
        self.output_mf_dropdown.currentTextChanged.connect(self.mf_changed_func)

    def _retranslate_ui(self):
        _translate = QtCore.QCoreApplication.translate
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

    def defuzzification_changed(self):
        self.defuzzification_dropdown_changed.emit()

    def is_dropdown_changed_func(self):
        self.is_dropdown_changed.emit()

    def radio_button_clicked(self):
        self.is_or_radio_changed.emit()

    def mf_changed_func(self):
        self.mf_changed.emit()
