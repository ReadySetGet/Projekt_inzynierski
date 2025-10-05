import pytest
from PyQt6 import QtWidgets, QtCore
from app.views.browser_frame_view import BrowserFrameWidget


@pytest.fixture
def app():
    if QtWidgets.QApplication.instance() is None:
        return QtWidgets.QApplication([])
    return QtWidgets.QApplication.instance()


@pytest.fixture
def tested_widget(qtbot, app):
    widget = BrowserFrameWidget()
    qtbot.addWidget(widget)
    return widget


def test_widget_initial_state(tested_widget):
    assert tested_widget.design_browser_label.text() == "DESIGN BROWSER"
    assert tested_widget.system_browser_label.text() == "SYSTEM BROWSER"

    assert isinstance(tested_widget, QtWidgets.QFrame)

    browser_tree_view = tested_widget.findChild(QtWidgets.QTreeView, "system_browser_tree_view")
    assert isinstance(browser_tree_view, QtWidgets.QTreeView)

    tree = browser_tree_view.findChild(QtWidgets.QTreeWidget, "tree")
    assert isinstance(tree, QtWidgets.QTreeWidget)

    rules = tree.topLevelItem(0)
    assert isinstance(rules, QtWidgets.QTreeWidgetItem)
    assert rules.text(0) == "Inputs"

    outputs = tree.topLevelItem(1)
    assert isinstance(outputs, QtWidgets.QTreeWidgetItem)
    assert outputs.text(0) == "Outputs"

    rules = tree.topLevelItem(2)
    assert isinstance(rules, QtWidgets.QTreeWidgetItem)
    assert rules.text(0) == "Rules"


def test_item_select_signal(qtbot, tested_widget):
    inputs_select = tested_widget.tree.topLevelItem(0)

    assert not inputs_select.isSelected()

    item_pos = tested_widget.tree.visualItemRect(inputs_select)
    click_pos = item_pos.center()

    with qtbot.waitSignal(tested_widget.selected_item):
        qtbot.mouseClick(tested_widget.tree.viewport(), QtCore.Qt.MouseButton.LeftButton, pos=click_pos)

    assert inputs_select.isSelected()


def test_expand(qtbot, tested_widget):
    inputs_select = tested_widget.tree.topLevelItem(0)
    assert not inputs_select.isExpanded()

    item_pos = tested_widget.tree.visualItemRect(inputs_select)
    click_pos = item_pos.bottomLeft() - QtCore.QPoint(10, int(item_pos.height() / 2))

    qtbot.mouseClick(tested_widget.tree.viewport(), QtCore.Qt.MouseButton.LeftButton, pos=click_pos)

    assert inputs_select.isExpanded()


def test_expand_then_select(qtbot, tested_widget):
    inputs_select = tested_widget.tree.topLevelItem(0)
    assert not inputs_select.isSelected()
    assert not inputs_select.isExpanded()

    item_pos = tested_widget.tree.visualItemRect(inputs_select)
    click_pos = item_pos.bottomLeft() - QtCore.QPoint(10, int(item_pos.height() / 2))

    qtbot.mouseClick(tested_widget.tree.viewport(), QtCore.Qt.MouseButton.LeftButton, pos=click_pos)

    assert inputs_select.isExpanded()
    assert not inputs_select.isSelected()

    test_input = inputs_select.child(0)

    assert not test_input.isSelected()
    assert not test_input.isExpanded()

    item_pos = tested_widget.tree.visualItemRect(test_input)
    click_pos = item_pos.bottomLeft() - QtCore.QPoint(10, int(item_pos.height() / 2))

    qtbot.mouseClick(tested_widget.tree.viewport(), QtCore.Qt.MouseButton.LeftButton, pos=click_pos)

    assert test_input.isExpanded()
    assert not test_input.isSelected()

    click_pos = item_pos.center()

    with qtbot.waitSignal(tested_widget.selected_item):
        qtbot.mouseClick(tested_widget.tree.viewport(), QtCore.Qt.MouseButton.LeftButton, pos=click_pos)

    assert test_input.isExpanded()
    assert test_input.isSelected()
