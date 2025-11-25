import pytest
from PyQt6 import QtWidgets
import pyqtgraph as pg
from app.views.trapezoid_plot import TrapezoidPlot


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

    x_data = [0, 10, 20, 30, 40, 50]
    y_data = [0, 0, 1, 1, 0, 0]
    color = '#ff0000'

    return TrapezoidPlot(plot_widget, x_data, y_data, color)


def test_initialization(plot_instance):
    assert isinstance(plot_instance, TrapezoidPlot)
    assert isinstance(plot_instance.trapezoid_plot_line, pg.PlotDataItem)

    assert isinstance(plot_instance.trapezoid_left_down_anchor, pg.TargetItem)
    assert isinstance(plot_instance.trapezoid_left_up_anchor, pg.TargetItem)
    assert isinstance(plot_instance.trapezoid_right_up_anchor, pg.TargetItem)
    assert isinstance(plot_instance.trapezoid_right_down_anchor, pg.TargetItem)


def test_anchor_initial_positions(plot_instance):
    assert plot_instance.trapezoid_left_down_anchor.pos().x() == 10
    assert plot_instance.trapezoid_left_up_anchor.pos().x() == 20
    assert plot_instance.trapezoid_right_up_anchor.pos().x() == 30
    assert plot_instance.trapezoid_right_down_anchor.pos().x() == 40


def test_left_down_anchor_interaction_valid(plot_instance, qtbot):
    initial_x = plot_instance.trapezoid_left_down_anchor.pos().x()

    new_pos = (initial_x + 5, 0)
    plot_instance.trapezoid_left_down_anchor.setPos(*new_pos)

    plot_instance.trapezoid_left_down_anchor.sigPositionChanged.emit(
        plot_instance.trapezoid_left_down_anchor)

    assert plot_instance.trap_x[1] == new_pos[0]
    assert plot_instance.trapezoid_plot_line.getData()[0][1] == new_pos[0]


def test_left_down_anchor_interaction_invalid(plot_instance, qtbot):
    initial_x = plot_instance.trapezoid_left_down_anchor.pos().x()

    plot_instance.trapezoid_left_down_anchor.setPos(-5, 0)
    plot_instance.trapezoid_left_down_anchor.sigPositionChanged.emit(
        plot_instance.trapezoid_left_down_anchor)

    assert plot_instance.trapezoid_left_down_anchor.pos().x() == initial_x


def test_left_up_anchor_interaction_valid(plot_instance, qtbot):
    initial_x = plot_instance.trapezoid_left_up_anchor.pos().x()

    new_pos = (initial_x + 5, 0)
    plot_instance.trapezoid_left_up_anchor.setPos(*new_pos)

    plot_instance.trapezoid_left_up_anchor.sigPositionChanged.emit(
        plot_instance.trapezoid_left_up_anchor)

    assert plot_instance.trap_x[2] == new_pos[0]
    assert plot_instance.trapezoid_plot_line.getData()[0][2] == new_pos[0]


def test_left_up_anchor_interaction_invalid(plot_instance, qtbot):
    initial_x = plot_instance.trapezoid_left_up_anchor.pos().x()

    plot_instance.trapezoid_left_up_anchor.setPos(-5, 0)
    plot_instance.trapezoid_left_up_anchor.sigPositionChanged.emit(
        plot_instance.trapezoid_left_up_anchor)

    plot_instance.trapezoid_left_up_anchor.setPos(200, 0)
    plot_instance.trapezoid_left_up_anchor.sigPositionChanged.emit(
        plot_instance.trapezoid_left_up_anchor)

    assert plot_instance.trapezoid_left_up_anchor.pos().x() == initial_x


def test_right_up_anchor_interaction_valid(plot_instance, qtbot):
    initial_x = plot_instance.trapezoid_right_up_anchor.pos().x()

    new_pos = (initial_x - 5, 0)
    plot_instance.trapezoid_right_up_anchor.setPos(*new_pos)

    plot_instance.trapezoid_right_up_anchor.sigPositionChanged.emit(
        plot_instance.trapezoid_left_up_anchor)

    assert plot_instance.trap_x[3] == new_pos[0]
    assert plot_instance.trapezoid_plot_line.getData()[0][3] == new_pos[0]


def test_right_up_anchor_interaction_invalid(plot_instance, qtbot):
    initial_x = plot_instance.trapezoid_right_up_anchor.pos().x()

    plot_instance.trapezoid_right_up_anchor.setPos(-5, 0)
    plot_instance.trapezoid_right_up_anchor.sigPositionChanged.emit(
        plot_instance.trapezoid_left_up_anchor)

    plot_instance.trapezoid_right_up_anchor.setPos(200, 0)
    plot_instance.trapezoid_right_up_anchor.sigPositionChanged.emit(
        plot_instance.trapezoid_left_up_anchor)

    assert plot_instance.trapezoid_right_up_anchor.pos().x() == initial_x


def test_right_down_anchor_interaction_valid(plot_instance, qtbot):
    initial_x = plot_instance.trapezoid_right_down_anchor.pos().x()

    new_pos = (initial_x - 5, 0)
    plot_instance.trapezoid_right_down_anchor.setPos(*new_pos)

    plot_instance.trapezoid_right_down_anchor.sigPositionChanged.emit(
        plot_instance.trapezoid_right_down_anchor)

    assert plot_instance.trap_x[4] == new_pos[0]
    assert plot_instance.trapezoid_plot_line.getData()[0][4] == new_pos[0]


def test_right_down_anchor_interaction_invalid(plot_instance, qtbot):
    initial_x = plot_instance.trapezoid_right_down_anchor.pos().x()

    plot_instance.trapezoid_right_down_anchor.setPos(200, 0)
    plot_instance.trapezoid_right_down_anchor.sigPositionChanged.emit(
        plot_instance.trapezoid_right_down_anchor)

    assert plot_instance.trapezoid_right_down_anchor.pos().x() == initial_x


def test_all_anchors_and_plot_update(plot_instance, qtbot):
    plot_instance.trapezoid_left_down_anchor.setPos(15, 0)
    plot_instance.trapezoid_left_up_anchor.setPos(25, 1)
    plot_instance.trapezoid_right_up_anchor.setPos(35, 1)
    plot_instance.trapezoid_right_down_anchor.setPos(45, 0)

    plot_instance.trapezoid_left_down_anchor.sigPositionChanged.emit(
        plot_instance.trapezoid_left_down_anchor)
    plot_instance.trapezoid_left_up_anchor.sigPositionChanged.emit(
        plot_instance.trapezoid_left_up_anchor)
    plot_instance.trapezoid_right_up_anchor.sigPositionChanged.emit(
        plot_instance.trapezoid_right_up_anchor)
    plot_instance.trapezoid_right_down_anchor.sigPositionChanged.emit(
        plot_instance.trapezoid_right_down_anchor)

    x_data_updated = plot_instance.trapezoid_plot_line.getData()[0]
    assert list(x_data_updated) == [0, 15, 25, 35, 45, 50]
