import pytest
from PyQt6 import QtWidgets
import pyqtgraph as pg
from app.views.triangle_plot import TrianglePlot


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

    x_data = [0, 10, 20, 40, 50]
    y_data = [0, 0, 1, 0, 0]
    color = '#ff0000'

    return TrianglePlot(plot_widget, x_data, y_data, color)


def test_initialization(plot_instance):
    assert isinstance(plot_instance, TrianglePlot)
    assert isinstance(plot_instance.triangle_plot_line, pg.PlotDataItem)

    assert isinstance(plot_instance.triangle_left_anchor, pg.TargetItem)
    assert isinstance(plot_instance.triangle_right_anchor, pg.TargetItem)
    assert isinstance(plot_instance.triangle_central_anchor, pg.TargetItem)


def test_anchor_initial_positions(plot_instance):
    assert plot_instance.triangle_left_anchor.pos().x() == 10
    assert plot_instance.triangle_central_anchor.pos().x() == 20
    assert plot_instance.triangle_right_anchor.pos().x() == 40


def test_left_anchor_interaction_valid(plot_instance, qtbot):
    initial_x = plot_instance.triangle_left_anchor.pos().x()

    new_pos = (initial_x + 5, 0)
    plot_instance.triangle_left_anchor.setPos(*new_pos)

    plot_instance.triangle_left_anchor.sigPositionChanged.emit(
        plot_instance.triangle_left_anchor)

    assert plot_instance.tri_x[1] == new_pos[0]
    assert plot_instance.triangle_plot_line.getData()[0][1] == new_pos[0]


def test_left_anchor_interaction_invalid(plot_instance, qtbot):
    initial_x = plot_instance.triangle_left_anchor.pos().x()

    plot_instance.triangle_left_anchor.setPos(-5, 0)
    plot_instance.triangle_left_anchor.sigPositionChanged.emit(
        plot_instance.triangle_left_anchor)

    assert plot_instance.triangle_left_anchor.pos().x() == initial_x


def test_central_anchor_interaction_valid(plot_instance, qtbot):
    initial_x = plot_instance.triangle_central_anchor.pos().x()

    new_pos = (initial_x + 5, 0)
    plot_instance.triangle_central_anchor.setPos(*new_pos)

    plot_instance.triangle_central_anchor.sigPositionChanged.emit(
        plot_instance.triangle_central_anchor)

    assert plot_instance.tri_x[2] == new_pos[0]
    assert plot_instance.triangle_plot_line.getData()[0][2] == new_pos[0]


def test_central_anchor_interaction_invalid(plot_instance, qtbot):
    initial_x = plot_instance.triangle_central_anchor.pos().x()

    plot_instance.triangle_central_anchor.setPos(-5, 0)
    plot_instance.triangle_central_anchor.sigPositionChanged.emit(
        plot_instance.triangle_central_anchor)

    plot_instance.triangle_central_anchor.setPos(200, 0)
    plot_instance.triangle_central_anchor.sigPositionChanged.emit(
        plot_instance.triangle_central_anchor)

    assert plot_instance.triangle_central_anchor.pos().x() == initial_x


def test_right_anchor_interaction_valid(plot_instance, qtbot):
    initial_x = plot_instance.triangle_right_anchor.pos().x()

    new_pos = (initial_x - 5, 0)
    plot_instance.triangle_right_anchor.setPos(*new_pos)

    plot_instance.triangle_right_anchor.sigPositionChanged.emit(
        plot_instance.triangle_right_anchor)

    assert plot_instance.tri_x[3] == new_pos[0]
    assert plot_instance.triangle_plot_line.getData()[0][3] == new_pos[0]


def test_right_anchor_interaction_invalid(plot_instance, qtbot):
    initial_x = plot_instance.triangle_right_anchor.pos().x()

    plot_instance.triangle_right_anchor.setPos(200, 0)
    plot_instance.triangle_right_anchor.sigPositionChanged.emit(
        plot_instance.triangle_right_anchor)

    assert plot_instance.triangle_right_anchor.pos().x() == initial_x


def test_all_anchors_and_plot_update(plot_instance, qtbot):
    plot_instance.triangle_left_anchor.setPos(15, 0)
    plot_instance.triangle_central_anchor.setPos(25, 1)
    plot_instance.triangle_right_anchor.setPos(35, 1)

    plot_instance.triangle_left_anchor.sigPositionChanged.emit(
        plot_instance.triangle_left_anchor)
    plot_instance.triangle_central_anchor.sigPositionChanged.emit(
        plot_instance.triangle_central_anchor)
    plot_instance.triangle_right_anchor.sigPositionChanged.emit(
        plot_instance.triangle_right_anchor)

    x_data_updated = plot_instance.triangle_plot_line.getData()[0]
    assert list(x_data_updated) == [0, 15, 25, 35, 50]
