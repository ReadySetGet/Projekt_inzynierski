import pytest
from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt
from app.views.top_menu_view import TopMenu


@pytest.fixture
def app():
    if QtWidgets.QApplication.instance() is None:
        return QtWidgets.QApplication([])
    return QtWidgets.QApplication.instance()


@pytest.fixture
def tested_widget(qtbot, app):
    widget = TopMenu()
    qtbot.addWidget(widget)
    return widget


def test_widget_initial_state(tested_widget):
    assert isinstance(tested_widget, QtWidgets.QTabWidget)
    assert tested_widget.new_button.text() == "New"


def test_tabs_structure(tested_widget):
    assert tested_widget.count() == 2
    assert tested_widget.tabText(0) == "Design"
    assert tested_widget.tabText(1) == "Tuning"
    assert tested_widget.widget(0).objectName() == "designTab"
    assert tested_widget.widget(1).objectName() == "tuningTab"


def test_new_signal_emit(qtbot, tested_widget):
    with qtbot.waitSignal(tested_widget.new_clicked, timeout=1000):
        qtbot.mouseClick(tested_widget.new_button, Qt.MouseButton.LeftButton)