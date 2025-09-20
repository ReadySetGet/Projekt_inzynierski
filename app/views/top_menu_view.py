from PyQt6 import QtCore, QtGui, QtWidgets


class TopMenu(QtWidgets.QTabWidget):
    add_input_clicked = QtCore.pyqtSignal()
    delete_input_clicked = QtCore.pyqtSignal()
    add_output_clicked = QtCore.pyqtSignal()
    delete_output_clicked = QtCore.pyqtSignal()
    help_clicked = QtCore.pyqtSignal()
    settings_clicked = QtCore.pyqtSignal()
    conversion_clicked = QtCore.pyqtSignal()
    new_clicked = QtCore.pyqtSignal()
    import_clicked = QtCore.pyqtSignal()
    export_clicked = QtCore.pyqtSignal()

    system_type = 'Mamdani'

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("topMenu")
        self._setup_ui()
        self._retranslate_ui()

    def _setup_ui(self):
        self.designTab = QtWidgets.QWidget()
        self.designTab.setObjectName("designTab")

        self.addTab(self.designTab, "")
        self.tuningTab = QtWidgets.QWidget()
        self.tuningTab.setObjectName("tuningTab")
        self.addTab(self.tuningTab, "")

    def _retranslate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        self.setTabText(self.indexOf(self.designTab), _translate("MainWindow", "Design"))
        self.setTabText(self.indexOf(self.tuningTab), _translate("MainWindow", "Tuning"))