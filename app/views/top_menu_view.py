from PyQt6 import QtCore, QtGui, QtWidgets


class TopMenu(QtWidgets.QTabWidget):
    add_input_clicked = QtCore.pyqtSignal()
    delete_input_clicked = QtCore.pyqtSignal()
    add_output_clicked = QtCore.pyqtSignal()
    delete_output_clicked = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("topMenu")
        self._setup_ui()

    def _setup_ui(self):
        self.designTab = QtWidgets.QWidget()
        self.designTab.setObjectName("designTab")

        self.input_output_button_area = QtWidgets.QScrollArea(parent=self.designTab)
        self.input_output_button_area.setGeometry(QtCore.QRect(180, 0, 221, 131))
        self.input_output_button_area.setWidgetResizable(True)
        self.input_output_button_area.setObjectName("input_output_button_area")

        self.scroll_area_widget_contents_3 = QtWidgets.QWidget()
        self.scroll_area_widget_contents_3.setGeometry(QtCore.QRect(0, 0, 219, 129))
        self.scroll_area_widget_contents_3.setObjectName("scroll_area_widget_contents_3")

        self.add_input_button = QtWidgets.QPushButton(parent=self.scroll_area_widget_contents_3)
        self.add_input_button.setGeometry(QtCore.QRect(10, 10, 91, 41))
        self.add_input_button.setObjectName("add_input_button")
        self.add_input_button.clicked.connect(self.add_input_clicked.emit)

        self.delete_input_button = QtWidgets.QPushButton(parent=self.scroll_area_widget_contents_3)
        self.delete_input_button.setGeometry(QtCore.QRect(110, 10, 91, 41))
        self.delete_input_button.setObjectName("delete_input_button")
        self.delete_input_button.clicked.connect(self.delete_input_clicked.emit)

        self.add_output_button = QtWidgets.QPushButton(parent=self.scroll_area_widget_contents_3)
        self.add_output_button.setGeometry(QtCore.QRect(10, 70, 91, 41))
        self.add_output_button.setObjectName("add_output_button")
        self.add_output_button.clicked.connect(self.add_output_clicked.emit)

        self.delete_output_button = QtWidgets.QPushButton(parent=self.scroll_area_widget_contents_3)
        self.delete_output_button.setGeometry(QtCore.QRect(110, 70, 91, 41))
        self.delete_output_button.setObjectName("delete_output_button")
        self.delete_output_button.clicked.connect(self.delete_output_clicked.emit)

        self.input_output_button_area.setWidget(self.scroll_area_widget_contents_3)

        self.addTab(self.designTab, "")
        self.tuningTab = QtWidgets.QWidget()
        self.tuningTab.setObjectName("tuningTab")
        self.addTab(self.tuningTab, "")

        self._retranslate_ui()

    def _retranslate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        self.add_input_button.setText(_translate("MainWindow", "Add Input"))
        self.delete_input_button.setText(_translate("MainWindow", "Delete Input"))
        self.add_output_button.setText(_translate("MainWindow", "Add Output"))
        self.delete_output_button.setText(_translate("MainWindow", "Delete Output"))
        self.setTabText(self.indexOf(self.designTab), _translate("MainWindow", "Design"))
        self.setTabText(self.indexOf(self.tuningTab), _translate("MainWindow", "Tuning"))
