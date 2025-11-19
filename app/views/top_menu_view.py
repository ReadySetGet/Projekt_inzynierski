"""Create a button area element GUI object above the central window of the application.

    Classes:
        TopMenu: button area element inheriting from QTabWidget.
"""
from PyQt6 import QtCore, QtGui, QtWidgets


class TopMenu(QtWidgets.QTabWidget):
    """Class inheriting from QTabWidget.
        Allows user interaction via QPushButton and QToolButton GUI elements .

        Methods:
            __init__(QtWidgets.*): create an instance of TopMenu and bind it to the parent widget.

        Attributes:
            spinbox_changed: pyqtSignal which gets emitted to backend whenever the amount of interpolation
            points is changed.
    """
    spinbox_changed = QtCore.pyqtSignal()

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

        self.interpolation_spinbox = QtWidgets.QSpinBox(parent=self.designTab)
        self.interpolation_spinbox.setGeometry(QtCore.QRect(830, 60, 81, 22))
        self.interpolation_spinbox.setObjectName("interpolation_spinbox")
        self.interpolation_spinbox.setValue(15)
        self.interpolation_spinbox.valueChanged.connect(self._interpolation_value_changed)

        self.interpolation_label = QtWidgets.QLabel(parent=self.designTab)
        self.interpolation_label.setGeometry(QtCore.QRect(810, 30, 121, 20))
        self.interpolation_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.interpolation_label.setObjectName("interpolation_label")

        self.addTab(self.designTab, "")

        self.tuningTab = QtWidgets.QWidget()
        self.tuningTab.setObjectName("tuningTab")
        self.addTab(self.tuningTab, "")

    def _retranslate_ui(self):
        """Add text to all the respective GUI elements."""
        _translate = QtCore.QCoreApplication.translate
        self.setTabText(self.indexOf(self.designTab), _translate("MainWindow", "Design"))
        self.setTabText(self.indexOf(self.tuningTab), _translate("MainWindow", "Tuning"))
        self.interpolation_label.setText(_translate("MainWindow", "Interpolation Points"))

    def _interpolation_value_changed(self):
        """Emit a signal to the back end that new amount of interpolation points has been set."""
        self.spinbox_changed.emit()
