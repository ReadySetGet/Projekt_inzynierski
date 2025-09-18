from PyQt6 import QtCore, QtGui, QtWidgets
from app.views.mf import MembershipFunction
import pyqtgraph as pg


def hide_axi(plot):
    """Universal function to hide the left and bottom axis of the plot"""
    left_axis = plot.getAxis('left')
    left_axis.hide()
    bottom_axis = plot.getAxis('bottom')
    bottom_axis.hide()


class FisTabView(QtWidgets.QTabWidget):
    input1 = []
    inputs = []
    outputs = []
    points = []

    colors = ["#0027FF", "#FF0000", "#3D7A00", "#FF2BE7", "#FFAE21", "#2AFF83"
                                                                     "#DF79FF", "#09FF24", "#FF723B", "#FF6CBA"]

    def __init__(self, parent=None):
        self.input1.append(MembershipFunction(x=[0, 10], y=[0, 10]))
        self.input1.append(MembershipFunction(x=[0, 10], y=[10, 0]))
        self.input1.append(MembershipFunction(x=[0, 10], y=[5, 5]))
        self.inputs.append(self.input1)
        self.inputs.append(self.input1)
        #self.inputs.append(self.input1)
        #self.inputs.append(self.input1)
        self.outputs.append(self.input1)
        super().__init__(parent)
        pg.setConfigOption('background', 'w')
        self.setObjectName("fisTab")
        self._setup_ui()
        #self._retranslate_ui()

    def _setup_ui(self):
        self.graph_frame = QtWidgets.QGraphicsView(parent=self)
        self.graph_frame.setGeometry(QtCore.QRect(10, 60, 490, 500))
        self.graph_frame.setFrameShape(QtWidgets.QGraphicsView.Shape.StyledPanel)
        self.graph_frame.setFrameShadow(QtWidgets.QGraphicsView.Shadow.Raised)
        self.graph_frame.setStyleSheet("background-color: #E5E8E8; border: 1px solid gray")
        self.graph_frame.setObjectName("graph_frame")

        for i in range(len(self.inputs)):
            """"For loop responsible for plotting the variable number of membership 
            function plots and result plots."""
            if len(self.inputs) == 1:
                position_y = 180
            elif len(self.inputs) == 2:
                height = 490
                position_y = int(height / len(self.inputs) * i + 60)
            elif len(self.inputs) == 3:
                height = 490
                position_y = int(height / len(self.inputs) * i + 10)
            else:
                position_y = int(5 + 50 * i)
            self.points.append([175, position_y])
            self.plot_inputs(i, position_y)

        for i in range(len(self.outputs)):
            if len(self.outputs) == 1:
                position_y = 180
            elif len(self.outputs) == 2:
                height = 490
                position_y = int(height / len(self.inputs) * i + 60)
            elif len(self.outputs) == 3:
                height = 490
                position_y = int(height / len(self.inputs) * i + 10)
            else:
                position_y = int(5 + 50 * i)
            self.points.append([340, position_y])
            self.plot_outputs(i, position_y)

        scene = QtWidgets.QGraphicsScene(parent=self.graph_frame)
        self.graph_frame.setScene(scene)
        pen = QtGui.QPen()
        pen.setColor(QtGui.QColor("black"))
        pen.setWidth(2)
        for point in self.points:
            print(point)
            scene.addLine(point[0], point[1], 255, 180, pen)

        system_label = QtWidgets.QLabel(parent=self.graph_frame)
        system_label.setGeometry(177, 190, 140, 140)
        system_label.setText("Mamdani \nType 1")
        system_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        system_label.setStyleSheet("background-color: white; border: 1px solid gray")

    def plot_inputs(self, i, position_y):
        frame_input = QtWidgets.QFrame(parent=self.graph_frame)
        frame_input.setGeometry(QtCore.QRect(15, position_y, 160, 160))
        frame_input.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        frame_input.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        frame_input.setStyleSheet("background-color: #E5E8E8; border: 0px")
        frame_input.setObjectName("activation_frame_input1")

        frame_layout_1 = QtWidgets.QVBoxLayout(frame_input)
        plot_input = pg.PlotWidget()
        for j in range(len(self.inputs[i])):
            if j >= 10:
                plot_input.plot(self.inputs[i][j].getX(), self.inputs[i][j].getY(), pen='b')
            else:
                plot_input.plot(self.inputs[i][j].getX(), self.inputs[i][j].getY(), pen=self.colors[j])
        plot_input.setStyleSheet("background-color: #E5E8E8; border: 1px solid gray")

        hide_axi(plot_input)
        frame_layout_1.addWidget(plot_input)

    def plot_outputs(self, i, position_y):
        frame_output = QtWidgets.QFrame(parent=self.graph_frame)
        frame_output.setGeometry(QtCore.QRect(320, position_y, 160, 160))
        frame_output.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        frame_output.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        frame_output.setStyleSheet("background-color: #E5E8E8; border: 0px")
        frame_output.setObjectName("activation_frame_input1")

        frame_layout_2 = QtWidgets.QVBoxLayout(frame_output)
        plot_output = pg.PlotWidget()
        for j in range(len(self.inputs[i])):
            if j >= 10:
                plot_output.plot(self.inputs[i][j].getX(), self.inputs[i][j].getY(), pen='b')
            else:
                plot_output.plot(self.inputs[i][j].getX(), self.inputs[i][j].getY(), pen=self.colors[j])
        plot_output.setStyleSheet("background-color: #E5E8E8; border: 1px solid gray")

        hide_axi(plot_output)
        frame_layout_2.addWidget(plot_output)
