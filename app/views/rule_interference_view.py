"""Create the rule interference tab as part of the center window of the application.

    Classes:
        RuleInterferenceTabWidget: central window of the application displaying all the most important information about the system.
            Inherits from QTabWidget.
    Functions:
        hide_axi(pg.PlotWidget): hides the x and y axi of the given plot.
"""
from PyQt6 import QtCore, QtGui, QtWidgets
import pyqtgraph as pg


def hide_axi(plot) -> None:
    """Universal function to hide the left and bottom axis of the plot"""
    left_axis = plot.getAxis('left')
    left_axis.hide()
    bottom_axis = plot.getAxis('bottom')
    bottom_axis.hide()


class RuleInterferenceTabWidget(QtWidgets.QWidget):
    """Class inheriting from QWidget.
        Displays the rule interference window and allows user interaction with the data.

        Methods:
            __init__(QtWidget.*): create an instance of CentralTabWidget and bind it to the parent widget.

        Attributes:
            placeholder attributes for testing purposes
            block_sliders: boolean, used to control cyclical signal calls
    """

    _counter_numb = 5
    # Example Placeholder data
    x = [0, 10]
    y = [0, 10]
    x_o = [0, 5, 10]
    y_o = [0, 10, 0]
    x_a = [0, 2.5, 7.5, 10]
    y_a = [0, 5, 5, 0]
    slider_1_value = 50
    slider_2_value = 50

    block_sliders = False

    def __init__(self, parent=None):
        """Initialize a new class instance.

                Parameters:
                    parent: The parent widget, in this case central tab, to which the widget will be attached.
        """
        super().__init__(parent)
        pg.setConfigOption('background', 'w')
        self.setObjectName("interferenceTab")
        self._setup_ui()
        self._retranslate_ui()

    def _setup_ui(self):
        """Set up all the GUI sub elements."""
        self.system_label = QtWidgets.QLabel(parent=self)
        self.system_label.setGeometry(QtCore.QRect(10, 10, 51, 16))
        self.system_label.setObjectName("system_label")

        self.name_label = QtWidgets.QLabel(parent=self)
        self.name_label.setGeometry(QtCore.QRect(70, 10, 71, 16))
        self.name_label.setObjectName("name_label")

        self.seperator_line = QtWidgets.QFrame(parent=self)
        self.seperator_line.setGeometry(QtCore.QRect(10, 20, 491, 20))
        self.seperator_line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.seperator_line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.seperator_line.setObjectName("seperator_line")

        self.input_values_label = QtWidgets.QLabel(parent=self)
        self.input_values_label.setGeometry(QtCore.QRect(10, 45, 81, 21))
        self.input_values_label.setObjectName("input_values_label")

        self.input_values_edit = QtWidgets.QLineEdit(parent=self)
        self.input_values_edit.setGeometry(QtCore.QRect(110, 40, 161, 31))
        self.input_values_edit.setObjectName("input_values_edit")
        self.input_values_edit.textChanged.connect(self._update_from_editor_field)

        self.input_1_label = QtWidgets.QLabel(parent=self)
        self.input_1_label.setGeometry(QtCore.QRect(65, 90, 101, 16))
        self.input_1_label.setObjectName("input_1_label")

        self.input_2_label = QtWidgets.QLabel(parent=self)
        self.input_2_label.setGeometry(QtCore.QRect(195, 90, 101, 16))
        self.input_2_label.setObjectName("input_2_label")

        for i in range(self._counter_numb):
            counter = QtWidgets.QLabel(parent=self)
            counter.setGeometry(QtCore.QRect(10, 140 + 80 * i, 16, 16))
            counter.setText(str(i + 1))
            counter.setObjectName("counter_" + str(i + 1))

            connector_label = QtWidgets.QLabel(parent=self)
            connector_label.setGeometry(QtCore.QRect(304, 130 + 80 * i, 61, 41))
            connector_label.setObjectName("connector_label")
            connector_label.setText("<html><head/><body><p align=\"center\">AND <br/>(min)</p></body></html>")

            self.activation_frame_input1 = QtWidgets.QFrame(parent=self)
            self.activation_frame_input1.setGeometry(QtCore.QRect(30, 120 + 80 * i, 131, 61))
            self.activation_frame_input1.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
            self.activation_frame_input1.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
            self.activation_frame_input1.setObjectName("activation_frame_input1")

            frame_layout_1 = QtWidgets.QVBoxLayout(self.activation_frame_input1)
            self.activation_plot_input1 = pg.PlotWidget()
            self.activation_plot_input1.plot(self.x, self.y, pen='b')

            hide_axi(self.activation_plot_input1)
            frame_layout_1.addWidget(self.activation_plot_input1)

            self.activation_frame_input2 = QtWidgets.QFrame(parent=self)
            self.activation_frame_input2.setGeometry(QtCore.QRect(170, 120 + 80 * i, 131, 61))
            self.activation_frame_input2.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
            self.activation_frame_input2.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
            self.activation_frame_input2.setObjectName("activation_frame_input2")

            frame_layout_2 = QtWidgets.QVBoxLayout(self.activation_frame_input2)
            self.activation_plot_input2 = pg.PlotWidget()
            self.activation_plot_input2.plot(self.x[::-1], self.y, pen='b')

            hide_axi(self.activation_plot_input2)
            frame_layout_2.addWidget(self.activation_plot_input2)

            self.activation_frame_output1 = QtWidgets.QFrame(parent=self)
            self.activation_frame_output1.setGeometry(QtCore.QRect(370, 120 + 80 * i, 131, 61))
            self.activation_frame_output1.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
            self.activation_frame_output1.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
            self.activation_frame_output1.setObjectName("activation_frame_output1")

            frame_layout_3 = QtWidgets.QVBoxLayout(self.activation_frame_output1)
            self.activation_plot_output1 = pg.PlotWidget()

            self.activation_plot_output1.plot(self.x_o, self.y_o, pen='b')
            self.activation_plot_output1.plot(self.x_a, self.y_a, brush='b', fillLevel=0.0)

            hide_axi(self.activation_plot_output1)
            frame_layout_3.addWidget(self.activation_plot_output1)

        self.output_label = QtWidgets.QLabel(parent=self)
        self.output_label.setGeometry(QtCore.QRect(395, 90, 101, 20))
        self.output_label.setObjectName("output_label")

        self.result_frame = QtWidgets.QFrame(parent=self)
        self.result_frame.setGeometry(QtCore.QRect(370, 200 + + 60 * self._counter_numb, 131, 61))
        self.result_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.result_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.result_frame.setObjectName("result_frame")

        result_layout = QtWidgets.QVBoxLayout(self.result_frame)

        self.result_plot = pg.PlotWidget()
        self.result_plot.plot(self.x_a, self.y_a, pen='b', brush='b', fillLevel=0.0)
        self.result_plot.setObjectName("result_plot")
        hide_axi(self.result_plot)

        result_layout.addWidget(self.result_plot)

        self.horizontalSlider = QtWidgets.QSlider(parent=self)
        self.horizontalSlider.setGeometry(QtCore.QRect(30, 200 + 60 * self._counter_numb, 121, 22))
        self.horizontalSlider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.horizontalSlider.setValue(self.slider_1_value)
        self.horizontalSlider.valueChanged.connect(self._update_from_sliders)

        self.horizontalSlider_2 = QtWidgets.QSlider(parent=self)
        self.horizontalSlider_2.setGeometry(QtCore.QRect(170, 200 + 60 * self._counter_numb, 121, 22))
        self.horizontalSlider_2.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.horizontalSlider_2.setObjectName("horizontalSlider_2")
        self.horizontalSlider_2.setValue(self.slider_2_value)
        self.horizontalSlider_2.valueChanged.connect(self._update_from_sliders)

    def _retranslate_ui(self):
        """Add text to all the respective GUI elements."""
        _translate = QtCore.QCoreApplication.translate
        self.system_label.setText(_translate("MainWindow", "System:"))
        self.name_label.setText(_translate("MainWindow", "Placeholder"))
        self.input_values_label.setText(_translate("MainWindow", "Input values"))

        self.input_values_edit.setText(_translate("MainWindow", f"{self.slider_1_value}, {self.slider_2_value}"))
        self.input_1_label.setText(_translate("MainWindow",
                                              f"<html><head/><body><p><span style=\" font-weight:600;\">"
                                              f"Input 1 = {self.slider_1_value}</span></p></body></html>"))
        self.input_2_label.setText(_translate("MainWindow",
                                              f"<html><head/><body><p><span style=\" font-weight:600;\">"
                                              f"Input 2 = {self.slider_2_value}</span></p></body></html>"))
        self.output_label.setText(_translate("MainWindow",
                                             "<html><head/><body><p><span style=\" font-weight:600;\">Output 1 = "
                                             "50</span></p></body></html>"))

    def _update_from_sliders(self) -> None:
        """Function which updates the editor field whenever slider positions change."""
        if not self.block_sliders:
            self.slider_1_value = self.horizontalSlider.value()
            self.slider_2_value = self.horizontalSlider_2.value()
            self.input_values_edit.setText(f"{self.slider_1_value}, {self.slider_2_value}")
            self.input_1_label.setText(f"<html><head/><body><p><span style=\" font-weight:600;\">"
                                       f"Input 1 = {self.slider_1_value}</span></p></body></html>")
            self.input_2_label.setText(f"<html><head/><body><p><span style=\" font-weight:600;\">"
                                       f"Input 2 = {self.slider_2_value}</span></p></body></html>")

    def _update_from_editor_field(self) -> None:
        """Function which updates the slider positions whenever the editor field changes."""
        s = self.input_values_edit.text()
        newstr = ''.join((ch if ch in '0123456789.-' else ' ') for ch in s)
        list_of_numbers = [int(i) for i in newstr.split()]

        self.block_sliders = True

        print(list_of_numbers)

        self.slider_1_value = list_of_numbers[0]
        self.slider_2_value = list_of_numbers[1]

        self.horizontalSlider.setValue(self.slider_1_value)
        self.horizontalSlider_2.setValue(self.slider_2_value)

        self.input_1_label.setText(f"<html><head/><body><p><span style=\" font-weight:600;\">"
                                   f"Input 1 = {self.slider_1_value}</span></p></body></html>")
        self.input_2_label.setText(f"<html><head/><body><p><span style=\" font-weight:600;\">"
                                   f"Input 2 = {self.slider_2_value}</span></p></body></html>")
        self.block_sliders = False
