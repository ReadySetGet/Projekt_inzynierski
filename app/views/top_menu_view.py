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
            conversion_clicked: pyqtSignal which gets emitted to back end when conversion_button is clicked.
            system_type: stores data about current fis system type.
    """
    conversion_clicked = QtCore.pyqtSignal()

    system_type = 'Mamdani'

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

        self.conversion_button = QtWidgets.QPushButton(parent=self.designTab)
        self.conversion_button.setGeometry(QtCore.QRect(530, 30, 131, 61))
        self.conversion_button.setObjectName("conversion_button")
        self.conversion_button.clicked.connect(self._conversion_button_clicked)

        self.addTab(self.designTab, "")
        self.tuningTab = QtWidgets.QWidget()
        self.tuningTab.setObjectName("tuningTab")
        self.addTab(self.tuningTab, "")

    def _retranslate_ui(self):
        """Add text to all the respective GUI elements."""
        _translate = QtCore.QCoreApplication.translate
        if self.system_type == 'Mamdani':
            self.conversion_button.setText(_translate("MainWindow", "Mamdani to Sugeno"))
        elif self.system_type == 'Sugeno':
            self.conversion_button.setText(_translate("MainWindow", "Sugeno to Mamdani"))
        else:
            self.conversion_button.setText(_translate("MainWindow", "Error"))
        self.setTabText(self.indexOf(self.designTab), _translate("MainWindow", "Design"))
        self.setTabText(self.indexOf(self.tuningTab), _translate("MainWindow", "Tuning"))

    def _conversion_button_clicked(self):
        """Converts system from mamdani to sugeno and vice versa.
        Updates the text on the button to indicate the change.
        Emits a signal to the backend to convert the system.
        """
        if self.system_type == "Mamdani":
            self.system_type = "Sugeno"
            self.conversion_button.setText("Sugeno to Mamdani")
        else:
            self.system_type = "Mamdani"
            self.conversion_button.setText("Mamdani to Sugeno")
        self.conversion_clicked.emit()
