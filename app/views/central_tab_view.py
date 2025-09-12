from PyQt6 import QtCore, QtGui, QtWidgets
from app.views.rule_interference_view import RuleInterferenceTabWidget
import numpy as np
import pyqtgraph as pg
from app.views.triangle_plot import TrianglePlot
from app.views.trapezoid_plot import TrapezoidPlot
from app.views.gauss_plot import GaussPlot
from app.views.bell_plot import BellPlot


class CentralTabWidget(QtWidgets.QTabWidget):
    addRuleClicked = QtCore.pyqtSignal()
    deleteRuleClicked = QtCore.pyqtSignal()
    tri_x = [-100.0, 25, 50, 75, 200]
    tri_y = [0.0, 0, 1, 0, 0]
    trap_x = [-100.0, 10, 25, 75, 90, 200]
    trap_y = [0.0, 0, 1, 1, 0, 0]

    mu = 50
    sigma = 16.67
    gauss_x = np.linspace(-100, 200, 400)
    gauss_y = np.exp(-(1/2) * ((gauss_x - mu) / sigma)**2)

    a = 20.0
    b = 2.0
    c = 50.0
    bell_x = np.linspace(-100, 200, 200)
    bell_y = 1 / (1 + np.abs((bell_x - c) / a)**(2 * b))

    variable = "Name"

    def __init__(self, parent=None):
        super().__init__(parent)
        pg.setConfigOption('background', 'w')
        self.setObjectName("centralTab")
        self._setup_ui()
        self._retranslate_ui()

    def _setup_ui(self):
        self.fis_plot = QtWidgets.QWidget()
        self.fis_plot.setObjectName("fis_plot")

        self.graph_frame = QtWidgets.QFrame(parent=self.fis_plot)
        self.graph_frame.setGeometry(QtCore.QRect(-1, 49, 461, 471))
        self.graph_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.graph_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.graph_frame.setObjectName("graph_frame")
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
        self.mf_plot_graph.setXRange(0,100)

        self.triangle = (TrianglePlot(
            plot_widget=self.mf_plot_graph,
            x_data=self.tri_x,
            y_data=self.tri_y,
            color='b',
            central_x=50
            )
        )

        self.trapezoid = (TrapezoidPlot(
            plot_widget=self.mf_plot_graph,
            x_data=self.trap_x,
            y_data=self.trap_y,
            color='r',
            central_x=50
        ))

        self.gauss = (GaussPlot(
            plot_widget=self.mf_plot_graph,
            x_data=self.gauss_x,
            y_data=self.gauss_y,
            sigma_data=self.sigma,
            mu_data=self.mu,
            color='#22B14C'
        ))

        self.bell = (BellPlot(
            plot_widget=self.mf_plot_graph,
            x_data=self.bell_x,
            y_data=self.bell_y,
            a_data=self.a,
            b_data=self.b,
            c_data=self.c,
            color='#B14D04'
        ))

        self.mf_plot_graph.setTitle("Membership Function Plot", color="black")
        self.mf_plot_graph.setLabel("left", "Degree of Membership", color="black")
        self.mf_plot_graph.setLabel("bottom", f"Input variable: {self.variable}", color="black")

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

        self.table_widget = QtWidgets.QTableWidget(parent=self.rule_editor)
        self.table_widget.setGeometry(QtCore.QRect(20, 100, 431, 491))
        self.table_widget.setObjectName("table_widget")
        self.table_widget.setColumnCount(0)
        self.table_widget.setRowCount(0)

        self.add_rule_button = QtWidgets.QPushButton(parent=self.rule_editor)
        self.add_rule_button.setGeometry(QtCore.QRect(460, 100, 41, 28))
        self.add_rule_button.setObjectName("addRuleButton")
        self.add_rule_button.clicked.connect(self.addRuleClicked.emit)

        self.delete_rule_button = QtWidgets.QPushButton(parent=self.rule_editor)
        self.delete_rule_button.setGeometry(QtCore.QRect(460, 140, 41, 28))
        self.delete_rule_button.setObjectName("delete_rule_button")
        self.delete_rule_button.clicked.connect(self.deleteRuleClicked.emit)

        self.seperator_line_2 = QtWidgets.QFrame(parent=self.rule_editor)
        self.seperator_line_2.setGeometry(QtCore.QRect(0, 20, 501, 31))
        self.seperator_line_2.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.seperator_line_2.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.seperator_line_2.setObjectName("seperator_line_2")

        self.system_label_2 = QtWidgets.QLabel(parent=self.rule_editor)
        self.system_label_2.setGeometry(QtCore.QRect(0, 10, 211, 16))
        self.system_label_2.setObjectName("system_label_2")

        self.addTab(self.rule_editor, "")

        self.rule_interference = RuleInterferenceTabWidget()
        self.rule_interference.setObjectName("rule_interference")
        self.addTab(self.rule_interference, "")

    def _retranslate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWhatsThis(_translate("MainWindow", "<html><head/><body><p><br/></p><p><br/></p></body></html>"))
        self.setTabText(self.indexOf(self.fis_plot), _translate("MainWindow", "FIS Plot"))
        self.system_name_label.setText(_translate("MainWindow", "System: Placeholder Name"))
        self.setTabText(self.indexOf(self.mf_plot), _translate("MainWindow", "MF Editor"))
        self.add_rule_button.setText(_translate("MainWindow", "+"))
        self.delete_rule_button.setText(_translate("MainWindow", "X"))
        self.system_label_2.setText(_translate("MainWindow", "System: Placeholder Name"))
        self.setTabText(self.indexOf(self.rule_editor), _translate("MainWindow", "Rule Editor"))
        self.setTabText(self.indexOf(self.rule_interference), _translate("MainWindow", "Rule Interference"))
