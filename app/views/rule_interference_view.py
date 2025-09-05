from PyQt6 import QtCore, QtGui, QtWidgets
import pyqtgraph as pg


class RuleInterferenceTabWidget(QtWidgets.QTabWidget):
    _counter_numb = 5
    x = [1, 10]
    y = [1, 10]

    def __init__(self, parent=None):
        super().__init__(parent)
        pg.setConfigOption('background', 'w')
        self.setObjectName("interferenceTab")
        self._setup_ui()
        self._retranslate_ui()

    def _setup_ui(self):
        self.system_label = QtWidgets.QLabel(parent=self)
        self.system_label.setGeometry(QtCore.QRect(10, 10, 51, 16))
        self.system_label.setObjectName("system_label")
        self.name_label = QtWidgets.QLabel(parent=self)

        self.name_label.setGeometry(QtCore.QRect(70, 10, 71, 16))
        self.name_label.setObjectName("name_label")

        self.ifLine_2 = QtWidgets.QFrame(parent=self)
        self.ifLine_2.setGeometry(QtCore.QRect(10, 20, 491, 20))
        self.ifLine_2.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.ifLine_2.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.ifLine_2.setObjectName("seperator_line")

        self.input_values_label = QtWidgets.QLabel(parent=self)
        self.input_values_label.setGeometry(QtCore.QRect(10, 45, 81, 21))
        self.input_values_label.setObjectName("input_values_label")

        self.input_values_edit = QtWidgets.QLineEdit(parent=self)
        self.input_values_edit.setGeometry(QtCore.QRect(110, 40, 161, 31))
        self.input_values_edit.setObjectName("input_values_edit")

        self.input_1_label = QtWidgets.QLabel(parent=self)
        self.input_1_label.setGeometry(QtCore.QRect(50, 90, 101, 16))
        self.input_1_label.setObjectName("input_1_label")

        self.input_2_label = QtWidgets.QLabel(parent=self)
        self.input_2_label.setGeometry(QtCore.QRect(180, 90, 101, 16))
        self.input_2_label.setObjectName("input_2_label")

        for i in range(self._counter_numb):
            counter = QtWidgets.QLabel(parent=self)
            counter.setGeometry(QtCore.QRect(10, 140 + 50 * i, 16, 16))
            counter.setText(str(i + 1))
            counter.setObjectName("counter_" + str(i + 1))

            connector_label = QtWidgets.QLabel(parent=self)
            connector_label.setGeometry(QtCore.QRect(304, 130 + 50 * i, 61, 41))
            connector_label.setObjectName("connector_label")
            connector_label.setText("<html><head/><body><p align=\"center\">AND <br/>(min)</p></body></html>")

        self.output_label = QtWidgets.QLabel(parent=self)
        self.output_label.setGeometry(QtCore.QRect(380, 90, 101, 20))
        self.output_label.setObjectName("output_label")

        self.activation_frame_input1 = QtWidgets.QFrame(parent=self)
        self.activation_frame_input1.setGeometry(QtCore.QRect(30, 120, 131, 61))
        self.activation_frame_input1.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.activation_frame_input1.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.activation_frame_input1.setObjectName("activation_frame_input1")

        frame_layout_1 = QtWidgets.QVBoxLayout(self.activation_frame_input1)
        self.activation_plot_input1 = pg.PlotWidget()
        self.activation_plot_input1.plot(self.x, self.y, pen='b', )

        self._hide_axi(self.activation_plot_input1)
        frame_layout_1.addWidget(self.activation_plot_input1)

        self.activation_frame_input2 = QtWidgets.QFrame(parent=self)
        self.activation_frame_input2.setGeometry(QtCore.QRect(170, 120, 131, 61))
        self.activation_frame_input2.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.activation_frame_input2.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.activation_frame_input2.setObjectName("activation_frame_input2")

        frame_layout_2 = QtWidgets.QVBoxLayout(self.activation_frame_input2)
        self.activation_plot_input2 = pg.PlotWidget()
        self.activation_plot_input2.plot(self.x[::-1], self.y, pen='b', )

        self._hide_axi(self.activation_plot_input2)
        frame_layout_2.addWidget(self.activation_plot_input2)

        self.activation_frame_output1 = QtWidgets.QFrame(parent=self)
        self.activation_frame_output1.setGeometry(QtCore.QRect(370, 120, 131, 61))
        self.activation_frame_output1.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.activation_frame_output1.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.activation_frame_output1.setObjectName("activation_frame_output1")

        frame_layout_3 = QtWidgets.QVBoxLayout(self.activation_frame_output1)
        self.activation_plot_output1 = pg.PlotWidget()
        x_o = [1, 5, 10]
        y_o = [1, 5, 1]
        self.activation_plot_output1.plot(x_o, y_o, pen='b',)

        self._hide_axi(self.activation_plot_output1)
        frame_layout_3.addWidget(self.activation_plot_output1)

        self.result_frame = QtWidgets.QFrame(parent=self)
        self.result_frame.setGeometry(QtCore.QRect(370, 200, 131, 61))
        self.result_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.result_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.result_frame.setObjectName("result_frame")

        self.horizontalSlider = QtWidgets.QSlider(parent=self)
        self.horizontalSlider.setGeometry(QtCore.QRect(30, 200, 121, 22))
        self.horizontalSlider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")

        self.horizontalSlider_2 = QtWidgets.QSlider(parent=self)
        self.horizontalSlider_2.setGeometry(QtCore.QRect(170, 200, 121, 22))
        self.horizontalSlider_2.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.horizontalSlider_2.setObjectName("horizontalSlider_2")

    def _retranslate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        self.system_label.setText(_translate("MainWindow", "System:"))
        self.name_label.setText(_translate("MainWindow", "Placeholder"))
        self.input_values_label.setText(_translate("MainWindow", "Input values"))
        self.input_values_edit.setText(_translate("MainWindow", "[50, 50]"))
        self.input_1_label.setText(_translate("MainWindow",
                                              "<html><head/><body><p><span style=\" font-weight:600;\">Input 1 = 50</span></p></body></html>"))
        self.input_2_label.setText(_translate("MainWindow",
                                              "<html><head/><body><p><span style=\" font-weight:600;\">Input 2 = 50</span></p></body></html>"))
        #self.counter.setText(_translate("MainWindow", "1"))
        self.output_label.setText(_translate("MainWindow",
                                             "<html><head/><body><p><span style=\" font-weight:600;\">Output 1 = 50</span></p></body></html>"))
        #self.connector_label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">AND <br/>(min)</p></body></html>"))

    def _hide_axi(self, plot):
        left_axis = plot.getAxis('left')
        left_axis.hide()
        bottom_axis = plot.getAxis('bottom')
        bottom_axis.hide()
