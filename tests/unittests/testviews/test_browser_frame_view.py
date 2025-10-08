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

    clear_in = tested_widget.findChild(QtWidgets.QPushButton,"del_inputs_button")
    assert isinstance(clear_in, QtWidgets.QPushButton)
    assert clear_in.text() == "Clear Inputs"

    clear_out = tested_widget.findChild(QtWidgets.QPushButton, "del_outputs_button")
    assert isinstance(clear_out, QtWidgets.QPushButton)
    assert clear_out.text() == "Clear Outputs"


def test_clear_inputs_signal(qtbot, tested_widget):
    with qtbot.waitSignal(tested_widget.del_inputs, timeout=1000, raising=True):
        qtbot.mouseClick(tested_widget.delete_all_inputs_button, QtCore.Qt.MouseButton.LeftButton)


def test_clear_outputs_signal(qtbot, tested_widget):
    with qtbot.waitSignal(tested_widget.del_outputs, timeout=1000, raising=True):
        qtbot.mouseClick(tested_widget.delete_all_outputs_button, QtCore.Qt.MouseButton.LeftButton)

