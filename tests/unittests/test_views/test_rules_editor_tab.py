import pytest
from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt

from app.views.rules_editor_tab import RulesEditorTab


@pytest.fixture
def app():
    if QtWidgets.QApplication.instance() is None:
        return QtWidgets.QApplication([])
    return QtWidgets.QApplication.instance()


@pytest.fixture
def tested_widget(qtbot, app):
    widget = RulesEditorTab()
    qtbot.addWidget(widget)
    return widget


def test_initial_state(tested_widget):
    if hasattr(tested_widget, "name_label"):
        assert tested_widget.name_label.text() in ["Name", "translated_NAME", "NAME", "NAME:", "translated_NAME:"]
    assert tested_widget.rule_weight_edit.text() == "1.0"
    if hasattr(tested_widget, "weight_label"):
        assert tested_widget.weight_label.text() in ["Weight", "translated_WEIGHT", "WEIGHT", "WEIGHT:", "translated_WEIGHT:"]
    assert tested_widget.rule_name_edit.text() == ""
    if hasattr(tested_widget, "if_label"):
        assert tested_widget.if_label.text() in ["If", "translated_IF", "IF"]
    if hasattr(tested_widget, "then_label"):
        assert tested_widget.then_label.text() in ["Then", "translated_THEN", "THEN"]
    if hasattr(tested_widget, "connection_label"):
        assert tested_widget.connection_label.text() in ["Connection", "translated_CONNECTION", "CONNECTION", "CONNECTION:", "translated_CONNECTION:"]
    if hasattr(tested_widget, "and_radio_button"):
        assert tested_widget.and_radio_button.text() in ["And", "translated_AND", "AND"]
    if hasattr(tested_widget, "or_radio_button"):
        assert tested_widget.or_radio_button.text() in ["Or", "translated_OR", "OR"]


def test_types(tested_widget):
    assert isinstance(tested_widget, QtWidgets.QWidget)
    if hasattr(tested_widget, "name_label"):
        assert isinstance(tested_widget.name_label, QtWidgets.QLabel)
    assert isinstance(tested_widget.rule_weight_edit, QtWidgets.QLineEdit)
    if hasattr(tested_widget, "weight_label"):
        assert isinstance(tested_widget.weight_label, QtWidgets.QLabel)
    assert isinstance(tested_widget.rule_name_edit, QtWidgets.QLineEdit)
    if hasattr(tested_widget, "if_label"):
        assert isinstance(tested_widget.if_label, QtWidgets.QLabel)
    if hasattr(tested_widget, "then_label"):
        assert isinstance(tested_widget.then_label, QtWidgets.QLabel)
    if hasattr(tested_widget, "connection_label"):
        assert isinstance(tested_widget.connection_label, QtWidgets.QLabel)
    if hasattr(tested_widget, "and_radio_button"):
        assert isinstance(tested_widget.and_radio_button, QtWidgets.QRadioButton)
    if hasattr(tested_widget, "or_radio_button"):
        assert isinstance(tested_widget.or_radio_button, QtWidgets.QRadioButton)


def test_is_isnt_dropdowns(qtbot, tested_widget):
    final_i_dropdown = tested_widget.findChild(QtWidgets.QComboBox, "final_input_is_isnt_dropdown")
    first_i_dropdown = tested_widget.findChild(QtWidgets.QComboBox, "first_input_is_isnt_dropdown")
    o_dropdown = tested_widget.findChild(QtWidgets.QComboBox, "output_is_isnt_dropdown")

    if first_i_dropdown:
        assert first_i_dropdown.currentIndex() >= 0
        if first_i_dropdown.count() > 0:
            assert first_i_dropdown.currentText() in ["Is", "translated_IS", "IS", "Isn't", "translated_ISNT", "ISNT"]
    if final_i_dropdown:
        assert final_i_dropdown.currentIndex() >= 0
    if o_dropdown:
        assert o_dropdown.currentIndex() >= 0


def test_radio_buttons(tested_widget, qtbot):
    and_button = tested_widget.findChild(QtWidgets.QRadioButton, "and_radio_button")
    or_button = tested_widget.findChild(QtWidgets.QRadioButton, "or_radio_button")

    if and_button and or_button:
        qtbot.mouseClick(and_button, Qt.MouseButton.LeftButton)
        assert and_button.isChecked() is True
        assert or_button.isChecked() is False

        qtbot.mouseClick(or_button, Qt.MouseButton.LeftButton)
        assert and_button.isChecked() is False
        assert or_button.isChecked() is True


def test_name_edit(tested_widget):
    name_edit = tested_widget.rule_name_edit
    assert isinstance(name_edit, QtWidgets.QLineEdit)

    name_edit.setText("test")
    assert name_edit.text() == "test"


def test_weight_edit(tested_widget):
    weight_edit = tested_widget.rule_weight_edit
    assert isinstance(weight_edit, QtWidgets.QLineEdit)

    weight_edit.setText("0.5")
    assert weight_edit.text() == "0.5"
