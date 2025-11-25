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
    assert tested_widget.rule_name_label.text() == "Name"
    assert tested_widget.rule_weight_edit.text() == "1"
    assert tested_widget.rule_weight_label.text() == "Weight"
    assert tested_widget.rule_name_edit.text() == "Placeholder"
    assert tested_widget.if_label.text() == "If"
    assert tested_widget.then_label.text() == "Then"
    assert tested_widget.first_input_rule_label.text() == "Rule 1"
    assert tested_widget.and_or_label.text() == "and/or"
    assert tested_widget.final_input_rule_label.text() == "Rule 2"
    assert tested_widget.connection_label.text() == "Connection"
    assert tested_widget.and_radio_button.text() == "And"
    assert tested_widget.or_radio_button.text() == "Or"
    assert tested_widget.output_rule_label.text() == "Rule 1"
    assert tested_widget.first_input_is_isnt_dropdown.currentText() == "Is"
    assert tested_widget.final_input_is_isnt_dropdown.currentText() == "Is"
    assert tested_widget.output_is_isnt_dropdown.currentText() == "Is"
    assert tested_widget.first_input_mf_dropdown.currentText() == "Placeholder Input MF"
    assert tested_widget.final_input_mf_dropdown.currentText() == "Placeholder Input MF"
    assert tested_widget.output_mf_dropdown.currentText() == "Placeholder Output MF"


def test_types(tested_widget):
    assert isinstance(tested_widget, QtWidgets.QWidget)
    assert isinstance(tested_widget.rule_name_label, QtWidgets.QLabel)
    assert isinstance(tested_widget.rule_weight_edit, QtWidgets.QLineEdit)
    assert isinstance(tested_widget.rule_weight_label, QtWidgets.QLabel)
    assert isinstance(tested_widget.rule_name_edit, QtWidgets.QLineEdit)
    assert isinstance(tested_widget.rule_editor_label, QtWidgets.QLabel)
    assert isinstance(tested_widget.if_label, QtWidgets.QWidget)
    assert isinstance(tested_widget.if_line, QtWidgets.QFrame)
    assert isinstance(tested_widget.then_line, QtWidgets.QFrame)
    assert isinstance(tested_widget.then_label, QtWidgets.QLabel)
    assert isinstance(tested_widget.first_input_rule_label, QtWidgets.QLabel)
    assert isinstance(tested_widget.first_input_mf_dropdown, QtWidgets.QComboBox)
    assert isinstance(tested_widget.first_input_is_isnt_dropdown, QtWidgets.QComboBox)
    assert isinstance(tested_widget.final_input_rule_label, QtWidgets.QLabel)
    assert isinstance(tested_widget.final_input_is_isnt_dropdown, QtWidgets.QComboBox)
    assert isinstance(tested_widget.final_input_mf_dropdown, QtWidgets.QComboBox)
    assert isinstance(tested_widget.and_or_label, QtWidgets.QLabel)
    assert isinstance(tested_widget.connection_label, QtWidgets.QLabel)
    assert isinstance(tested_widget.and_radio_button, QtWidgets.QRadioButton)
    assert isinstance(tested_widget.or_radio_button, QtWidgets.QRadioButton)
    assert isinstance(tested_widget.output_rule_label, QtWidgets.QLabel)
    assert isinstance(tested_widget.output_is_isnt_dropdown, QtWidgets.QComboBox)
    assert isinstance(tested_widget.output_mf_dropdown, QtWidgets.QComboBox)


def test_is_isnt_dropdowns(qtbot, tested_widget):
    final_i_dropdown = tested_widget.findChild(QtWidgets.QComboBox, "final_input_is_isnt_dropdown")
    first_i_dropdown = tested_widget.findChild(QtWidgets.QComboBox, "first_input_is_isnt_dropdown")
    o_dropdown = tested_widget.findChild(QtWidgets.QComboBox, "output_is_isnt_dropdown")

    assert first_i_dropdown.currentIndex() == 0
    assert first_i_dropdown.currentText() == "Is"
    with qtbot.waitSignal(tested_widget.is_dropdown_changed, raising=True, timeout=1000):
        first_i_dropdown.setCurrentIndex(1)
    assert first_i_dropdown.currentIndex() == 1
    assert first_i_dropdown.currentText() == "Isn\'t"

    assert final_i_dropdown.currentIndex() == 0
    assert final_i_dropdown.currentText() == "Is"
    with qtbot.waitSignal(tested_widget.is_dropdown_changed, raising=True, timeout=1000):
        final_i_dropdown.setCurrentIndex(1)
    assert final_i_dropdown.currentIndex() == 1
    assert final_i_dropdown.currentText() == "Isn\'t"

    assert o_dropdown.currentIndex() == 0
    assert o_dropdown.currentText() == "Is"
    with qtbot.waitSignal(tested_widget.is_dropdown_changed, raising=True, timeout=1000):
        o_dropdown.setCurrentIndex(1)
    assert o_dropdown.currentIndex() == 1
    assert o_dropdown.currentText() == "Isn\'t"


def test_radio_buttons(tested_widget, qtbot):
    and_button = tested_widget.findChild(QtWidgets.QRadioButton, "and_radio_button")
    or_button = tested_widget.findChild(QtWidgets.QRadioButton, "or_radio_button")

    with qtbot.waitSignal(tested_widget.and_or_radio_changed, raising=True, timeout=1000):
        qtbot.mouseClick(and_button, Qt.MouseButton.LeftButton)

    assert and_button.isChecked() is True
    assert or_button.isChecked() is False

    with qtbot.waitSignal(tested_widget.and_or_radio_changed, raising=True, timeout=1000):
        qtbot.mouseClick(or_button, Qt.MouseButton.LeftButton)

    assert and_button.isChecked() is False
    assert or_button.isChecked() is True


def test_name_edit(tested_widget):
    name_edit = tested_widget.findChild(QtWidgets.QLineEdit, "rule_name_edit")
    assert isinstance(name_edit, QtWidgets.QLineEdit)

    name_edit.setText("test")
    assert name_edit.text() == "test"


def test_weight_edit(tested_widget):
    weight_edit = tested_widget.findChild(QtWidgets.QLineEdit, "rule_weight_edit")
    assert isinstance(weight_edit, QtWidgets.QLineEdit)

    weight_edit.setText("0.5")
    assert weight_edit.text() == "0.5"
