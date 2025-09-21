"""Create a widget GUI element responsible for customising the parameters of a membership function
(range, shape, name) as well as adding and deleting functions from inputs and outputs.
    Classes:
        MFPropertiesWidget: a widget inheriting from QWidget responsible for allowing the user to
            edit membership functions inside the system.
"""
from PyQt6 import QtCore, QtGui, QtWidgets


class MFPropertiesWidget(QtWidgets.QWidget):
    """Class inheriting from QWidget.
    Allows user interaction via QPushButton, QLineEdit and QComboBox GUI elements.
    The current membership functions in the system are displayed within the table.

        Methods:
           __init__(parent): create an instance of TopMenu and bind it to the parent window.

        Attributes:
               add_mf_clicked: pyqtSignal which gets emitted to backend when add_mf_button is clicked.
               default_parameters: default parameters of a new function.
    """
    add_mf_clicked = QtCore.pyqtSignal()
    default_parameters = "[0, 0.5, 1]"

    def __init__(self, parent=None):
        """Initialize a new class instance.

            Parameters:
                parent: The parent widget, in this case main window, to which the widget will be attached.
        """
        super().__init__(parent)
        self.setObjectName("mf_properties_tab")
        self._setup_ui()
        self._retranslate_ui()

    def _setup_ui(self):
        """Set up all the GUI sub elements."""
        self.editor_frame = QtWidgets.QFrame(parent=self)
        self.editor_frame.setGeometry(QtCore.QRect(-10, 0, 291, 641))
        self.editor_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.editor_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.editor_frame.setObjectName("editor_frame")

        self.property_editor_label = QtWidgets.QLabel(parent=self.editor_frame)
        self.property_editor_label.setGeometry(QtCore.QRect(10, 0, 121, 31))
        self.property_editor_label.setObjectName("property_editor_label")

        self.mf_name_label = QtWidgets.QLabel(parent=self.editor_frame)
        self.mf_name_label.setGeometry(QtCore.QRect(20, 50, 55, 16))
        self.mf_name_label.setObjectName("mf_name_label")

        self.mf_range_label = QtWidgets.QLabel(parent=self.editor_frame)
        self.mf_range_label.setGeometry(QtCore.QRect(20, 100, 55, 16))
        self.mf_range_label.setObjectName("mf_range_label")

        self.mf_name_edit = QtWidgets.QLineEdit(parent=self.editor_frame)
        self.mf_name_edit.setGeometry(QtCore.QRect(110, 40, 161, 31))
        self.mf_name_edit.setObjectName("mf_name_edit")

        self.mf_range_edit = QtWidgets.QLineEdit(parent=self.editor_frame)
        self.mf_range_edit.setGeometry(QtCore.QRect(110, 90, 161, 31))
        self.mf_range_edit.setObjectName("mf_range_edit")
        self.mf_range_edit.setText(self.default_parameters)

        self.mf_table = QtWidgets.QTableWidget(parent=self.editor_frame)
        self.mf_table.setGeometry(QtCore.QRect(10, 230, 281, 421))
        self.mf_table.setObjectName("mf_table")

        self.mf_table.setRowCount(1)
        self.mf_table.setColumnCount(3)
        self.mf_table.setColumnWidth(0, 80)
        self.mf_table.setColumnWidth(1, 80)
        self.mf_table.setColumnWidth(2, 100)

        self.shape_select_dropdown = QtWidgets.QComboBox(parent=self.mf_table)
        self.shape_select_dropdown.addItems(['Triangle'])
        self.shape_select_dropdown.setObjectName("shape_select_dropdown")

        self.mf_table.setHorizontalHeaderLabels(["Name", "Type", "Parameters"])

        self.mf_table.setItem(0, 0, QtWidgets.QTableWidgetItem("Placeholder"))
        self.mf_table.setCellWidget(0, 1, self.shape_select_dropdown)
        self.mf_table.setItem(0, 2, QtWidgets.QTableWidgetItem(self.mf_range_edit.text()))

        self.add_mf_button = QtWidgets.QPushButton(parent=self.editor_frame)
        self.add_mf_button.setGeometry(QtCore.QRect(60, 190, 93, 28))
        self.add_mf_button.setObjectName("add_mf_button")
        self.add_mf_button.clicked.connect(self._add_mf)

        self.number_of_mf_label = QtWidgets.QLabel(parent=self.editor_frame)
        self.number_of_mf_label.setGeometry(QtCore.QRect(20, 150, 151, 16))
        self.number_of_mf_label.setObjectName("number_of_mf_label")

        self._retranslate_ui()

    def _retranslate_ui(self):
        """Add text to all the respective GUI elements."""
        _translate = QtCore.QCoreApplication.translate
        self.property_editor_label.setText(_translate("MainWindow", "Property Editor"))
        self.mf_name_label.setText(_translate("MainWindow", "Name"))
        self.mf_range_label.setText(_translate("MainWindow", "Range"))
        self.mf_name_edit.setText(_translate("MainWindow", "Placeholder"))
        self.mf_range_edit.setText(_translate("MainWindow", self.default_parameters))
        self.add_mf_button.setText(_translate("MainWindow", "Add MF"))
        self.number_of_mf_label.setText(_translate("MainWindow", "Number of MF:"))

    def get_mf_name(self) -> str:
        """Get the current name of the membership function via the line edit"""
        return self.mf_name_edit.text()

    def _set_number_of_mf(self, count: int):
        """Update the label text to reflect current mf count"""
        self.number_of_mf_label.setText(f"Number of MF: {count}")

    def _add_mf(self):
        """Add a new row to the table and fill it with new membership function with default parameters.
        Emit the signal to the back end."""
        rows = self.mf_table.rowCount()
        shape_select_dropdown = QtWidgets.QComboBox(parent=self.mf_table)
        shape_select_dropdown.addItems(['Triangle'])
        shape_select_dropdown.setObjectName("shape_select_dropdown")
        self.mf_table.setRowCount(rows+1)
        self.mf_table.setItem(rows, 0, QtWidgets.QTableWidgetItem("Placeholder"))
        self.mf_table.setCellWidget(rows, 1, shape_select_dropdown)
        self.mf_table.setItem(rows, 2, QtWidgets.QTableWidgetItem(self.default_parameters))
        self.add_mf_clicked.emit()

