from PyQt6 import QtCore, QtGui, QtWidgets
from app.views.mf import MembershipFunction
from app.views.in_output import InOutput
import pyqtgraph as pg


def hide_axi(plot):
    """Universal function to hide the left and bottom axis of the plot"""
    left_axis = plot.getAxis('left')
    left_axis.hide()
    bottom_axis = plot.getAxis('bottom')
    bottom_axis.hide()


class FisTabView(QtWidgets.QTabWidget):
    membership_functions = []
    inputs = []
    outputs = []
    points = []
    plots = []

    colors = ["#0027FF", "#FF0000", "#3D7A00", "#FF2BE7", "#FFAE21", "#2AFF83"
                                                                     "#DF79FF", "#09FF24", "#FF723B", "#FF6CBA"]

    def __init__(self, parent=None):
        self.membership_functions.append(MembershipFunction(x=[0, 10], y=[0, 10]))
        self.membership_functions.append(MembershipFunction(x=[0, 10], y=[10, 0]))
        self.membership_functions.append(MembershipFunction(x=[0, 10], y=[5, 5]))
        self.input_1 = InOutput(mfs=self.membership_functions, name="Input 1")
        self.inputs.append(self.input_1)
        self.inputs.append(self.input_1)
        self.output_1 = InOutput(mfs=self.membership_functions, name="Output 1")
        self.outputs.append(self.output_1)
        super().__init__(parent)
        pg.setConfigOption('background', 'w')
        self.setObjectName("fisTab")
        self._setup_ui()
        self._retranslate_ui()

    def _setup_ui(self):
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
            self.points.append([160, position_y])
            self.plot_graphs(position_y, position_x=20, data=self.inputs[i])

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
            self.plot_graphs(position_y, position_x=330, data=self.outputs[i])

        scene = QtWidgets.QGraphicsScene(parent=self.graph_frame)
        self.graph_frame.setScene(scene)
        pen = QtGui.QPen()
        pen.setColor(QtGui.QColor("black"))
        pen.setWidth(2)
        for point in self.points:
            scene.addLine(point[0], point[1], 255, 180, pen)

        self.box_system_label = QtWidgets.QLabel(parent=self.graph_frame)
        self.box_system_label.setGeometry(175, 180, 140, 140)
        self.box_system_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.box_system_label.setStyleSheet("background-color: white; border: 1px solid gray")

    def _retranslate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        self.box_system_label.setText(_translate("Main Window", "Mamdani \nType 1"))
        self.system_label.setText(_translate("MainWindow", "System:"))
        self.name_label.setText(_translate("MainWindow", "Placeholder"))



    def plot_graphs(self, position_y, position_x, data):
        in_out_plot = pg.PlotWidget(parent=self.graph_frame)
        mfs = data.GetMfs()
        for i in range(len(mfs)):
            if i >= 10:
                in_out_plot.plot(mfs[i].getX(), mfs[i].getY(), pen='b')
            else:
                in_out_plot.plot(mfs[i].getX(), mfs[i].getY(), pen=self.colors[i])
        self.plots.append(in_out_plot)
        in_out_plot.setStyleSheet("background-color: #E5E8E8; border: 1px solid gray")
        in_out_plot.setGeometry(QtCore.QRect(position_x, position_y, 140, 140))

        name_label = QtWidgets.QLabel(parent=self.graph_frame)
        name_label.setGeometry(QtCore.QRect(position_x, position_y + 140, 140, 20))
        name_label.setStyleSheet("border: 0px")
        name_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        name_label.setText(f"{data.GetName()} ({len(data.GetMfs())} MFs)")

        hide_axi(in_out_plot)
