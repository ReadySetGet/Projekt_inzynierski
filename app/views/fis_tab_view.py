"""Create a widget GUI element responsible for displaying the inputs and outputs inside the fis system.
    Classes:
        FisTabView: a widget inheriting from QWidget responsible for displaying the plots of all the inputs
        and outputs inside the fis system as well as the system name.

Temporarily(?) imports placeholder classes in MembershipFunction and InOutput.
"""

from PyQt6 import QtCore, QtGui, QtWidgets
from app.views.mf import MembershipFunction
from app.views.in_output import InOutput
import pyqtgraph as pg


def hide_axi(plot):
    """Hide the left and bottom axis of the plot
        Parameters:
            plot: the plot which will have its axis removed.
    """
    left_axis = plot.getAxis('left')
    left_axis.hide()
    bottom_axis = plot.getAxis('bottom')
    bottom_axis.hide()


class FisTabView(QtWidgets.QWidget):
    """Class inheriting from QWidget.
        Displays the inputs and outputs inside fis system as plots.

        Methods:
            __init__(parent): create an instance of MFPropertiesWidget and bind it to the parent window.
            remove_plots(): remove every single plot and label from the widget. Clear the graphic scene.
            add_input(inp): add a new input to the system, recalculate plot positions, redraw plots and labels.
            add_output(out): add a new output to the system, recalculate plot positions, redraw plots and labels.
            remove_input(inp): remove an input to the system, recalculate plot positions, redraw plots and labels.
            remove_output(out): remove an output to the system, recalculate plot positions, redraw plots and labels.
        Attributes:
            membership_functions: membership functions present within the system.
            inputs: fis inputs present within the system.
            outputs: fis outputs present within the system.
            points: list of points to draw lines between in order to show connections
            plots: list of plots created and displayed by the class
            labels: list of labels of aforementioned plots
            middle_height: the middle point of the frame taken as a baseline for plotting
            gap: the gap between plots
            colors: table of colours used to differentiate different membership functions
    """
    membership_functions = []
    inputs = []
    outputs = []
    points = []
    plots = []
    labels = []
    middle_height = 180
    gap = 160
    colors = ["#0027FF", "#FF0000", "#3D7A00", "#FF2BE7", "#FFAE21", "#2AFF83"
                                                                     "#DF79FF", "#09FF24", "#FF723B", "#FF6CBA"]

    def __init__(self, parent=None):
        """Initialize a new class instance.

            Parameters:
                parent: The parent widget, in this case central tab, to which the widget will be attached.
        """
        #Set up placeholder data for testing
        self.membership_functions.append(MembershipFunction(x=[0, 10], y=[0, 10]))
        self.membership_functions.append(MembershipFunction(x=[0, 10], y=[10, 0]))
        self.membership_functions.append(MembershipFunction(x=[0, 10], y=[5, 5]))
        self.input_1 = InOutput(mfs=self.membership_functions, name="Input 1")
        self.inputs.append(self.input_1)
        self.inputs.append(self.input_1)
        self.output_1 = InOutput(mfs=self.membership_functions, name="Output 1")
        self.outputs.append(self.output_1)
        self.outputs.append(self.output_1)
        super().__init__(parent)
        pg.setConfigOption('background', 'w')
        self.setObjectName("fisTab")
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

        self.graph_frame = QtWidgets.QGraphicsView(parent=self)
        self.graph_frame.setGeometry(QtCore.QRect(10, 60, 490, 510))
        self.graph_frame.setFrameShape(QtWidgets.QGraphicsView.Shape.StyledPanel)
        self.graph_frame.setFrameShadow(QtWidgets.QGraphicsView.Shadow.Raised)
        self.graph_frame.setStyleSheet("background-color: #E5E8E8; border: 1px solid gray")
        self.graph_frame.setObjectName("graph_frame")

        plot_positions = self._calculate_plot_positions(self.inputs, "input")
        for i in range(len(self.inputs)):
            #self.plot_graphs(position_y=plot_positions[i], position_x=20, data=self.inputs[i])
            break

        plot_positions = self._calculate_plot_positions(self.outputs, "output")

        for i in range(len(self.outputs)):
            #self.plot_graphs(position_y=plot_positions[i], position_x=330, data=self.outputs[i])
            break

        self.scene = QtWidgets.QGraphicsScene(parent=self.graph_frame)
        self.graph_frame.setScene(self.scene)
        self.pen = QtGui.QPen()
        self.pen.setColor(QtGui.QColor("black"))
        self.pen.setWidth(2)
        self._draw_lines()

        self.box_system_label = QtWidgets.QLabel(parent=self.graph_frame)
        self.box_system_label.setGeometry(175, 180, 140, 140)
        self.box_system_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.box_system_label.setStyleSheet("background-color: white; border: 1px solid gray")
        self.remove_plots()
        #self.add_input(self.input_1)
        self.add_output(self.output_1)

    def _retranslate_ui(self):
        """Add text to all the respective GUI elements."""
        _translate = QtCore.QCoreApplication.translate
        self.box_system_label.setText(_translate("Main Window", "Mamdani \nType 1"))
        self.system_label.setText(_translate("MainWindow", "System:"))
        self.name_label.setText(_translate("MainWindow", "Placeholder"))

    def _plot_graphs(self, position_y, position_x, data):
        """
        Plot all the input or output data as graphs and label them.
        :param position_y: the y position where in the window the plot frame gets displayed
        :param position_x:  the x position where in the window the plot frame gets displayed
        :param data: an In_Output class object representing the data of an input or an output
        """
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
        self.labels.append(name_label)

        hide_axi(in_out_plot)

    def _calculate_plot_positions(self, data, side):
        """
        Class which calculates the positions in which the plot frames will get displayed as well
        as point coordinates to connect via pen.
        :param data: list of all the inputs or outputs to plot
        :param side: whether the data is supposed to get displayed on the 'input' side (left) or 'output' side (right)
        :return: returns the list of calculated frame positions
        """
        positions = []
        x_pos = 0
        if side == "input":
            x_pos = 20
        elif side == "output":
            x_pos = 330
        else:
            return -1

        if len(data) % 2 != 0:
            positions.append(self.middle_height)
            self.points.append([x_pos + self.gap / 2, self.middle_height])
            pair_numb = (len(data) - 1) // 2
            for i in range(1, pair_numb + 1):
                positions.append(self.middle_height - i * self.gap)
                self.points.append([x_pos + self.gap / 2, self.middle_height - i * self.gap])
                positions.append(self.middle_height + i * self.gap)
                self.points.append([x_pos + self.gap / 2, self.middle_height + i * self.gap])

        else:
            pair_numb = (len(data)) // 2
            for i in range(pair_numb):
                positions.append(int(self.middle_height - (i + 0.5) * 160))
                self.points.append([x_pos + self.gap / 2, int(self.middle_height - (i + 0.5) * self.gap)])
                positions.append(int(self.middle_height + (i + 0.5) * 160))
                self.points.append([x_pos + self.gap / 2, int(self.middle_height + (i + 0.5) * self.gap)])
        return positions

    def _draw_lines(self):
        """Clears the graphic scene and draws lines connecting all the plot frames with the system name frame."""
        self.scene.clear()
        for point in self.points:
            self.scene.addLine(point[0], point[1], 255, 180, self.pen)

    def remove_plots(self):
        """Remove all plots, labels and points from the widget. Clear the graphic scene."""
        for label in self.labels:
            label.setParent(None)
            label.deleteLater()
        self.labels.clear()
        for plot in self.plots:
            plot.setParent(None)
            plot.deleteLater()
        self.plots.clear()
        self.scene.clear()
        self.points.clear()

    def add_input(self, inp):
        """
        Add a new input to the system. Calculate new plot positions, redraw plots and labels.
        :param inp: fis input
        """
        self.inputs.append(inp)
        self.remove_plots()
        input_pos = self._calculate_plot_positions(self.inputs, "input")
        for i in range(len(self.inputs)):
            self._plot_graphs(position_y=input_pos[i], position_x=20, data=self.inputs[i])

        output_pos = self._calculate_plot_positions(self.outputs, "output")
        for i in range(len(self.outputs)):
            self._plot_graphs(position_y=output_pos[i], position_x=330, data=self.outputs[i])

        self._draw_lines()

    def add_output(self, out):
        """
            Add a new output to the system. Calculate new plot positions, redraw plots and labels.
            :param out: fis input
        """
        self.outputs.append(out)
        self.remove_plots()
        input_pos = self._calculate_plot_positions(self.inputs, "input")
        for i in range(len(self.inputs)):
            self._plot_graphs(position_y=input_pos[i], position_x=20, data=self.inputs[i])

        output_pos = self._calculate_plot_positions(self.outputs, "output")
        for i in range(len(self.outputs)):
            self._plot_graphs(position_y=output_pos[i], position_x=330, data=self.outputs[i])

        self._draw_lines()

    def remove_input(self, inp):
        """
            Remove an input from the system. Calculate new plot positions, redraw plots and labels.
            :param inp: fis input
        """
        self.inputs.remove(inp)
        self.remove_plots()
        input_pos = self._calculate_plot_positions(self.inputs, "input")
        for i in range(len(self.inputs)):
            self._plot_graphs(position_y=input_pos[i], position_x=20, data=self.inputs[i])

        output_pos = self._calculate_plot_positions(self.outputs, "output")
        for i in range(len(self.outputs)):
            self._plot_graphs(position_y=output_pos[i], position_x=330, data=self.outputs[i])

        self._draw_lines()

    def remove_output(self, out):
        """
            Remove an output from the system. Calculate new plot positions, redraw plots and labels.
            :param out: fis output
        """
        self.outputs.remove(out)
        self.remove_plots()
        input_pos = self._calculate_plot_positions(self.inputs, "input")
        for i in range(len(self.inputs)):
            self._plot_graphs(position_y=input_pos[i], position_x=20, data=self.inputs[i])

        output_pos = self._calculate_plot_positions(self.outputs, "output")
        for i in range(len(self.outputs)):
            self._plot_graphs(position_y=output_pos[i], position_x=330, data=self.outputs[i])

        self._draw_lines()
