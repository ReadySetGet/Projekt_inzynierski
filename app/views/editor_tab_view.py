from PyQt6 import QtCore, QtGui, QtWidgets


class EditorTabWidget(QtWidgets.QTabWidget):
    defuzzification_changed_signal = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("editorTab")
        self._setup_ui()
        self._retranslate_ui()

    def _setup_ui(self):
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

        """Dropdown allowing the user to choose their prefered defuzzififcation method."""
        self.defuzzification_dropdown = QtWidgets.QComboBox(parent=self.fis_properties_tab)
        self.defuzzification_dropdown.setGeometry(QtCore.QRect(160, 290, 101, 31))
        self.defuzzification_dropdown.setObjectName("defuzzification_dropdown")
        self.defuzzification_dropdown.addItem("")
        self.defuzzification_dropdown.addItem("")
        self.defuzzification_dropdown.addItem("")
        self.defuzzification_dropdown.currentTextChanged.connect(self.defuzzification_changed)

        self.system_type_label_2 = QtWidgets.QLabel(parent=self.fis_properties_tab)
        self.system_type_label_2.setGeometry(QtCore.QRect(150, 20, 111, 21))
        self.system_type_label_2.setObjectName("system_type_label_2")

        self.addTab(self.fis_properties_tab, "fis_properties_tab")

        self.mf_properties_tab = QtWidgets.QWidget()
        self.mf_properties_tab.setObjectName("fis_properties_tab")

        self.addTab(self.mf_properties_tab, "mf_properties_tab")

        self.rule_editor_tab = QtWidgets.QWidget()
        self.rule_editor_tab.setObjectName("rule_editor_tab")

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
        self.defuzzification_dropdown.setItemText(2, _translate("MainWindow", "lom"))
        self.system_type_label_2.setText(_translate("MainWindow", "System_type"))
        self.setTabText(self.indexOf(self.fis_properties_tab), _translate("MainWindow", "fisPropertiesTab"))
        self.setTabText(self.indexOf(self.mf_properties_tab), _translate("MainWindow", "mfPropertiesTab"))
        self.setTabText(self.indexOf(self.rule_editor_tab), _translate("MainWindow", "rulePropertiesTab"))

    def defuzzification_changed(self):
        self.defuzzification_changed_signal.emit()
