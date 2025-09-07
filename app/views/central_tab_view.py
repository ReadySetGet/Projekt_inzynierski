from PyQt6 import QtCore, QtGui, QtWidgets
from app.views.rule_interference_view import RuleInterferenceTabWidget, hide_axi
import numpy as np
import pyqtgraph as pg


class CentralTabWidget(QtWidgets.QTabWidget):
    addRuleClicked = QtCore.pyqtSignal()
    deleteRuleClicked = QtCore.pyqtSignal()
    #Poprawić skalę, podzielić na klasy ig
    tri_x = [0, 2.5, 5, 7.5, 10]
    tri_y = [0, 0, 10, 0, 0]
    trap_x = [0, 1, 2.5, 7.5, 9, 10]
    trap_y = [0, 0, 10, 10, 0, 0]

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

        self.triangle_central_anchor = pg.TargetItem(
            pos=(self.tri_x[2], self.tri_y[2]),
            size=10,
            symbol='o',
            pen="b",
            brush='b'
        )
        self.triangle_central_anchor.sigPositionChanged.connect(self._central_triangle_interaction)

        self.triangle_left_anchor = pg.TargetItem(
            pos=(self.tri_x[1], self.tri_y[1]),
            size=10,
            symbol='o',
            pen="b",
            brush='b'
        )
        self.triangle_left_anchor.sigPositionChanged.connect(self._left_triangle_interaction)

        self.triangle_right_anchor = pg.TargetItem(
            pos=(self.tri_x[3], self.tri_y[3]),
            size=10,
            symbol='o',
            pen="b",
            brush='b'
        )
        self.triangle_right_anchor.sigPositionChanged.connect(self._right_triangle_interaction)

        self.trapezoid_left_down_anchor = pg.TargetItem(
            pos=(self.trap_x[1], self.trap_y[1]),
            size=10,
            symbol='o',
            pen="r",
            brush='r'
        )
        self.trapezoid_left_down_anchor.sigPositionChanged.connect(self._left_down_trap_interaction)

        self.trapezoid_left_up_anchor = pg.TargetItem(
            pos=(self.trap_x[2], self.trap_y[2]),
            size=10,
            symbol='o',
            pen="r",
            brush='r'
        )
        self.trapezoid_left_up_anchor.sigPositionChanged.connect(self._left_up_trap_interaction)

        self.trapezoid_right_up_anchor = pg.TargetItem(
            pos=(self.trap_x[3], self.trap_y[3]),
            size=10,
            symbol='o',
            pen="r",
            brush='r'
        )
        self.trapezoid_right_up_anchor.sigPositionChanged.connect(self._right_up_trap_interaction)

        self.trapezoid_right_down_anchor = pg.TargetItem(
            pos=(self.trap_x[4], self.trap_y[4]),
            size=10,
            symbol='o',
            pen="r",
            brush='r'
        )
        self.trapezoid_right_down_anchor.sigPositionChanged.connect(self._right_down_trap_interaction)

        hide_axi(self.mf_plot_graph)

        self._plot_all()

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

    def _central_triangle_interaction(self):
        if (self.triangle_central_anchor.pos().x() > self.triangle_right_anchor.pos().x()
                or self.triangle_central_anchor.pos().x() < self.triangle_left_anchor.pos().x()):
            self.triangle_central_anchor.setPos(self.tri_x[2], self.tri_y[2])
        else:
            self.triangle_central_anchor.setPos(self.triangle_central_anchor.pos().x(), self.tri_y[2])
            self.tri_x[2] = self.triangle_central_anchor.pos().x()
        self._plot_all()

    def _left_triangle_interaction(self):
        if (self.triangle_left_anchor.pos().x() > self.triangle_central_anchor.pos().x()
                or self.triangle_left_anchor.pos().x() < 0):
            self.triangle_left_anchor.setPos(self.tri_x[1], self.tri_y[1])
        else:
            self.triangle_left_anchor.setPos(self.triangle_left_anchor.pos().x(),self.tri_y[1])
            self.tri_x[1] = self.triangle_left_anchor.pos().x()
        self._plot_all()

    def _right_triangle_interaction(self):
        if (self.triangle_right_anchor.pos().x() < self.triangle_central_anchor.pos().x()
                or self.triangle_right_anchor.pos().x() > 10):
            self.triangle_right_anchor.setPos(self.tri_x[3], self.tri_y[3])
        else:
            self.triangle_right_anchor.setPos(self.triangle_right_anchor.pos().x(), self.tri_y[3])
            self.tri_x[3] = self.triangle_right_anchor.pos().x()
        self._plot_all()

    def _left_down_trap_interaction(self):
        if (self.trapezoid_left_down_anchor.pos().x() < 0
                or self.trapezoid_left_down_anchor.pos().x() > self.trapezoid_left_up_anchor.pos().x()):
            self.trapezoid_left_down_anchor.setPos(self.trap_x[1], self.trap_y[1])
        else:
            self.trapezoid_left_down_anchor.setPos(self.trapezoid_left_down_anchor.pos().x(), self.trap_y[1])
            self.trap_x[1] = self.trapezoid_left_down_anchor.pos().x()
        self._plot_all()

    def _left_up_trap_interaction(self):
        if (self.trapezoid_left_up_anchor.pos().x() < self.trapezoid_left_down_anchor.pos().x()
                or self.trapezoid_left_up_anchor.pos().x() > self.trapezoid_right_up_anchor.pos().x()):
            self.trapezoid_left_up_anchor.setPos(self.trap_x[2], self.trap_y[2])
        else:
            self.trapezoid_left_up_anchor.setPos(self.trapezoid_left_up_anchor.pos().x(), self.trap_y[2])
            self.trap_x[2] = self.trapezoid_left_up_anchor.pos().x()
        self._plot_all()

    def _right_up_trap_interaction(self):
        if (self.trapezoid_right_up_anchor.pos().x() < self.trapezoid_left_up_anchor.pos().x()
                or self.trapezoid_right_up_anchor.pos().x() > self.trapezoid_right_down_anchor.pos().x()):
            self.trapezoid_right_up_anchor.setPos(self.trap_x[3], self.trap_y[3])
        else:
            self.trapezoid_right_up_anchor.setPos(self.trapezoid_right_up_anchor.pos().x(), self.trap_y[3])
            self.trap_x[3] = self.trapezoid_right_up_anchor.pos().x()
        self._plot_all()

    def _right_down_trap_interaction(self):
        if (self.trapezoid_right_down_anchor.pos().x() < self.trapezoid_right_up_anchor.pos().x()
                or self.trapezoid_right_down_anchor.pos().x() > 10):
            self.trapezoid_right_down_anchor.setPos(self.trap_x[4], self.trap_y[4])
        else:
            self.trapezoid_right_down_anchor.setPos(self.trapezoid_right_down_anchor.pos().x(), self.trap_y[4])
            self.trap_x[4] = self.trapezoid_right_down_anchor.pos().x()
        self._plot_all()

    def _plot_all(self):
        self.mf_plot_graph.clear()
        self.mf_plot_graph.plot(self.tri_x, self.tri_y, pen='b')
        self.mf_plot_graph.addItem(self.triangle_central_anchor)
        self.mf_plot_graph.addItem(self.triangle_left_anchor)
        self.mf_plot_graph.addItem(self.triangle_right_anchor)
        self.mf_plot_graph.plot(self.trap_x, self.trap_y, pen='r')
        self.mf_plot_graph.addItem(self.trapezoid_left_down_anchor)
        self.mf_plot_graph.addItem(self.trapezoid_left_up_anchor)
        self.mf_plot_graph.addItem(self.trapezoid_right_up_anchor)
        self.mf_plot_graph.addItem(self.trapezoid_right_down_anchor)
