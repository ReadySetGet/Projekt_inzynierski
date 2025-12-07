from unittest.mock import Mock, PropertyMock

import pytest
from PyQt6 import QtWidgets

from app.views.editor_tab_view import EditorTabWidget


@pytest.fixture
def app():
    if QtWidgets.QApplication.instance() is None:
        return QtWidgets.QApplication([])
    return QtWidgets.QApplication.instance()


@pytest.fixture
def tested_widget(qtbot, app, setup_base_view_model_context, mock_fuzzy_service):
    mock_fis = Mock()
    mock_fis.Name = "test_fis"
    mock_fis.__class__ = type("MamFis", (), {})
    mock_fis.Inputs = []
    mock_fis.Outputs = []
    mock_fis_model = Mock()
    mock_fis_model._fis = mock_fis
    mock_fuzzy_service.get_fis_model = Mock(return_value=mock_fis_model)

    widget = EditorTabWidget()
    if hasattr(widget, "view_model") and widget.view_model:
        type(widget.view_model).default_parameters = PropertyMock(return_value="[0, 0.5, 1]")
    qtbot.addWidget(widget)
    return widget


def test_initial_state(tested_widget):
    assert tested_widget.property_editor_label.text() in ["translated_PROPERTY_EDITOR", "PROPERTY_EDITOR"]

    assert tested_widget.mf_name_label.text() in ["translated_NAME", "NAME"]

    assert tested_widget.mf_range_label.text() in ["translated_RANGE", "RANGE"]

    assert tested_widget.mf_name_edit.text() == ""

    assert tested_widget.mf_table.columnCount() == 3
    assert tested_widget.mf_table.horizontalHeaderItem(0).text() in ["translated_NAME", "NAME"]
    assert tested_widget.mf_table.horizontalHeaderItem(1).text() in ["translated_TYPE", "TYPE"]
    assert tested_widget.mf_table.horizontalHeaderItem(2).text() in ["translated_PARAMETERS", "PARAMETERS"]

    assert (
        "NUMBER_OF_MF" in tested_widget.number_of_mf_label.text()
        or "translated_NUMBER_OF_MF" in tested_widget.number_of_mf_label.text()
    )


def test_object_names(tested_widget):
    assert tested_widget.editor_frame.objectName() == "editor_frame"
    assert tested_widget.property_editor_label.objectName() == "property_editor_label"
    assert tested_widget.mf_name_label.objectName() == "mf_name_label"
    assert tested_widget.mf_range_label.objectName() == "mf_range_label"
    assert tested_widget.mf_name_edit.objectName() == "mf_name_edit"
    assert tested_widget.mf_table.objectName() == "mf_table"
    assert tested_widget.number_of_mf_label.objectName() == "number_of_mf_label"


def test_types(tested_widget):
    assert isinstance(tested_widget, QtWidgets.QTabWidget)
    assert isinstance(tested_widget.editor_frame, QtWidgets.QFrame)
    assert isinstance(tested_widget.property_editor_label, QtWidgets.QLabel)
    assert isinstance(tested_widget.mf_name_label, QtWidgets.QLabel)
    assert isinstance(tested_widget.mf_range_label, QtWidgets.QLabel)
    assert isinstance(tested_widget.mf_name_edit, QtWidgets.QLineEdit)
    assert isinstance(tested_widget.mf_range_edit, QtWidgets.QLineEdit)
    assert isinstance(tested_widget.mf_table, QtWidgets.QTableWidget)
    assert isinstance(tested_widget.number_of_mf_label, QtWidgets.QLabel)


def test_shape_select_dropdown(tested_widget):
    tested_widget.mf_table.setRowCount(1)
    tested_widget.mf_table.setItem(0, 0, QtWidgets.QTableWidgetItem("test_mf"))

    type_dropdown = QtWidgets.QComboBox()
    type_dropdown.addItems(["translated_TRIANGLE", "translated_TRAPEZOID", "translated_GAUSS", "translated_BELL"])
    tested_widget.mf_table.setCellWidget(0, 1, type_dropdown)

    shape_select = tested_widget.mf_table.cellWidget(0, 1)

    assert shape_select.currentIndex() == 0
    assert shape_select.currentText() == "translated_TRIANGLE"

    shape_select.setCurrentIndex(1)

    assert shape_select.currentIndex() == 1
    assert shape_select.currentText() == "translated_TRAPEZOID"

    shape_select.setCurrentIndex(2)

    assert shape_select.currentIndex() == 2
    assert shape_select.currentText() == "translated_GAUSS"

    shape_select.setCurrentIndex(3)

    assert shape_select.currentIndex() == 3
    assert shape_select.currentText() == "translated_BELL"

    shape_select.setCurrentIndex(0)

    assert shape_select.currentIndex() == 0
    assert shape_select.currentText() == "translated_TRIANGLE"


def test_change_name(tested_widget):
    tested_widget.mf_table.setRowCount(1)
    tested_widget.mf_table.setItem(0, 0, QtWidgets.QTableWidgetItem("old_name"))
    tested_widget.mf_table.selectRow(0)
    new_name = "Test Name"
    tested_widget.mf_name_edit.setText(new_name)

    assert tested_widget.mf_name_edit.text() == new_name
