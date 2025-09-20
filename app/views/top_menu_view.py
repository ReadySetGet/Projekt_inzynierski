from PyQt6 import QtCore, QtGui, QtWidgets


class TopMenu(QtWidgets.QTabWidget):
    import_clicked = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("topMenu")
        self._setup_ui()
        self._retranslate_ui()

    def _setup_ui(self):
        self.designTab = QtWidgets.QWidget()
        self.designTab.setObjectName("designTab")

        self.files_management_button_area = QtWidgets.QScrollArea(parent=self.designTab)
        self.files_management_button_area.setGeometry(QtCore.QRect(0, 0, 271, 131))
        self.files_management_button_area.setWidgetResizable(True)
        self.files_management_button_area.setObjectName("files_management_button_area")

        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 269, 129))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")

        self.import_button = QtWidgets.QToolButton(parent=self.scrollAreaWidgetContents)
        self.import_button.setGeometry(QtCore.QRect(100, 40, 71, 41))
        self.import_button.setObjectName("import_button")
        self.import_button.clicked.connect(self._import_button_clicked)

        self.files_management_button_area.setWidget(self.scrollAreaWidgetContents)

        self.addTab(self.designTab, "")
        self.tuningTab = QtWidgets.QWidget()
        self.tuningTab.setObjectName("tuningTab")
        self.addTab(self.tuningTab, "")

    def _retranslate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        self.import_button.setText(_translate("MainWindow", "Import"))
        self.setTabText(self.indexOf(self.designTab), _translate("MainWindow", "Design"))
        self.setTabText(self.indexOf(self.tuningTab), _translate("MainWindow", "Tuning"))

    def _import_button_clicked(self):
        self.import_clicked.emit()
