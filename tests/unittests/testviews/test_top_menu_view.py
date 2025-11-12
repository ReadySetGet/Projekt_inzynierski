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
    assert tested_widget.import_button.text() == "Import"
    assert tested_widget.export_button.text() == "Export"


def test_tabs_structure(tested_widget):
    assert tested_widget.count() == 2
    assert tested_widget.tabText(0) == "Design"
    assert tested_widget.tabText(1) == "Tuning"
    assert tested_widget.widget(0).objectName() == "designTab"
    assert tested_widget.widget(1).objectName() == "tuningTab"


def test_buttons_exist(tested_widget):
    assert tested_widget.findChild(QtWidgets.QToolButton, "new_button") is tested_widget.new_button
    assert tested_widget.findChild(QtWidgets.QToolButton, "import_button") is tested_widget.import_button
    assert tested_widget.findChild(QtWidgets.QToolButton, "export_button") is tested_widget.export_button


def test_import_clicked_emit(qtbot, tested_widget):
    with qtbot.waitSignal(tested_widget.import_clicked, timeout=1000):
        qtbot.mouseClick(tested_widget.import_button, Qt.MouseButton.LeftButton)


def test_export_clicked_emit(qtbot, tested_widget):
    with qtbot.waitSignal(tested_widget.export_clicked, timeout=1000):
        qtbot.mouseClick(tested_widget.export_button, Qt.MouseButton.LeftButton)
