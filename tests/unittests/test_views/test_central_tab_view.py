import numpy as np
import pyqtgraph as pg
import pytest
from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt

from app.views.bell_plot import BellPlot
from app.views.central_tab_view import CentralTabWidget
from app.views.gauss_plot import GaussPlot
from app.views.trapezoid_plot import TrapezoidPlot
from app.views.triangle_plot import TrianglePlot


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
    assert tested_widget.system_label_2.text() == "System: Placeholder Name"


def test_tabs_structure(tested_widget):
    assert tested_widget.count() == 4
    assert tested_widget.tabText(0) == "FIS Plot"
    assert tested_widget.tabText(1) == "MF Editor"
    assert tested_widget.tabText(2) == "Rule Editor"
    assert tested_widget.tabText(3) == "Rule Interference"
    assert tested_widget.widget(0).objectName() == "fis_plot"
    assert tested_widget.widget(1).objectName() == "mf_plot"
    assert tested_widget.widget(2).objectName() == "rule_editor"
    assert tested_widget.widget(3).objectName() == "rule_interference"


def test_fis_plot_widgets(tested_widget):
    fis_tab = tested_widget.findChild(QtWidgets.QWidget, "fis_plot")
    assert isinstance(fis_tab, QtWidgets.QWidget)


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

    plot = mf_tab.findChild(pg.PlotWidget, "plot")
    assert isinstance(plot, pg.PlotWidget)


def test_editor_tab(tested_widget):
    editor_tab = tested_widget.findChild(QtWidgets.QWidget, "rule_editor")
    assert isinstance(editor_tab, QtWidgets.QWidget)

    seperator_line = editor_tab.findChild(QtWidgets.QFrame, "seperator_line_2")
    assert isinstance(seperator_line, QtWidgets.QFrame)

    system_label = editor_tab.findChild(QtWidgets.QLabel, "system_label_2")
    assert isinstance(system_label, QtWidgets.QLabel)
    assert system_label.text() == "System: Placeholder Name"


def test_add_triangle(tested_widget):
    plot_numb = len(tested_widget.plots)
    x = [-100, 1.0, 10, 100, 200]
    y = [0.0, 0, 1, 0, 0]
    tested_widget.add_triangle_plot(x, y, "r")
    assert len(tested_widget.plots) == plot_numb + 1


def test_add_trapezoid(tested_widget):
    plot_numb = len(tested_widget.plots)
    x = [-100.0, 10, 25, 75, 90, 200]
    y = [0.0, 0, 1, 1, 0, 0]
    tested_widget.add_trapezoid_plot(x, y, "r")
    assert len(tested_widget.plots) == plot_numb + 1


def test_add_gauss(tested_widget):
    plot_numb = len(tested_widget.plots)
    mu = 50
    sigma = 16.67
    gauss_x = np.linspace(-100, 200, 400)
    gauss_y = np.exp(-(1 / 2) * ((gauss_x - mu) / sigma) ** 2)
    tested_widget.add_gauss_plot(gauss_x, gauss_y, sigma, mu, "r")
    assert len(tested_widget.plots) == plot_numb + 1


def test_add_bell(tested_widget):
    plot_numb = len(tested_widget.plots)
    a = 20.0
    b = 2.0
    c = 50.0
    bell_x = np.linspace(-100, 200, 200)
    bell_y = 1 / (1 + np.abs((bell_x - c) / a) ** (2 * b))
    tested_widget.add_bell_plot(bell_x, bell_y, a, b, c, "r")
    assert len(tested_widget.plots) == plot_numb + 1
