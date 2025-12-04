import numpy as np
import pyqtgraph as pg
import pytest
from PyQt6 import QtWidgets

from app.views.gauss_plot import GaussPlot


@pytest.fixture
def main_window_with_plot(qtbot):
    main_window = QtWidgets.QMainWindow()
    plot_widget = pg.PlotWidget()
    main_window.setCentralWidget(plot_widget)
    qtbot.addWidget(main_window)
    return main_window


@pytest.fixture
def plot_instance(main_window_with_plot):
    plot_widget = main_window_with_plot.centralWidget()
    x_data = np.linspace(0, 100, 100)
    y_data = np.exp(-(1 / 2) * ((x_data - 50) / 10) ** 2)
    sigma = 10.0
    mu = 50.0
    color = "#ff0000"
    return GaussPlot(plot_widget, x_data, y_data, sigma, mu, color)


def test_initialization(plot_instance):
    assert isinstance(plot_instance, GaussPlot)
    assert isinstance(plot_instance.gauss_plot_line, pg.PlotDataItem)
    assert isinstance(plot_instance.gauss_left_anchor, pg.TargetItem)
    assert isinstance(plot_instance.gauss_right_anchor, pg.TargetItem)
    assert plot_instance.sigma == 10.0
    assert plot_instance.mu == 50.0


def test_anchor_initial_positions(plot_instance):
    initial_y = np.exp(-0.5)
    assert np.isclose(plot_instance.gauss_left_anchor.pos().x(), 40)
    assert np.isclose(plot_instance.gauss_left_anchor.pos().y(), initial_y)
    assert np.isclose(plot_instance.gauss_right_anchor.pos().x(), 60)
    assert np.isclose(plot_instance.gauss_right_anchor.pos().y(), initial_y)


def test_left_anchor_interaction_valid(plot_instance, qtbot):
    new_pos = (35, np.exp(-0.5))
    plot_instance.gauss_left_anchor.setPos(*new_pos)
    plot_instance.gauss_left_anchor.sigPositionChanged.emit(plot_instance.gauss_left_anchor)

    assert np.isclose(plot_instance.sigma, 15.0)

    assert np.isclose(plot_instance.gauss_right_anchor.pos().x(), 65.0)

    expected_y = np.exp(-(1 / 2) * ((plot_instance.gauss_x - 50) / 15.0) ** 2)
    assert np.allclose(plot_instance.gauss_plot_line.getData()[1], expected_y)


def test_left_anchor_interaction_invalid(plot_instance, qtbot):
    initial_sigma = plot_instance.sigma
    new_pos = (55, np.exp(-0.5))
    plot_instance.gauss_left_anchor.setPos(*new_pos)
    plot_instance.gauss_left_anchor.sigPositionChanged.emit(plot_instance.gauss_left_anchor)

    assert np.isclose(plot_instance.sigma, initial_sigma)


def test_right_anchor_interaction_valid(plot_instance, qtbot):
    new_pos = (70, np.exp(-0.5))
    plot_instance.gauss_right_anchor.setPos(*new_pos)
    plot_instance.gauss_right_anchor.sigPositionChanged.emit(plot_instance.gauss_right_anchor)

    assert np.isclose(plot_instance.sigma, 20.0)
    assert np.isclose(plot_instance.gauss_left_anchor.pos().x(), 30.0)


def test_right_anchor_interaction_invalid(plot_instance, qtbot):
    initial_sigma = plot_instance.sigma
    new_pos = (50, np.exp(-0.5))
    plot_instance.gauss_right_anchor.setPos(*new_pos)
    plot_instance.gauss_right_anchor.sigPositionChanged.emit(plot_instance.gauss_right_anchor)

    assert np.isclose(plot_instance.sigma, initial_sigma)
