from PyQt6 import QtCore, QtGui, QtWidgets


class EditorTabWidget(QtWidgets.QTabWidget):
    addMFClicked = QtCore.pyqtSignal()
    removeMFClicked = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("editorTab")
        self._setup_ui()

    def _setup_ui(self):
        self.fisPropertiesTab = QtWidgets.QWidget()
        self.fisPropertiesTab.setObjectName("fisPropertiesTab")

        self.addTab(self.fisPropertiesTab, "fisPropertiesTab")

        self.mfPropertiesTab = QtWidgets.QWidget()
        self.mfPropertiesTab.setObjectName("mfPropertiesTab")

        self.editorFrame = QtWidgets.QFrame(parent=self.mfPropertiesTab)
        self.editorFrame.setGeometry(QtCore.QRect(-10, 0, 291, 641))
        self.editorFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.editorFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.editorFrame.setObjectName("editorFrame")

        self.propertyEditorLabel = QtWidgets.QLabel(parent=self.editorFrame)
        self.propertyEditorLabel.setGeometry(QtCore.QRect(10, 0, 121, 31))
        self.propertyEditorLabel.setObjectName("propertyEditorLabel")

        self.mfNameLabel = QtWidgets.QLabel(parent=self.editorFrame)
        self.mfNameLabel.setGeometry(QtCore.QRect(20, 50, 55, 16))
        self.mfNameLabel.setObjectName("mfNameLabel")

        self.mfRangeLabel = QtWidgets.QLabel(parent=self.editorFrame)
        self.mfRangeLabel.setGeometry(QtCore.QRect(20, 100, 55, 16))
        self.mfRangeLabel.setObjectName("mfRangeLabel")

        self.mfNameEdit = QtWidgets.QLineEdit(parent=self.editorFrame)
        self.mfNameEdit.setGeometry(QtCore.QRect(110, 40, 161, 31))
        self.mfNameEdit.setObjectName("mfNameEdit")

        self.mfRangeEdit = QtWidgets.QLineEdit(parent=self.editorFrame)
        self.mfRangeEdit.setGeometry(QtCore.QRect(110, 90, 161, 31))
        self.mfRangeEdit.setObjectName("mfRangeEdit")

        self.mfTable = QtWidgets.QTableView(parent=self.editorFrame)
        self.mfTable.setGeometry(QtCore.QRect(10, 230, 281, 421))
        self.mfTable.setObjectName("mfTable")

        self.addMFButton = QtWidgets.QPushButton(parent=self.editorFrame)
        self.addMFButton.setGeometry(QtCore.QRect(60, 190, 93, 28))
        self.addMFButton.setObjectName("addMFButton")
        self.addMFButton.clicked.connect(self.addMFClicked.emit)

        self.removeMFButton = QtWidgets.QPushButton(parent=self.editorFrame)
        self.removeMFButton.setGeometry(QtCore.QRect(160, 190, 93, 28))
        self.removeMFButton.setObjectName("removeMFButton")
        self.removeMFButton.clicked.connect(self.removeMFClicked.emit)

        self.numberOfMFLabel = QtWidgets.QLabel(parent=self.editorFrame)
        self.numberOfMFLabel.setGeometry(QtCore.QRect(20, 150, 151, 16))
        self.numberOfMFLabel.setObjectName("numberOfMFLabel")

        self.addTab(self.mfPropertiesTab, "mfPropertiesTab")

        self.ruleEditorTab = QtWidgets.QWidget()
        self.ruleEditorTab.setObjectName("ruleEditorTab")

        self.ruleNameLabel = QtWidgets.QLabel(parent=self.ruleEditorTab)
        self.ruleNameLabel.setGeometry(QtCore.QRect(10, 50, 55, 16))
        self.ruleNameLabel.setObjectName("ruleNameLabel")

        self.ruleWeightEdit = QtWidgets.QLineEdit(parent=self.ruleEditorTab)
        self.ruleWeightEdit.setGeometry(QtCore.QRect(100, 90, 161, 31))
        self.ruleWeightEdit.setObjectName("ruleWeightEdit")

        self.ruleWeightLabel = QtWidgets.QLabel(parent=self.ruleEditorTab)
        self.ruleWeightLabel.setGeometry(QtCore.QRect(10, 100, 55, 16))
        self.ruleWeightLabel.setObjectName("ruleWeightLabel")

        self.ruleNameEdit = QtWidgets.QLineEdit(parent=self.ruleEditorTab)
        self.ruleNameEdit.setGeometry(QtCore.QRect(100, 40, 161, 31))
        self.ruleNameEdit.setObjectName("ruleNameEdit")

        self.ruleEditorLabel = QtWidgets.QLabel(parent=self.ruleEditorTab)
        self.ruleEditorLabel.setGeometry(QtCore.QRect(0, 0, 121, 31))
        self.ruleEditorLabel.setObjectName("ruleEditorLabel")

        self.ifLabel = QtWidgets.QLabel(parent=self.ruleEditorTab)
        self.ifLabel.setGeometry(QtCore.QRect(10, 180, 51, 21))
        self.ifLabel.setObjectName("ifLabel")

        self.ifLine = QtWidgets.QFrame(parent=self.ruleEditorTab)
        self.ifLine.setGeometry(QtCore.QRect(10, 200, 241, 20))
        self.ifLine.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.ifLine.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.ifLine.setObjectName("ifLine")

        self.thenLine = QtWidgets.QFrame(parent=self.ruleEditorTab)
        self.thenLine.setGeometry(QtCore.QRect(10, 440, 241, 20))
        self.thenLine.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.thenLine.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.thenLine.setObjectName("thenLine")

        self.thenLabel = QtWidgets.QLabel(parent=self.ruleEditorTab)
        self.thenLabel.setGeometry(QtCore.QRect(10, 420, 51, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.thenLabel.setFont(font)
        self.thenLabel.setObjectName("thenLabel")

        self.firstInputRuleLabel = QtWidgets.QLabel(parent=self.ruleEditorTab)
        self.firstInputRuleLabel.setGeometry(QtCore.QRect(10, 240, 51, 16))
        self.firstInputRuleLabel.setObjectName("firstInputRuleLabel")

        self.firstInputIsIsntDropdown = QtWidgets.QPushButton(parent=self.ruleEditorTab)
        self.firstInputIsIsntDropdown.setGeometry(QtCore.QRect(70, 230, 71, 31))
        self.firstInputIsIsntDropdown.setObjectName("firstInputIsIsntDropdown")

        self.firstInputMFDropdown = QtWidgets.QPushButton(parent=self.ruleEditorTab)
        self.firstInputMFDropdown.setGeometry(QtCore.QRect(150, 230, 61, 31))
        self.firstInputMFDropdown.setObjectName("firstInputMFDropdown")

        self.andOrLabel = QtWidgets.QLabel(parent=self.ruleEditorTab)
        self.andOrLabel.setGeometry(QtCore.QRect(220, 240, 55, 16))
        self.andOrLabel.setObjectName("andOrLabel")

        self.finalInputMFDropdown = QtWidgets.QPushButton(parent=self.ruleEditorTab)
        self.finalInputMFDropdown.setGeometry(QtCore.QRect(150, 270, 61, 31))
        self.finalInputMFDropdown.setObjectName("finalInputMFDropdown")

        self.finalInputIsIsntDropdown = QtWidgets.QPushButton(parent=self.ruleEditorTab)
        self.finalInputIsIsntDropdown.setGeometry(QtCore.QRect(70, 270, 71, 31))
        self.finalInputIsIsntDropdown.setObjectName("finalInputIsIsntDropdown")

        self.finalInputRuleLabel = QtWidgets.QLabel(parent=self.ruleEditorTab)
        self.finalInputRuleLabel.setGeometry(QtCore.QRect(10, 280, 51, 16))
        self.finalInputRuleLabel.setObjectName("finalInputRuleLabel")

        self.connectionLabel = QtWidgets.QLabel(parent=self.ruleEditorTab)
        self.connectionLabel.setGeometry(QtCore.QRect(10, 150, 91, 16))
        self.connectionLabel.setObjectName("connectionLabel")

        self.andRadioButton = QtWidgets.QRadioButton(parent=self.ruleEditorTab)
        self.andRadioButton.setGeometry(QtCore.QRect(100, 150, 61, 20))
        self.andRadioButton.setObjectName("andRadioButton")

        self.orRadioButton = QtWidgets.QRadioButton(parent=self.ruleEditorTab)
        self.orRadioButton.setGeometry(QtCore.QRect(170, 150, 61, 20))
        self.orRadioButton.setObjectName("orRadioButton")

        self.outputRuleLabel = QtWidgets.QLabel(parent=self.ruleEditorTab)
        self.outputRuleLabel.setGeometry(QtCore.QRect(10, 470, 51, 16))
        self.outputRuleLabel.setObjectName("outputRuleLabel")

        self.outputIsIsntDropdown = QtWidgets.QPushButton(parent=self.ruleEditorTab)
        self.outputIsIsntDropdown.setGeometry(QtCore.QRect(70, 460, 71, 31))
        self.outputIsIsntDropdown.setObjectName("outputIsIsntDropdown")

        self.outputMFDropdown = QtWidgets.QPushButton(parent=self.ruleEditorTab)
        self.outputMFDropdown.setGeometry(QtCore.QRect(150, 460, 61, 31))
        self.outputMFDropdown.setObjectName("outputMFDropdown")

        self.addTab(self.ruleEditorTab, "ruleEditorTab")

        self._retranslate_ui()

    def _retranslate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        self.setTabText(self.indexOf(self.fisPropertiesTab), _translate("MainWindow", "fisPropertiesTab"))
        self.propertyEditorLabel.setText(_translate("MainWindow", "Property Editor"))
        self.mfNameLabel.setText(_translate("MainWindow", "Name"))
        self.mfRangeLabel.setText(_translate("MainWindow", "Range"))
        self.mfNameEdit.setText(_translate("MainWindow", "Placeholder"))
        self.mfRangeEdit.setText(_translate("MainWindow", "[0 100]"))
        self.addMFButton.setText(_translate("MainWindow", "Add MF"))
        self.removeMFButton.setText(_translate("MainWindow", "Remove MF"))
        self.numberOfMFLabel.setText(_translate("MainWindow", "Number of MF:"))
        self.setTabText(self.indexOf(self.mfPropertiesTab), _translate("MainWindow", "mfPropertiesTab"))
        self.ruleNameLabel.setText(_translate("MainWindow", "Name"))
        self.ruleWeightEdit.setText(_translate("MainWindow", "1"))
        self.ruleWeightLabel.setText(_translate("MainWindow", "Weight"))
        self.ruleNameEdit.setText(_translate("MainWindow", "Placeholder"))
        self.ruleEditorLabel.setText(_translate("MainWindow", "Rule Editor"))
        self.ifLabel.setText(_translate("MainWindow", "If"))
        self.thenLabel.setText(_translate("MainWindow", "Then"))
        self.firstInputRuleLabel.setText(_translate("MainWindow", "Rule 1"))
        self.firstInputIsIsntDropdown.setText(_translate("MainWindow", "is/isn\'t"))
        self.firstInputMFDropdown.setText(_translate("MainWindow", "MF"))
        self.andOrLabel.setText(_translate("MainWindow", "and/or"))
        self.finalInputMFDropdown.setText(_translate("MainWindow", "MF"))
        self.finalInputIsIsntDropdown.setText(_translate("MainWindow", "is/isn\'t"))
        self.finalInputRuleLabel.setText(_translate("MainWindow", "Rule 2"))
        self.connectionLabel.setText(_translate("MainWindow", "Connection"))
        self.andRadioButton.setText(_translate("MainWindow", "And"))
        self.orRadioButton.setText(_translate("MainWindow", "Or"))
        self.outputRuleLabel.setText(_translate("MainWindow", "Rule 1"))
        self.outputIsIsntDropdown.setText(_translate("MainWindow", "is/isn\'t"))
        self.outputMFDropdown.setText(_translate("MainWindow", "MF"))
        self.setTabText(self.indexOf(self.ruleEditorTab), _translate("MainWindow", "rulePropertiesTab"))

    def get_mf_name(self) -> str:
        return self.mfNameEdit.text()

    def set_number_of_mf(self, count: int):
        self.numberOfMFLabel.setText(f"Number of MF: {count}")
