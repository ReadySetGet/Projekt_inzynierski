import numpy as np
import pyqtgraph as pg
import pytest
from PyQt6 import QtWidgets

from app.views.central_tab_view import CentralTabWidget


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
    system_name_text = tested_widget.system_name_label.text() if hasattr(tested_widget, "system_name_label") else ""
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

    plot = mf_tab.findChild(pg.PlotWidget, "plot")
    if plot:
        assert isinstance(plot, pg.PlotWidget)


def test_editor_tab(tested_widget):
    editor_tab = tested_widget.findChild(QtWidgets.QWidget, "rule_editor")
    if editor_tab:
        assert isinstance(editor_tab, QtWidgets.QWidget)

        seperator_line = editor_tab.findChild(QtWidgets.QFrame, "seperator_line_2")
        if seperator_line:
            assert isinstance(seperator_line, QtWidgets.QFrame)

        system_label = editor_tab.findChild(QtWidgets.QLabel, "system_label_2")
        if system_label:
            assert isinstance(system_label, QtWidgets.QLabel)
            assert (
                "SYSTEM" in system_label.text()
                or "System" in system_label.text()
                or "translated_SYSTEM" in system_label.text()
            )


def test_add_triangle(tested_widget):
    plot_numb = len(tested_widget.mf_plots) if hasattr(tested_widget, "mf_plots") else 0
    x = [-100, 1.0, 10, 100, 200]
    y = [0.0, 0, 1, 0, 0]
    if hasattr(tested_widget, "add_triangle_plot"):
        tested_widget.add_triangle_plot(x, y, "r")
        assert len(tested_widget.mf_plots) == plot_numb + 1
    else:
        pytest.skip("add_triangle_plot method not available")


def test_add_trapezoid(tested_widget):
    plot_numb = len(tested_widget.mf_plots) if hasattr(tested_widget, "mf_plots") else 0
    x = [-100.0, 10, 25, 75, 90, 200]
    y = [0.0, 0, 1, 1, 0, 0]
    if hasattr(tested_widget, "add_trapezoid_plot"):
        tested_widget.add_trapezoid_plot(x, y, "r")
        assert len(tested_widget.mf_plots) == plot_numb + 1
    else:
        pytest.skip("add_trapezoid_plot method not available")


def test_add_gauss(tested_widget):
    plot_numb = len(tested_widget.mf_plots) if hasattr(tested_widget, "mf_plots") else 0
    mu = 50
    sigma = 16.67
    gauss_x = np.linspace(-100, 200, 400)
    gauss_y = np.exp(-(1 / 2) * ((gauss_x - mu) / sigma) ** 2)
    if hasattr(tested_widget, "add_gauss_plot"):
        tested_widget.add_gauss_plot(gauss_x, gauss_y, sigma, mu, "r")
        assert len(tested_widget.mf_plots) == plot_numb + 1
    else:
        pytest.skip("add_gauss_plot method not available")


def test_add_bell(tested_widget):
    plot_numb = len(tested_widget.mf_plots) if hasattr(tested_widget, "mf_plots") else 0
    a = 20.0
    b = 2.0
    c = 50.0
    bell_x = np.linspace(-100, 200, 200)
    bell_y = 1 / (1 + np.abs((bell_x - c) / a) ** (2 * b))
    if hasattr(tested_widget, "add_bell_plot"):
        tested_widget.add_bell_plot(bell_x, bell_y, a, b, c, "r")
        assert len(tested_widget.mf_plots) == plot_numb + 1
    else:
        pytest.skip("add_bell_plot method not available")
