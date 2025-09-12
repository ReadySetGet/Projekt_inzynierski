from PyQt6 import QtCore, QtGui, QtWidgets
from app.views.area_plot_view import AreaPlot


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
        self.w = None
        self._setup_ui()
        self._retranslate_ui()

    def _setup_ui(self):
        self.designTab = QtWidgets.QWidget()
        self.designTab.setObjectName("designTab")

        self.input_output_button_area = QtWidgets.QScrollArea(parent=self.designTab)
        self.input_output_button_area.setGeometry(QtCore.QRect(270, 0, 221, 131))
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

        self.help_button = QtWidgets.QPushButton(parent=self.designTab)
        self.help_button.setGeometry(QtCore.QRect(950, 20, 93, 28))
        self.help_button.setObjectName("help_button")
        self.help_button.clicked.connect(self.help_clicked.emit)

        self.settings_button = QtWidgets.QPushButton(parent=self.designTab)
        self.settings_button.setGeometry(QtCore.QRect(950, 70, 93, 28))
        self.settings_button.setObjectName("settings_button")
        self.settings_button.clicked.connect(self.settings_clicked.emit)

        self.conversion_button = QtWidgets.QPushButton(parent=self.designTab)
        self.conversion_button.setGeometry(QtCore.QRect(530, 30, 131, 61))
        self.conversion_button.setObjectName("conversion_button")
        self.conversion_button.clicked.connect(self.conversion_clicked.emit)

        self.files_management_button_area = QtWidgets.QScrollArea(parent=self.designTab)
        self.files_management_button_area.setGeometry(QtCore.QRect(0, 0, 271, 131))
        self.files_management_button_area.setWidgetResizable(True)
        self.files_management_button_area.setObjectName("files_management_button_area")

        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 269, 129))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")

        self.new_button = QtWidgets.QToolButton(parent=self.scrollAreaWidgetContents)
        self.new_button.setGeometry(QtCore.QRect(10, 40, 81, 41))
        self.new_button.setObjectName("new_button")
        self.new_button.clicked.connect(self.new_clicked.emit)

        self.import_button = QtWidgets.QToolButton(parent=self.scrollAreaWidgetContents)
        self.import_button.setGeometry(QtCore.QRect(100, 40, 71, 41))
        self.import_button.setObjectName("import_button")
        self.import_button.clicked.connect(self.import_clicked.emit)

        self.export_button = QtWidgets.QToolButton(parent=self.scrollAreaWidgetContents)
        self.export_button.setGeometry(QtCore.QRect(180, 41, 81, 41))
        self.export_button.setObjectName("export_button")
        self.export_button.clicked.connect(self.export_clicked.emit)

        self.files_management_button_area.setWidget(self.scrollAreaWidgetContents)

        self.files_management_button_area_2 = QtWidgets.QScrollArea(parent=self.designTab)
        self.files_management_button_area_2.setGeometry(QtCore.QRect(670, 0, 201, 131))
        self.files_management_button_area_2.setWidgetResizable(True)
        self.files_management_button_area_2.setObjectName("files_management_button_area_2")

        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 199, 129))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")

        self.interference_button = QtWidgets.QToolButton(parent=self.scrollAreaWidgetContents_2)
        self.interference_button.setGeometry(QtCore.QRect(10, 40, 81, 61))
        self.interference_button.setObjectName("interference_button")

        self.surface_button = QtWidgets.QToolButton(parent=self.scrollAreaWidgetContents_2)
        self.surface_button.setGeometry(QtCore.QRect(110, 40, 81, 61))
        self.surface_button.setObjectName("surface_button")
        self.surface_button.clicked.connect(self._show_area_plot_window)

        self.files_management_button_area_2.setWidget(self.scrollAreaWidgetContents_2)

        self.addTab(self.designTab, "")
        self.tuningTab = QtWidgets.QWidget()
        self.tuningTab.setObjectName("tuningTab")
        self.addTab(self.tuningTab, "")

    def _retranslate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        self.add_input_button.setText(_translate("MainWindow", "Add Input"))
        self.delete_input_button.setText(_translate("MainWindow", "Delete Input"))
        self.add_output_button.setText(_translate("MainWindow", "Add Output"))
        self.delete_output_button.setText(_translate("MainWindow", "Delete Output"))
        self.setTabText(self.indexOf(self.designTab), _translate("MainWindow", "Design"))
        self.setTabText(self.indexOf(self.tuningTab), _translate("MainWindow", "Tuning"))
        self.help_button.setText(_translate("MainWindow", "Help"))
        self.settings_button.setText(_translate("MainWindow", "Settings"))
        if self.system_type == 'Mamdani':
            self.conversion_button.setText(_translate("MainWindow", "Mamdani to Sugeno"))
        elif self.system_type == 'Sugeno':
            self.conversion_button.setText(_translate("MainWindow", "Sugeno to Mamdani"))
        else:
            self.conversion_button.setText(_translate("MainWindow", "Error"))
        self.new_button.setText(_translate("MainWindow", "New"))
        self.import_button.setText(_translate("MainWindow", "Import"))
        self.export_button.setText(_translate("MainWindow", "Export"))
        self.interference_button.setText(_translate("MainWindow", "Rule \n"
                                                                  "Interference"))
        self.surface_button.setText(_translate("MainWindow", "Control\n"
                                                             "Surface"))

    def _show_area_plot_window(self):
        if self.w is None:
            self.w = AreaPlot()
        self.w.show()
