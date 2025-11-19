import pytest
from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt
from app.views.editor_tab_view import EditorTabWidget


@pytest.fixture
def app():
    if QtWidgets.QApplication.instance() is None:
        return QtWidgets.QApplication([])
    return QtWidgets.QApplication.instance()


@pytest.fixture
def tested_widget(qtbot, app):
    widget = EditorTabWidget()
    qtbot.addWidget(widget)
    return widget


def test_tabs_structure(tested_widget):
    assert tested_widget.count() == 3
    assert tested_widget.tabText(0) == "fisPropertiesTab"
    assert tested_widget.tabText(1) == "mfPropertiesTab"
    assert tested_widget.tabText(2) == "rulePropertiesTab"
    assert tested_widget.widget(0).objectName() == "fis_properties_tab"
    assert tested_widget.widget(1).objectName() == "mf_properties_tab"
    assert tested_widget.widget(2).objectName() == "rule_editor_tab"


def test_fis_properties_tab_initial_state(tested_widget):
    fis_tab = tested_widget.findChild(QtWidgets.QWidget, "fis_properties_tab")
    assert isinstance(fis_tab, QtWidgets.QWidget)

    sys_type_label = fis_tab.findChild(QtWidgets.QLabel, "system_type_label_1")
    assert isinstance(sys_type_label, QtWidgets.QLabel)
    assert sys_type_label.text() == "Type:"

    sys_name_label = fis_tab.findChild(QtWidgets.QLabel, "system_name_label")
    assert sys_name_label.text() == "Name"

    and_label = fis_tab.findChild(QtWidgets.QLabel, "and_method_label")
    assert and_label.text() == "And method"

    or_label = fis_tab.findChild(QtWidgets.QLabel, "or_method_label")
    assert or_label.text() == "Or method"

    implication_label = fis_tab.findChild(QtWidgets.QLabel, "implication_method_label")
    assert implication_label.text() == "Implication method"

    aggregation_label = fis_tab.findChild(QtWidgets.QLabel, "aggregation_method_label")
    assert aggregation_label.text() == "Aggregation method"

    defuz_label = fis_tab.findChild(QtWidgets.QLabel, "defuzzification_method_label")
    assert defuz_label.text() == "Defuzzification method"

    defuz_dropdown = fis_tab.findChild(QtWidgets.QComboBox, "defuzzification_dropdown")
    assert defuz_dropdown.currentText() == "centroid"

    sys_type_label_2 = tested_widget.findChild(QtWidgets.QLabel, "system_type_label_2")
    assert sys_type_label_2.text() == "System_type"


def test_defuz_dropdown(tested_widget):
    defuz_dropdown = tested_widget.findChild(QtWidgets.QComboBox, "defuzzification_dropdown")

    assert defuz_dropdown.currentIndex() == 0
    assert defuz_dropdown.currentText() == "centroid"

    defuz_dropdown.setCurrentIndex(1)

    assert defuz_dropdown.currentIndex() == 1
    assert defuz_dropdown.currentText() == "bisector"

    defuz_dropdown.setCurrentIndex(2)

    assert defuz_dropdown.currentIndex() == 2
    assert defuz_dropdown.currentText() == "lom"

    defuz_dropdown.setCurrentIndex(0)

    assert defuz_dropdown.currentIndex() == 0
    assert defuz_dropdown.currentText() == "centroid"
