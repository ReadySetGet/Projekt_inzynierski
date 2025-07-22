from PyQt6 import QtCore, QtGui, QtWidgets

class TopMenu(QtWidgets.QTabWidget):
    addInputClicked = QtCore.pyqtSignal()
    deleteInputClicked = QtCore.pyqtSignal()
    addOutputClicked = QtCore.pyqtSignal()
    deleteOutputClicked = QtCore.pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("topMenu")
        self._setup_ui()

    def _setup_ui(self):

        self.designTab = QtWidgets.QWidget()
        self.designTab.setObjectName("designTab")

        self.inputOutputButtonArea = QtWidgets.QScrollArea(parent=self.designTab)
        self.inputOutputButtonArea.setGeometry(QtCore.QRect(180, 0, 221, 131))
        self.inputOutputButtonArea.setWidgetResizable(True)
        self.inputOutputButtonArea.setObjectName("inputOutputButtonArea")

        self.scrollAreaWidgetContents_3 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_3.setGeometry(QtCore.QRect(0, 0, 219, 129))
        self.scrollAreaWidgetContents_3.setObjectName("scrollAreaWidgetContents_3")

        self.addInputButton = QtWidgets.QPushButton(parent=self.scrollAreaWidgetContents_3)
        self.addInputButton.setGeometry(QtCore.QRect(10, 10, 91, 41))
        self.addInputButton.setObjectName("addInputButton")
        self.addInputButton.clicked.connect(self.addInputClicked.emit)

        self.deleteInputButton = QtWidgets.QPushButton(parent=self.scrollAreaWidgetContents_3)
        self.deleteInputButton.setGeometry(QtCore.QRect(110, 10, 91, 41))
        self.deleteInputButton.setObjectName("deleteInputButton")
        self.deleteInputButton.clicked.connect(self.deleteInputClicked.emit)

        self.addOutputButton = QtWidgets.QPushButton(parent=self.scrollAreaWidgetContents_3)
        self.addOutputButton.setGeometry(QtCore.QRect(10, 70, 91, 41))
        self.addOutputButton.setObjectName("addOutputButton")
        self.addOutputButton.clicked.connect(self.addOutputClicked.emit)

        self.deleteOutputButton = QtWidgets.QPushButton(parent=self.scrollAreaWidgetContents_3)
        self.deleteOutputButton.setGeometry(QtCore.QRect(110, 70, 91, 41))
        self.deleteOutputButton.setObjectName("deleteOutputButton")
        self.deleteOutputButton.clicked.connect(self.deleteOutputClicked.emit)

        self.inputOutputButtonArea.setWidget(self.scrollAreaWidgetContents_3)

        self.addTab(self.designTab, "")
        self.tuningTab = QtWidgets.QWidget()
        self.tuningTab.setObjectName("tuningTab")
        self.addTab(self.tuningTab, "")

        self._retranslate_ui()

    def _retranslate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        self.addInputButton.setText(_translate("MainWindow", "Add Input"))
        self.deleteInputButton.setText(_translate("MainWindow", "Delete Input"))
        self.addOutputButton.setText(_translate("MainWindow", "Add Output"))
        self.deleteOutputButton.setText(_translate("MainWindow", "Delete Output"))
        self.setTabText(self.indexOf(self.designTab), _translate("MainWindow", "Design"))
        self.setTabText(self.indexOf(self.tuningTab), _translate("MainWindow", "Tuning"))