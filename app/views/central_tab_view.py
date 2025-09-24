"""Create the central GUI window at the center of the application.

    Classes:
        CentralTabWidget: central window of the application displaying all the most important information about the system.
            Inherits from QTabWidget.
"""
from PyQt6 import QtCore, QtGui, QtWidgets
import numpy as np
import pyqtgraph as pg
from app.views.triangle_plot import TrianglePlot
from app.views.trapezoid_plot import TrapezoidPlot
from app.views.gauss_plot import GaussPlot
from app.views.bell_plot import BellPlot


class CentralTabWidget(QtWidgets.QTabWidget):
    """Class inheriting from QTabWidget.
        Allows user interaction via QPushButton GUI elements.

        Displays four tabs with information about different aspects of the system:
            Fis plot: tab responsible for displaying the plots of all the inputs and outputs in the system.
            MF plot: tab responsible for displaying individual input or output and interaction with the
                    membership functions.
            Rule editor: tab responsible for adding and deleting rules from the system and displaying them
                in a table.
            Interference tab: tab responsible for showing the user the end result of rule interference.

            Methods:
                __init__(QtWidget.*): create an instance of CentralTabWidget and bind it to the parent widget.

            Attributes:
                plots: list of plots added to the system
                placeholder attributes for testing purposes
    """
    plots = []

    tri_x = [-100.0, 25, 50, 75, 200]
    tri_y = [0.0, 0, 1, 0, 0]
    trap_x = [-100.0, 10, 25, 75, 90, 200]
    trap_y = [0.0, 0, 1, 1, 0, 0]

    mu = 50
    sigma = 16.67
    gauss_x = np.linspace(-100, 200, 400)
    gauss_y = np.exp(-(1 / 2) * ((gauss_x - mu) / sigma) ** 2)

    a = 20.0
    b = 2.0
    c = 50.0
    bell_x = np.linspace(-100, 200, 200)
    bell_y = 1 / (1 + np.abs((bell_x - c) / a) ** (2 * b))

    variable = "Name"

    def __init__(self, parent=None):
        super().__init__(parent)
        pg.setConfigOption('background', 'w')
        self.setObjectName("centralTab")
        self._setup_ui()
        self._retranslate_ui()

    def _setup_ui(self):
        self.fis_plot = QtWidgets.QWidget(parent=self)
        self.fis_plot.setObjectName("fis_plot")
        self.addTab(self.fis_plot, "")

        self.mf_plot = QtWidgets.QWidget()
        self.mf_plot.setObjectName("mf_plot")

        self.plot_frame = QtWidgets.QFrame(parent=self.mf_plot)
        self.plot_frame.setGeometry(QtCore.QRect(-5, 40, 521, 521))
        self.plot_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.plot_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.plot_frame.setObjectName("plot_frame")

        frame_layout = QtWidgets.QVBoxLayout(self.plot_frame)

        self.mf_plot_graph = pg.PlotWidget()
        self.mf_plot_graph.setXRange(0, 100)

        self.add_triangle_plot(self.tri_x, self.tri_y, 'b')

        self.add_trapezoid_plot(self.trap_x, self.trap_y, 'r')

        self.add_gauss_plot(self.gauss_x, self.gauss_y, self.sigma, self.mu, '#22B14C')

        self.add_bell_plot(self.bell_x, self.bell_y, self.a, self.b, self.c, '#B14D04')

        self.mf_plot_graph.setTitle("Membership Function Plot", color="black")
        self.mf_plot_graph.setLabel("left", "Degree of Membership", color="black")
        self.mf_plot_graph.setLabel("bottom", f"Input variable: {self.variable}", color="black")
        """Adding plot widget to the layout to display it."""
        frame_layout.addWidget(self.mf_plot_graph)

        self.seperator_line = QtWidgets.QFrame(parent=self.mf_plot)
        self.seperator_line.setGeometry(QtCore.QRect(0, 20, 501, 31))
        self.seperator_line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.seperator_line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.seperator_line.setObjectName("seperator_line")

        self.system_name_label = QtWidgets.QLabel(parent=self.mf_plot)
        self.system_name_label.setGeometry(QtCore.QRect(0, 10, 211, 16))
        self.system_name_label.setObjectName("system_name_label")
        self.addTab(self.mf_plot, "")

        self.rule_editor = QtWidgets.QWidget()
        self.rule_editor.setObjectName("rule_editor")

        self.seperator_line_2 = QtWidgets.QFrame(parent=self.rule_editor)
        self.seperator_line_2.setGeometry(QtCore.QRect(0, 20, 501, 31))
        self.seperator_line_2.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.seperator_line_2.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.seperator_line_2.setObjectName("seperator_line_2")

        self.system_label_2 = QtWidgets.QLabel(parent=self.rule_editor)
        self.system_label_2.setGeometry(QtCore.QRect(0, 10, 211, 16))
        self.system_label_2.setObjectName("system_label_2")

        self.addTab(self.rule_editor, "")

        self.rule_interference = QtWidgets.QWidget(parent=self)
        self.rule_interference.setObjectName("rule_interference")
        self.addTab(self.rule_interference, "")

    def _retranslate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWhatsThis(_translate("MainWindow", "<html><head/><body><p><br/></p><p><br/></p></body></html>"))
        self.setTabText(self.indexOf(self.fis_plot), _translate("MainWindow", "FIS Plot"))
        self.system_name_label.setText(_translate("MainWindow", "System: Placeholder Name"))
        self.setTabText(self.indexOf(self.mf_plot), _translate("MainWindow", "MF Editor"))
        self.system_label_2.setText(_translate("MainWindow", "System: Placeholder Name"))
        self.setTabText(self.indexOf(self.rule_editor), _translate("MainWindow", "Rule Editor"))
        self.setTabText(self.indexOf(self.rule_interference), _translate("MainWindow", "Rule Interference"))

    def add_triangle_plot(self, x, y, color) -> None:
        """
        Add a new triangle plot
        :param x: list[float] of the points on x axi
        :param y: list[float] of the points on y axi
        :param color: hexadecimal string representing colour
        :return: None
        """
        triangle = (TrianglePlot(
            plot_widget=self.mf_plot_graph,
            x_data=x,
            y_data=y,
            color=color,
        ))
        self.plots.append(triangle)

    def add_trapezoid_plot(self, x, y, color) -> None:
        """
        Add a new trapezoid plot
        :param x: list[float] of the points on x axi
        :param y: list[float] of the points on y axi
        :param color: hexadecimal string representing colour
        :return: None
        """
        trapezoid = (TrapezoidPlot(
            plot_widget=self.mf_plot_graph,
            x_data=x,
            y_data=y,
            color=color,
        ))
        self.plots.append(trapezoid)

    def add_gauss_plot(self, x, y, sigma, mu, color) -> None:
        """
        Add a new trapezoid plot
        :param x: list[float] of the points on x axi
        :param y: list[float] of the points on y axi
        :param sigma: float representing the standard deviation
        :param mu: float representing the median point on the x axi
        :param color: hexadecimal string representing colour
        :return: None
        """
        gauss = (GaussPlot(
            plot_widget=self.mf_plot_graph,
            x_data=x,
            y_data=y,
            sigma_data=sigma,
            mu_data=mu,
            color=color
        ))
        self.plots.append(gauss)

    def add_bell_plot(self, x, y, a, b, c, color) -> None:
        """
        Add a new trapezoid plot
        :param x: list[float] of the points on x axi
        :param y: list[float] of the points on y axi
        :param a: float, the a value from the f(x,a,b,c) = 1/(1 + |(x - c)/a|^2b) formula
        :param b: float, the b value from the f(x,a,b,c) = 1/(1 + |(x - c)/a|^2b) formula
        :param c: float, the c value from the f(x,a,b,c) = 1/(1 + |(x - c)/a|^2b) formula
        :param color: hexadecimal string representing colour
        :return: None
        """
        bell = (BellPlot(
            plot_widget=self.mf_plot_graph,
            x_data=x,
            y_data=y,
            a_data=a,
            b_data=b,
            c_data=c,
            color=color
        ))
        self.plots.append(bell)

