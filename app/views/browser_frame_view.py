"""Create the browser GUI window at the left of the application.

    Classes:
        BrowserFrameWidget: left window of the application displaying all the present inputs, outputs and rules in the
            system as well as their hierarchy. Inherits from QFrame.
"""
from PyQt6 import QtCore, QtGui, QtWidgets

class BrowserFrameWidget(QtWidgets.QFrame):
    """Class inheriting from QFrame.
        Displays the information about the fis system via hierarchical QTreeView widget. Allows user interaction
        via QTreeWidgetItems elements.

            Methods:
                __init__(QtWidget.*): create an instance of BrowserFrameWidget and bind it to the parent widget.
                clour_inputs(): remove all inputs from the system browser tree widget, emit a signal to the backend.
                clear_outputs(): remove all outputs from the system browser tree widget, emit a signal to the backend.

            Attributes:
                del_inputs: pyqtSignal which gets emitted to the backend whenever the user presses delete_all_inputs
                    button
                del_outputs: pyqtSignal which gets emitted to the backend whenever the user presses delete_all_outputs
                    button
                placeholder attributes for testing purposes
    """
    del_inputs = QtCore.pyqtSignal()
    del_outputs = QtCore.pyqtSignal()
    def __init__(self, parent=None):
        """Initialize a new class instance.

            Parameters:
                parent: The parent QtWidget, in this case centralwidget, to which the widget will be attached.
        """
        super().__init__(parent)
        self.setObjectName("browserFrame")
        self._setup_ui()
        self._retranslate_ui()

    def _setup_ui(self):
        """Set up all the GUI sub elements."""
        self.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)

        self.delete_all_inputs_button = QtWidgets.QPushButton(parent=self)
        self.delete_all_inputs_button.setGeometry(QtCore.QRect(10, 246, 140, 28))
        self.delete_all_inputs_button.setObjectName("del_inputs_button")
        self.delete_all_inputs_button.clicked.connect(self.clear_inputs)

        self.delete_all_outputs_button = QtWidgets.QPushButton(parent=self)
        self.delete_all_outputs_button.setGeometry(QtCore.QRect(155, 246, 140, 28))
        self.delete_all_outputs_button.setObjectName("del_outputs_button")
        self.delete_all_outputs_button.clicked.connect(self.clear_outputs)

        self.system_browser_label = QtWidgets.QLabel(parent=self)
        self.system_browser_label.setGeometry(QtCore.QRect(4, 274, 281, 21))
        self.system_browser_label.setObjectName("system_browser_label")

        self.design_browser_label = QtWidgets.QLabel(parent=self)
        self.design_browser_label.setGeometry(QtCore.QRect(10, 10, 111, 16))
        self.design_browser_label.setObjectName("design_browser_label")

    def _retranslate_ui(self):
        """Add text to all the respective GUI elements."""
        _translate = QtCore.QCoreApplication.translate
        self.system_browser_label.setText(_translate("MainWindow", "SYSTEM BROWSER"))
        self.design_browser_label.setText(_translate("MainWindow", "DESIGN BROWSER"))
        self.delete_all_inputs_button.setText(_translate("MainWindow", "Clear Inputs"))
        self.delete_all_outputs_button.setText(_translate("MainWindow", "Clear Outputs"))

    def clear_inputs(self) -> None:
        """
        Remove all the inputs and their children from the system browsers tree widget. Send a signal to the backend.
        :return: None
        """
        #for i in range(self.tree_data_input.childCount()):
        #    self.tree_data_input.removeChild(self.tree_data_input.child(0))
        self.del_inputs.emit()

    def clear_outputs(self) -> None:
        """
        Remove all the outputs and their children from the system browsers tree widget. Send a signal to the backend.
        :return: None
        """
        #for i in range(self.tree_data_output.childCount()):
        #    self.tree_data_output.removeChild(self.tree_data_output.child(0))
        self.del_outputs.emit()
