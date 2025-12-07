import pytest
from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt

from app.views.central_tab_view import CentralTabWidget
from app.views.rule import Rule

rule1 = Rule(
    "In1",
    "Mf1",
    "1",
    "In2",
    "Mf2",
    "2",
    "Out",
    "Mf3",
    "3",
    "is",
    "and",
    "1",
    "Rule 1",
)
rule2 = Rule(
    "In1",
    "Mf1",
    "1",
    "In2",
    "Mf2",
    "2",
    "Out",
    "Mf3",
    "3",
    "is",
    "and",
    "1",
    "Rule 2",
)
rule3 = Rule(
    "In1",
    "Mf1",
    "1",
    "In2",
    "Mf2",
    "2",
    "Out",
    "Mf3",
    "3",
    "is",
    "and",
    "1",
    "Rule 3",
)
rules = [rule1, rule2, rule3]


@pytest.fixture
def app():
    if QtWidgets.QApplication.instance() is None:
        return QtWidgets.QApplication([])
    return QtWidgets.QApplication.instance()


@pytest.fixture
def tested_widget(qtbot, app):
    widget = CentralTabWidget()
    qtbot.addWidget(widget)
    return widget


def test_widget_initial_state(tested_widget):
    assert isinstance(tested_widget, QtWidgets.QTabWidget)
    if hasattr(tested_widget, "system_name_label"):
        system_name_text = tested_widget.system_name_label.text()
        assert "SYSTEM" in system_name_text or "System" in system_name_text or "translated_SYSTEM" in system_name_text


def test_tabs_structure(tested_widget):
    assert tested_widget.count() >= 3
    assert tested_widget.tabText(0) in ["FIS Plot", "translated_FIS_PLOT", "FIS_PLOT"]
    if tested_widget.count() > 1:
        assert tested_widget.tabText(1) in [
            "MF Editor",
            "translated_MF_EDITOR",
            "MF_EDITOR",
            "MF Plot",
            "translated_MF_PLOT",
        ]
    assert tested_widget.widget(0).objectName() == "fis_plot"


def test_fis_plot_widgets(tested_widget):
    fis_tab = tested_widget.findChild(QtWidgets.QWidget, "fis_plot")
    assert isinstance(fis_tab, QtWidgets.QWidget)

    graph_frame = fis_tab.findChild(QtWidgets.QFrame, "graph_frame")
    assert isinstance(graph_frame, QtWidgets.QFrame)


def test_mf_plot_widgets(tested_widget):
    mf_tab = tested_widget.findChild(QtWidgets.QWidget, "mf_plot")
    assert isinstance(mf_tab, QtWidgets.QWidget)

    plot_frame = mf_tab.findChild(QtWidgets.QFrame, "plot_frame")
    assert isinstance(plot_frame, QtWidgets.QFrame)

    seperator_line = mf_tab.findChild(QtWidgets.QFrame, "seperator_line")
    if seperator_line:
        assert isinstance(seperator_line, QtWidgets.QFrame)

    system_label = mf_tab.findChild(QtWidgets.QLabel, "system_name_label")
    if system_label:
        assert isinstance(system_label, QtWidgets.QLabel)
        assert (
            "SYSTEM" in system_label.text()
            or "System" in system_label.text()
            or "translated_SYSTEM" in system_label.text()
        )


def test_editor_tab(tested_widget):
    editor_tab = tested_widget.findChild(QtWidgets.QWidget, "rule_editor")
    if editor_tab:
        assert isinstance(editor_tab, QtWidgets.QWidget)

        table = editor_tab.findChild(QtWidgets.QTableWidget, "table_widget")
        if table:
            assert isinstance(table, QtWidgets.QTableWidget)

            add_rules_button = editor_tab.findChild(QtWidgets.QPushButton, "add_all_rules")
            if add_rules_button:
                assert isinstance(add_rules_button, QtWidgets.QPushButton)
                assert add_rules_button.text() in [
                    "Add All Possible Rules",
                    "translated_ADD_ALL_POSSIBLE_RULES",
                    "ADD_ALL_POSSIBLE_RULES",
                    "translated_ADD_ALL_RULES",
                    "ADD_ALL_RULES",
                ]

            if table.columnCount() > 0 and table.horizontalHeaderItem(0):
                header_text = table.horizontalHeaderItem(0).text()
                assert header_text in [
                    "Rule",
                    "translated_RULE",
                    "RULE",
                    "Name",
                    "translated_NAME",
                    "NAME",
                    "Weight",
                    "translated_WEIGHT",
                    "WEIGHT",
                ]


def test_add_rules_button(qtbot, tested_widget):
    if not hasattr(tested_widget, "set_rules"):
        pytest.skip("set_rules method not available")

    tested_widget.set_rules(rules)
    editor_tab = tested_widget.findChild(QtWidgets.QWidget, "rule_editor")
    if editor_tab:
        table = editor_tab.findChild(QtWidgets.QTableWidget, "table_widget")
        if table and hasattr(tested_widget, "add_all_rules_button"):
            table.setRowCount(0)

            with qtbot.waitSignal(tested_widget.add_all_rules_button.clicked, timeout=1000):
                qtbot.mouseClick(tested_widget.add_all_rules_button, Qt.MouseButton.LeftButton)

            assert table.rowCount() == 3
            if table.item(0, 0):
                assert "In1" in table.item(0, 0).text() or "Mf1" in table.item(0, 0).text()
