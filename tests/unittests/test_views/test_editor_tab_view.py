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
    assert tested_widget.system_name_label.text() == "System: Placeholder Name"


def test_tabs_structure(tested_widget):
    assert tested_widget.count() == 3
    assert tested_widget.tabText(0) == "FIS Plot"
    assert tested_widget.tabText(1) == "MF Editor"
    assert tested_widget.tabText(2) == "Rule Editor"
    assert tested_widget.widget(0).objectName() == "fis_plot"
    assert tested_widget.widget(1).objectName() == "mf_plot"
    assert tested_widget.widget(2).objectName() == "rule_editor"


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
    assert isinstance(seperator_line, QtWidgets.QFrame)

    system_label = mf_tab.findChild(QtWidgets.QLabel, "system_name_label")
    assert isinstance(system_label, QtWidgets.QLabel)
    assert system_label.text() == "System: Placeholder Name"


def test_editor_tab(tested_widget):
    editor_tab = tested_widget.findChild(QtWidgets.QWidget, "rule_editor")
    assert isinstance(editor_tab, QtWidgets.QWidget)

    table = editor_tab.findChild(QtWidgets.QTableWidget, "table_widget")
    assert isinstance(table, QtWidgets.QTableWidget)

    add_rules_button = editor_tab.findChild(QtWidgets.QPushButton, "add_all_rules")
    assert isinstance(add_rules_button, QtWidgets.QPushButton)
    assert add_rules_button.text() == "Add All Possible Rules"

    assert table.horizontalHeaderItem(0).text() == "Rule"
    assert table.horizontalHeaderItem(1).text() == "Weight"
    assert table.horizontalHeaderItem(2).text() == "Name"


def test_add_rules_button(qtbot, tested_widget):
    tested_widget.set_rules(rules)
    editor_tab = tested_widget.findChild(QtWidgets.QWidget, "rule_editor")
    table = editor_tab.findChild(QtWidgets.QTableWidget, "table_widget")
    table.setRowCount(0)

    with qtbot.waitSignal(tested_widget.add_all_rules_button.clicked, timeout=1000):
        qtbot.mouseClick(tested_widget.add_all_rules_button, Qt.MouseButton.LeftButton)

    assert table.rowCount() == 3
    assert table.item(0, 0).text() == "If In1 is Mf1 and In2 is Mf2 then Out is Mf3"
    assert table.item(0, 1).text() == "1"
    assert table.item(0, 2).text() == "Rule 1"
    assert table.item(1, 2).text() == "Rule 2"
    assert table.item(2, 2).text() == "Rule 3"
