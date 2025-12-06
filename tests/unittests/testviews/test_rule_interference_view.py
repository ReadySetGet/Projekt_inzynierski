import pytest
import pyqtgraph as pg
from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt
from app.views.rule_interference_view import RuleInterferenceTabWidget


@pytest.fixture
def app():
    if QtWidgets.QApplication.instance() is None:
        return QtWidgets.QApplication([])
    return QtWidgets.QApplication.instance()


@pytest.fixture
def tested_widget(qtbot, app):
    widget = RuleInterferenceTabWidget()
    qtbot.addWidget(widget)
    return widget


def test_initial_state(tested_widget):
    assert tested_widget.system_label.text() == "System:"

    assert tested_widget.name_label.text() == "Placeholder"

    assert tested_widget.input_values_label.text() == "Input values"

    assert tested_widget.input_values_edit.text() == f"{tested_widget.slider_1_value}, {tested_widget.slider_2_value}"

    assert tested_widget.input_1_label.text() == (f"<html><head/><body><p><span style=\" font-weight:600;\">Input 1 = "
                                                  f"{tested_widget.slider_1_value}</span></p></body></html>")

    assert tested_widget.input_2_label.text() == (f"<html><head/><body><p><span style=\" font-weight:600;\">Input 2 = "
                                                  f"{tested_widget.slider_2_value}</span></p></body></html>")

    assert tested_widget.output_label.text() == ("<html><head/><body><p><span style=\" font-weight:600;\">Output 1 = "
                                                 "50</span></p></body></html>")


def test_object_names(tested_widget):
    assert tested_widget.system_label.objectName() == "system_label"
    assert tested_widget.name_label.objectName() == "name_label"
    assert tested_widget.seperator_line.objectName() == "seperator_line"
    assert tested_widget.input_values_label.objectName() == "input_values_label"
    assert tested_widget.input_values_edit.objectName() == "input_values_edit"
    assert tested_widget.input_1_label.objectName() == "input_1_label"
    assert tested_widget.input_2_label.objectName() == "input_2_label"
    assert tested_widget.output_label.objectName() == "output_label"
    assert tested_widget.result_frame.objectName() == "result_frame"
    assert tested_widget.result_plot.objectName() == "result_plot"
    assert tested_widget.horizontalSlider.objectName() == "horizontalSlider"
    assert tested_widget.horizontalSlider_2.objectName() == "horizontalSlider_2"

    for i in range(5):
        counter = tested_widget.findChild(QtWidgets.QLabel, "counter_" + str(i + 1))
        assert counter.objectName() == "counter_" + str(i + 1)

        activation_input_1 = tested_widget.findChild(QtWidgets.QFrame, f"activation_frame_input1_{i}")
        assert activation_input_1.objectName() == f"activation_frame_input1_{i}"

        activation_plot_1 = activation_input_1.findChild(pg.PlotWidget, f"activation_plot_input1_{i}")
        assert activation_plot_1.objectName() == f"activation_plot_input1_{i}"

        activation_input_2 = tested_widget.findChild(QtWidgets.QFrame, f"activation_frame_input2_{i}")
        assert activation_input_2.objectName() == f"activation_frame_input2_{i}"

        activation_plot_2 = activation_input_2.findChild(pg.PlotWidget, f"activation_plot_input2_{i}")
        assert activation_plot_2.objectName() == f"activation_plot_input2_{i}"

        activation_output_1 = tested_widget.findChild(QtWidgets.QFrame, f"activation_frame_output1_{i}")
        assert activation_output_1.objectName() == f"activation_frame_output1_{i}"

        activation_plot_3 = activation_output_1.findChild(pg.PlotWidget, f"activation_plot_output1_{i}")
        assert activation_plot_3.objectName() == f"activation_plot_output1_{i}"


def test_types(tested_widget):
    assert isinstance(tested_widget, QtWidgets.QWidget)
    assert isinstance(tested_widget.system_label, QtWidgets.QLabel)
    assert isinstance(tested_widget.name_label, QtWidgets.QLabel)
    assert isinstance(tested_widget.seperator_line, QtWidgets.QFrame)
    assert isinstance(tested_widget.input_values_label, QtWidgets.QLabel)
    assert isinstance(tested_widget.input_values_edit, QtWidgets.QLineEdit)
    assert isinstance(tested_widget.input_1_label, QtWidgets.QLabel)
    assert isinstance(tested_widget.input_2_label, QtWidgets.QLabel)
    assert isinstance(tested_widget.output_label, QtWidgets.QLabel)
    assert isinstance(tested_widget.result_frame, QtWidgets.QFrame)
    assert isinstance(tested_widget.result_plot, pg.PlotWidget)
    assert isinstance(tested_widget.horizontalSlider, QtWidgets.QSlider)
    assert isinstance(tested_widget.horizontalSlider_2, QtWidgets.QSlider)

    for i in range(5):
        counter = tested_widget.findChild(QtWidgets.QLabel, "counter_" + str(i + 1))
        assert isinstance(counter, QtWidgets.QLabel)

        activation_input_1 = tested_widget.findChild(QtWidgets.QFrame, f"activation_frame_input1_{i}")
        assert isinstance(activation_input_1, QtWidgets.QFrame)

        activation_plot_1 = activation_input_1.findChild(pg.PlotWidget, f"activation_plot_input1_{i}")
        assert isinstance(activation_plot_1, pg.PlotWidget)

        activation_input_2 = tested_widget.findChild(QtWidgets.QFrame, f"activation_frame_input2_{i}")
        assert isinstance(activation_input_2, QtWidgets.QFrame)

        activation_plot_2 = activation_input_2.findChild(pg.PlotWidget, f"activation_plot_input2_{i}")
        assert isinstance(activation_plot_2, pg.PlotWidget)

        activation_output_1 = tested_widget.findChild(QtWidgets.QFrame, f"activation_frame_output1_{i}")
        assert isinstance(activation_output_1, QtWidgets.QFrame)

        activation_plot_3 = activation_output_1.findChild(pg.PlotWidget, f"activation_plot_output1_{i}")
        assert isinstance(activation_plot_3, pg.PlotWidget)


def test_slider_1(qtbot, tested_widget):
    slider = tested_widget.findChild(QtWidgets.QSlider, "horizontalSlider")

    with qtbot.waitSignal(tested_widget.value_changed, timeout=1000, raising=True):
        slider.setValue(75)

    assert tested_widget.slider_1_value == 75
    assert tested_widget.input_values_edit.text() == "75, 50"


def test_slider_2(qtbot, tested_widget):
    slider = tested_widget.findChild(QtWidgets.QSlider, "horizontalSlider_2")
    with qtbot.waitSignal(tested_widget.value_changed, timeout=1000, raising=True):
        slider.setValue(75)

    assert tested_widget.slider_2_value == 75
    assert tested_widget.input_values_edit.text() == "50, 75"


def test_edit_valid(qtbot, tested_widget):
    edit = tested_widget.findChild(QtWidgets.QLineEdit, "input_values_edit")
    with qtbot.waitSignal(tested_widget.value_changed, timeout=1000, raising=True):
        edit.setText("75, 75")

    assert tested_widget.horizontalSlider.value() == 75
    assert tested_widget.input_values_edit.text() == "75, 75"
    assert tested_widget.horizontalSlider_2.value() == 75



