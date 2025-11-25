import pytest
from PyQt6 import QtWidgets

from app.views.mf_editor_tab import MFPropertiesWidget


@pytest.fixture
def app():
    if QtWidgets.QApplication.instance() is None:
        return QtWidgets.QApplication([])
    return QtWidgets.QApplication.instance()


@pytest.fixture
def tested_widget(qtbot, app):
    widget = MFPropertiesWidget()
    qtbot.addWidget(widget)
    return widget


def test_initial_state(tested_widget):
    assert tested_widget.property_editor_label.text() == "Property Editor"

    assert tested_widget.mf_name_label.text() == "Name"

    assert tested_widget.mf_range_label.text() == "Range"

    assert tested_widget.mf_name_edit.text() == "Placeholder"

    assert tested_widget.mf_range_edit.text() == tested_widget.default_parameters

    assert tested_widget.mf_table.rowCount() == 1
    assert tested_widget.mf_table.columnCount() == 3
    assert tested_widget.mf_table.horizontalHeaderItem(0).text() == "Name"
    assert tested_widget.mf_table.horizontalHeaderItem(1).text() == "Type"
    assert tested_widget.mf_table.horizontalHeaderItem(2).text() == "Parameters"
    assert tested_widget.mf_table.item(0, 0).text() == "Placeholder"
    assert tested_widget.mf_table.item(0, 2).text() == tested_widget.default_parameters

    assert tested_widget.shape_select_dropdown.itemText(0) == "Triangle"
    assert tested_widget.shape_select_dropdown.itemText(1) == "Trapezoid"
    assert tested_widget.shape_select_dropdown.itemText(2) == "Gauss"
    assert tested_widget.shape_select_dropdown.itemText(3) == "Bell"

    assert tested_widget.number_of_mf_label.text() == "Number of MF:"


def test_object_names(tested_widget):
    assert tested_widget.editor_frame.objectName() == "editor_frame"
    assert tested_widget.property_editor_label.objectName() == "property_editor_label"
    assert tested_widget.mf_name_label.objectName() == "mf_name_label"
    assert tested_widget.mf_range_label.objectName() == "mf_range_label"
    assert tested_widget.mf_name_edit.objectName() == "mf_name_edit"
    assert tested_widget.mf_table.objectName() == "mf_table"
    assert tested_widget.shape_select_dropdown.objectName() == "shape_select_dropdown"
    assert tested_widget.number_of_mf_label.objectName() == "number_of_mf_label"


def test_types(tested_widget):
    assert isinstance(tested_widget, QtWidgets.QWidget)
    assert isinstance(tested_widget.editor_frame, QtWidgets.QFrame)
    assert isinstance(tested_widget.property_editor_label, QtWidgets.QLabel)
    assert isinstance(tested_widget.mf_name_label, QtWidgets.QLabel)
    assert isinstance(tested_widget.mf_range_label, QtWidgets.QLabel)
    assert isinstance(tested_widget.mf_name_edit, QtWidgets.QLineEdit)
    assert isinstance(tested_widget.mf_range_edit, QtWidgets.QLineEdit)
    assert isinstance(tested_widget.mf_table, QtWidgets.QTableWidget)
    assert isinstance(tested_widget.shape_select_dropdown, QtWidgets.QComboBox)
    assert isinstance(tested_widget.number_of_mf_label, QtWidgets.QLabel)


def test_shape_select_dropdown(tested_widget):
    shape_select = tested_widget.findChild(QtWidgets.QComboBox, "shape_select_dropdown")

    assert shape_select.currentIndex() == 0
    assert shape_select.currentText() == "Triangle"

    shape_select.setCurrentIndex(1)

    assert shape_select.currentIndex() == 1
    assert shape_select.currentText() == "Trapezoid"

    shape_select.setCurrentIndex(2)

    assert shape_select.currentIndex() == 2
    assert shape_select.currentText() == "Gauss"

    shape_select.setCurrentIndex(3)

    assert shape_select.currentIndex() == 3
    assert shape_select.currentText() == "Bell"

    shape_select.setCurrentIndex(0)

    assert shape_select.currentIndex() == 0
    assert shape_select.currentText() == "Triangle"


def test_change_name(tested_widget):
    tested_widget.mf_table.selectRow(0)
    new_name = "Test Name"
    tested_widget.mf_name_edit.setText(new_name)

    assert tested_widget.mf_table.item(0, 0).text() == new_name
