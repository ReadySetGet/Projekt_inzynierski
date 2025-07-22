from PyQt6 import QtCore, QtGui, QtWidgets


class CentralTabWidget(QtWidgets.QTabWidget):
    addRuleClicked = QtCore.pyqtSignal()
    deleteRuleClicked = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("centralTab")
        self._setup_ui()

    def _setup_ui(self):
        self.fisPlot = QtWidgets.QWidget()
        self.fisPlot.setObjectName("fisPlot")

        self.graphFrame = QtWidgets.QFrame(parent=self.fisPlot)
        self.graphFrame.setGeometry(QtCore.QRect(-1, 49, 461, 471))
        self.graphFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.graphFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.graphFrame.setObjectName("graphFrame")
        self.addTab(self.fisPlot, "")

        self.mfPlot = QtWidgets.QWidget()
        self.mfPlot.setObjectName("mfPlot")

        self.plotFrame = QtWidgets.QFrame(parent=self.mfPlot)
        self.plotFrame.setGeometry(QtCore.QRect(0, 60, 531, 551))
        self.plotFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.plotFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.plotFrame.setObjectName("plotFrame")

        self.seperatorLine = QtWidgets.QFrame(parent=self.mfPlot)
        self.seperatorLine.setGeometry(QtCore.QRect(0, 20, 501, 31))
        self.seperatorLine.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.seperatorLine.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.seperatorLine.setObjectName("seperatorLine")

        self.systemNameLabel = QtWidgets.QLabel(parent=self.mfPlot)
        self.systemNameLabel.setGeometry(QtCore.QRect(0, 10, 211, 16))
        self.systemNameLabel.setObjectName("systemNameLabel")
        self.addTab(self.mfPlot, "")

        self.ruleEditor = QtWidgets.QWidget()
        self.ruleEditor.setObjectName("ruleEditor")

        self.tableWidget = QtWidgets.QTableWidget(parent=self.ruleEditor)
        self.tableWidget.setGeometry(QtCore.QRect(20, 100, 431, 491))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)

        self.addRuleButton = QtWidgets.QPushButton(parent=self.ruleEditor)
        self.addRuleButton.setGeometry(QtCore.QRect(460, 100, 41, 28))
        self.addRuleButton.setObjectName("addRuleButton")
        self.addRuleButton.clicked.connect(self.addRuleClicked.emit)

        self.deleteRuleButton = QtWidgets.QPushButton(parent=self.ruleEditor)
        self.deleteRuleButton.setGeometry(QtCore.QRect(460, 140, 41, 28))
        self.deleteRuleButton.setObjectName("deleteRuleButton")
        self.deleteRuleButton.clicked.connect(self.deleteRuleClicked.emit)

        self.seperatorLine_2 = QtWidgets.QFrame(parent=self.ruleEditor)
        self.seperatorLine_2.setGeometry(QtCore.QRect(0, 20, 501, 31))
        self.seperatorLine_2.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.seperatorLine_2.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.seperatorLine_2.setObjectName("seperatorLine_2")

        self.systemLabel_2 = QtWidgets.QLabel(parent=self.ruleEditor)
        self.systemLabel_2.setGeometry(QtCore.QRect(0, 10, 211, 16))
        self.systemLabel_2.setObjectName("systemLabel_2")

        self.addTab(self.ruleEditor, "")

        self._retranslate_ui()

    def _retranslate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWhatsThis(_translate("MainWindow", "<html><head/><body><p><br/></p><p><br/></p></body></html>"))
        self.setTabText(self.indexOf(self.fisPlot), _translate("MainWindow", "FIS Plot"))
        self.systemNameLabel.setText(_translate("MainWindow", "System: Placeholder Name"))
        self.setTabText(self.indexOf(self.mfPlot), _translate("MainWindow", "MF Editor"))
        self.addRuleButton.setText(_translate("MainWindow", "+"))
        self.deleteRuleButton.setText(_translate("MainWindow", "X"))
        self.systemLabel_2.setText(_translate("MainWindow", "System: Placeholder Name"))
        self.setTabText(self.indexOf(self.ruleEditor), _translate("MainWindow", "Rule Editor"))
