import numpy as np
import pytest
from PyQt6 import QtWidgets
import pyqtgraph as pg
from app.views.bell_plot import BellPlot


@pytest.fixture
def main_window_with_plot(qtbot):
    main_window = QtWidgets.QMainWindow()
    plot_widget = pg.PlotWidget()
    main_window.setCentralWidget(plot_widget)
    qtbot.addWidget(main_window)
    return main_window


@pytest.fixture
def bell_plot_instance(main_window_with_plot):
    plot_widget = main_window_with_plot.centralWidget()
    x_data = np.linspace(0, 100, 100)
    y_data = np.zeros(100)
    a = 15.0
    b = 2.0
    c = 50.0
    color = '#00ff00'
    return BellPlot(plot_widget, x_data, y_data, a, b, c, color)


def test_initialization(bell_plot_instance):
    assert isinstance(bell_plot_instance, BellPlot)
    assert isinstance(bell_plot_instance.bell_plot_line, pg.PlotDataItem)
    assert isinstance(bell_plot_instance.left_a_anchor, pg.TargetItem)
    assert isinstance(bell_plot_instance.right_a_anchor, pg.TargetItem)
    assert isinstance(bell_plot_instance.left_b_anchor, pg.TargetItem)
    assert isinstance(bell_plot_instance.right_b_anchor, pg.TargetItem)


def test_initial_anchor_positions(bell_plot_instance):
    a, b, c = bell_plot_instance.a, bell_plot_instance.b, bell_plot_instance.c
    b_height = bell_plot_instance.b_height

    assert bell_plot_instance.left_a_anchor.pos().x() == pytest.approx(c - a)
    assert bell_plot_instance.left_a_anchor.pos().y() == pytest.approx(0.5)
    assert bell_plot_instance.right_a_anchor.pos().x() == pytest.approx(c + a)
    assert bell_plot_instance.right_a_anchor.pos().y() == pytest.approx(0.5)

    expected_b_x = c + a * 0.25 ** (1 / (2 * b))
    assert bell_plot_instance.right_b_anchor.pos().x() == pytest.approx(expected_b_x)
    assert bell_plot_instance.right_b_anchor.pos().y() == pytest.approx(b_height)


def test_left_a_interaction_valid(bell_plot_instance, qtbot):
    initial_a = bell_plot_instance.a
    new_pos = (bell_plot_instance.c - 20, 0.5)

    bell_plot_instance.left_a_anchor.setPos(*new_pos)
    bell_plot_instance.left_a_anchor.sigPositionChanged.emit(bell_plot_instance.left_a_anchor)

    assert bell_plot_instance.a == 20.0


def test_left_a_interaction_invalid(bell_plot_instance, qtbot):
    initial_a = bell_plot_instance.a
    new_pos = (-5, 0.5)

    bell_plot_instance.left_a_anchor.setPos(*new_pos)
    bell_plot_instance.left_a_anchor.sigPositionChanged.emit(bell_plot_instance.left_a_anchor)

    assert bell_plot_instance.a == initial_a


def test_right_a_interaction_valid(bell_plot_instance, qtbot):
    initial_a = bell_plot_instance.a
    new_pos = (bell_plot_instance.c + 20, 0.5)

    bell_plot_instance.right_a_anchor.setPos(*new_pos)
    bell_plot_instance.right_a_anchor.sigPositionChanged.emit(bell_plot_instance.left_a_anchor)

    assert bell_plot_instance.a == 20.0


def test_right_a_interaction_invalid(bell_plot_instance, qtbot):
    initial_a = bell_plot_instance.a
    new_pos = (200, 0.5)

    bell_plot_instance.left_a_anchor.setPos(*new_pos)
    bell_plot_instance.left_a_anchor.sigPositionChanged.emit(bell_plot_instance.left_a_anchor)

    assert bell_plot_instance.a == initial_a


def test_update_b_interaction(bell_plot_instance, qtbot):
    new_pos = (60, bell_plot_instance.b_height)

    bell_plot_instance.right_b_anchor.setPos(*new_pos)
    bell_plot_instance.right_b_anchor.sigPositionChanged.emit(bell_plot_instance.right_b_anchor)

    expected_b = np.log(1 / bell_plot_instance.b_height - 1) / (
            2 * np.log(abs((new_pos[0] - bell_plot_instance.c) / bell_plot_instance.a)))
    assert bell_plot_instance.b == pytest.approx(expected_b)

    expected_left_b_x = bell_plot_instance.c - bell_plot_instance.a * 0.25 ** (1 / (2 * expected_b))
    assert bell_plot_instance.left_b_anchor.pos().x() == pytest.approx(expected_left_b_x)
