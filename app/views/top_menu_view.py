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
            new_clicked: pyqtSignal which gets emitted to back end when new_button is clicked.
    """
    new_clicked = QtCore.pyqtSignal()

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

        self.new_button.clicked.connect(self._new_button_clicked)

        self.files_management_button_area.setWidget(self.scrollAreaWidgetContents)

        self.addTab(self.designTab, "")
        self.tuningTab = QtWidgets.QWidget()
        self.tuningTab.setObjectName("tuningTab")
        self.addTab(self.tuningTab, "")

    def _retranslate_ui(self):
        """Add text to all the respective GUI elements."""
        _translate = QtCore.QCoreApplication.translate
        self.new_button.setText(_translate("MainWindow", "New"))
        self.setTabText(self.indexOf(self.designTab), _translate("MainWindow", "Design"))
        self.setTabText(self.indexOf(self.tuningTab), _translate("MainWindow", "Tuning"))

    def _new_button_clicked(self):
        """Emit a signal that new system is supposed to get created."""
        self.new_clicked.emit()
