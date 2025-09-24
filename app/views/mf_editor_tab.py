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
             __init__(QTWidget.*): create an instance of MFPropertiesWidget and bind it to the parent QTWidget
             or None if the widget is standalone.
             get_mf_name(): get the name of the mf from the line edit.

          Attributes:
                 shape_changed: pyqtSignal which gets emitted to backend when shape_select_dropdown selected
                    item is changed.
                 name_changed: pyqtSignal which gets emitted to backend when mf_name_edit value is changed.
                 default_parameters: default parameters of a new function.
      """
    shape_changed = QtCore.pyqtSignal()
    name_changed = QtCore.pyqtSignal()
    default_parameters = "[0, 0.5, 1]"

    def __init__(self, parent=None):
        """Initialize a new class instance.

            Parameters:
                parent: The parent widget, in this case editor tab, to which the widget will be attached.
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
        self.mf_name_edit.textChanged.connect(self._set_name_table_text)

        self.mf_range_edit = QtWidgets.QLineEdit(parent=self.editor_frame)
        self.mf_range_edit.setGeometry(QtCore.QRect(110, 90, 70, 31))
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
        self.shape_select_dropdown.addItems(['Gauss', 'Trapezoid', 'Triangle', 'Bell'])
        self.shape_select_dropdown.setObjectName("shape_select_dropdown")
        self.shape_select_dropdown.currentIndexChanged.connect(self._shape_changed)

        self.mf_table.setHorizontalHeaderLabels(["Name", "Type", "Parameters"])

        self.mf_table.setItem(0, 0, QtWidgets.QTableWidgetItem("Placeholder"))
        self.mf_table.setCellWidget(0, 1, self.shape_select_dropdown)
        self.mf_table.setItem(0, 2, QtWidgets.QTableWidgetItem(self.mf_range_edit.text()))

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
        self.mf_range_submit_button.setText(_translate("MainWindow", "Submit"))
        self.mf_range_edit.setText(_translate("MainWindow", self.default_parameters))
        self.number_of_mf_label.setText(_translate("MainWindow", "Number of MF:"))

    def get_mf_name(self) -> str:
        """Get the current name of the membership function via the line edit"""
        return self.mf_name_edit.text()

    def _set_number_of_mf(self, count: int):
        """Update the label text to reflect current mf count"""
        self.number_of_mf_label.setText(f"Number of MF: {count}")

    def _shape_changed(self) -> None:
        """Emit a signal that the selected item in dropdown was changed."""
        self.shape_changed.emit()

    def _set_name_table_text(self) -> None:
        """Update the name of the selected mf in the table. Emit a signal to backend."""
        selected_row = self.mf_table.currentRow()
        if selected_row == -1 or len(self.mf_name_edit.text()) > 100:
            return
        label = self.mf_table.item(selected_row, 0)
        label.setText(self.mf_name_edit.text())
        self.mf_table.setItem(selected_row, 0, label)
        self.name_changed.emit()
