"""Create a button area element GUI object above the central window of the application.

    Classes:
        TopMenu: button area element inheriting from QTabWidget.
"""
from PyQt6 import QtCore, QtGui, QtWidgets


class TopMenu(QtWidgets.QTabWidget):
    """Class inheriting from QTabWidget.
        Allows user interaction via QPushButton and QToolButton GUI elements .

        Methods:
            __init__(parent): create an instance of TopMenu and bind it to the parent window.

        Attributes:

            add_output_clicked: pyqtSignal which gets emitted to back end when add_output_button is clicked.
            delete_output_clicked: pyqtSignal which gets emitted to back end when delete_output_button is clicked.
            add_input_clicked: pyqtSignal which gets emitted to back end when add_input_button is clicked.
            delete_input_clicked: pyqtSignal which gets emitted to back end when delete_input_button is clicked.
    """

    add_output_clicked = QtCore.pyqtSignal()
    delete_output_clicked = QtCore.pyqtSignal()

    add_input_clicked = QtCore.pyqtSignal()
    delete_input_clicked = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        """Initialize a new class instance.

            Parameters:
                parent: The parent widget, in this case main window, to which the widget will be attached.
        """
        super().__init__(parent)
        self.setObjectName("topMenu")
        self._setup_ui()
        self._retranslate_ui()

    def _setup_ui(self):
        """Set up all the GUI sub elements."""
        self.designTab = QtWidgets.QWidget()
        self.designTab.setObjectName("designTab")

        self.input_output_button_area = QtWidgets.QScrollArea(parent=self.designTab)
        self.input_output_button_area.setGeometry(QtCore.QRect(270, 0, 221, 131))
        self.input_output_button_area.setWidgetResizable(True)
        self.input_output_button_area.setObjectName("input_output_button_area")

        self.scroll_area_widget_contents_3 = QtWidgets.QWidget()
        self.scroll_area_widget_contents_3.setGeometry(QtCore.QRect(0, 0, 219, 129))
        self.scroll_area_widget_contents_3.setObjectName("scroll_area_widget_contents_3")


        self.add_output_button = QtWidgets.QPushButton(parent=self.scroll_area_widget_contents_3)
        self.add_output_button.setGeometry(QtCore.QRect(10, 70, 91, 41))
        self.add_output_button.setObjectName("add_output_button")
        self.add_output_button.clicked.connect(self._add_output_button_clicked)

        self.delete_output_button = QtWidgets.QPushButton(parent=self.scroll_area_widget_contents_3)
        self.delete_output_button.setGeometry(QtCore.QRect(110, 70, 91, 41))
        self.delete_output_button.setObjectName("delete_output_button")
        self.delete_output_button.clicked.connect(self._del_output_button_clicked)

        self.add_input_button = QtWidgets.QPushButton(parent=self.scroll_area_widget_contents_3)
        self.add_input_button.setGeometry(QtCore.QRect(10, 10, 91, 41))
        self.add_input_button.setObjectName("add_input_button")
        self.add_input_button.clicked.connect(self._add_input_button_clicked)

        self.delete_input_button = QtWidgets.QPushButton(parent=self.scroll_area_widget_contents_3)
        self.delete_input_button.setGeometry(QtCore.QRect(110, 10, 91, 41))
        self.delete_input_button.setObjectName("delete_input_button")
        self.delete_input_button.clicked.connect(self._del_input_button_clicked)


        self.input_output_button_area.setWidget(self.scroll_area_widget_contents_3)

        self.addTab(self.designTab, "")
        self.tuningTab = QtWidgets.QWidget()
        self.tuningTab.setObjectName("tuningTab")
        self.addTab(self.tuningTab, "")

    def _retranslate_ui(self):
        """Add text to all the respective GUI elements."""
        _translate = QtCore.QCoreApplication.translate
        self.add_output_button.setText(_translate("MainWindow", "Add Output"))
        self.delete_output_button.setText(_translate("MainWindow", "Delete Output"))
        self.setTabText(self.indexOf(self.designTab), _translate("MainWindow", "Design"))
        self.setTabText(self.indexOf(self.tuningTab), _translate("MainWindow", "Tuning"))
        self.add_input_button.setText(_translate("MainWindow", "Add Input"))
        self.delete_input_button.setText(_translate("MainWindow", "Delete Input"))

    def _add_output_button_clicked(self):
        """Emit a signal that new output is supposed to get added."""
        self.add_output_clicked.emit()

    def _del_output_button_clicked(self):
        """Emit a signal that an existing output is supposed to get deleted."""
        self.delete_output_clicked.emit()

    def _add_input_button_clicked(self):
        """Emit a signal that new input is supposed to get added."""
        self.add_input_clicked.emit()

    def _del_input_button_clicked(self):
        """Emit a signal that an existing input is supposed to get deleted."""
        self.delete_input_clicked.emit()

