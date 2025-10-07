from PyQt6 import QtCore, QtGui, QtWidgets
from app.views.rule_interference_view import RuleInterferenceTabWidget
import numpy as np
import pyqtgraph as pg
import re
from app.views.triangle_plot import TrianglePlot
from app.views.trapezoid_plot import TrapezoidPlot
from app.views.gauss_plot import GaussPlot
from app.views.bell_plot import BellPlot
from app.views.rule import Rule
from app.views.in_output import InOutput
from app.views.fis_tab_view import FisTabView


def _regex_func(match) -> str:
    """Fuction responsible for substituting the antecedent ==
    with consequent = after the => symbol"""
    then = match.group(1)
    after = match.group(2)
    consequent = re.sub(r"==", r'=', after)
    return then + consequent


class CentralTabWidget(QtWidgets.QTabWidget):
    """Central tab of the program responsible for displaying MF plots, input/output plots,
    rule interference plots and all the rules present in the program."""
    addRuleClicked = QtCore.pyqtSignal()
    deleteRuleClicked = QtCore.pyqtSignal()
    _symbols = {
        "is": "==",
        "is not": "~=",
        "then": "=>",
        "and": "&",
        "or": "|"
    }
    tri_x = [-100.0, 25, 50, 75, 200]
    tri_y = [0.0, 0, 1, 0, 0]
    trap_x = [-100.0, 10, 25, 75, 90, 200]
    trap_y = [0.0, 0, 1, 1, 0, 0]

    """Placeholder data for rule generation"""
    inputs = []
    input_1 = InOutput("wysokie", ["wysokie", "przeciętne", "niskie"])
    input_2 = InOutput("drzewa", ["obiekt", "drzewo"])
    inputs.append(input_1)
    inputs.append(input_2)

    outputs = []
    output = InOutput("wysokie drzewa", ["niski obiekt", "średni obiekt", "wysoki obiekt",
                                         "niskie drzewo", "średnie drzewo", "wysokie drzewo"])
    outputs.append(output)

    rules = []

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

    def __init__(self, parent=None, status_bar=None):
        super().__init__(parent)
        pg.setConfigOption('background', 'w')
        self.setObjectName("centralTab")
        self.status_bar = status_bar
        self._setup_ui()
        self._retranslate_ui()

    def _setup_ui(self):
        self.fis_plot = FisTabView()
        self.fis_plot.setObjectName("fis_plot")
        self.addTab(self.fis_plot, "")

        self.mf_plot = QtWidgets.QWidget()
        self.mf_plot.setObjectName("mf_plot")

        """Creation of the plot frame in which membership functions will be displayed."""
        self.plot_frame = QtWidgets.QFrame(parent=self.mf_plot)
        self.plot_frame.setGeometry(QtCore.QRect(-5, 40, 521, 521))
        self.plot_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.plot_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.plot_frame.setObjectName("plot_frame")

        """Creating layout and binding it to the frame."""
        frame_layout = QtWidgets.QVBoxLayout(self.plot_frame)

        """Creation of plot widget which is responsible for plotting the membership functions."""
        self.mf_plot_graph = pg.PlotWidget()
        self.mf_plot_graph.setXRange(0, 100)

        """Creating plots"""
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

        self.add_all_rules_button = QtWidgets.QPushButton(parent=self.rule_editor)
        self.add_all_rules_button.setGeometry(QtCore.QRect(20, 60, 140, 28))
        self.add_all_rules_button.setObjectName("add_all_rules")
        self.add_all_rules_button.clicked.connect(self.generateRules)

        """Setting up the rules table widget."""
        self.table_widget = QtWidgets.QTableWidget(parent=self.rule_editor)
        self.table_widget.setGeometry(QtCore.QRect(20, 100, 431, 491))
        self.table_widget.setObjectName("table_widget")
        self.table_widget.setRowCount(1)
        self.table_widget.setColumnCount(3)
        self.table_widget.setColumnWidth(0, 314)
        self.table_widget.setColumnWidth(1, 50)
        self.table_widget.setColumnWidth(2, 50)

        self.table_widget.setHorizontalHeaderLabels(["Rule", "Weight", "Name"])

        self.clear_rules_button = QtWidgets.QPushButton(parent=self.rule_editor)
        self.clear_rules_button.setGeometry(QtCore.QRect(180, 60, 100, 28))
        self.clear_rules_button.setObjectName("clear_rules")
        self.clear_rules_button.clicked.connect(self.clearTable)

        self.rule_style_dropdown = QtWidgets.QComboBox(parent=self.rule_editor)
        self.rule_style_dropdown.setGeometry(QtCore.QRect(300, 60, 100, 28))
        self.rule_style_dropdown.setObjectName("rule_style_dropdown")
        self.rule_style_dropdown.addItems(['Verbose', 'Symbolic', 'Indexed'])
        self.rule_style_dropdown.currentIndexChanged.connect(self._update_rule_style)

        self.add_rule_button = QtWidgets.QPushButton(parent=self.rule_editor)
        self.add_rule_button.setGeometry(QtCore.QRect(460, 100, 41, 28))
        self.add_rule_button.setObjectName("addRuleButton")
        self.add_rule_button.clicked.connect(self.add_rule)

        self.delete_rule_button = QtWidgets.QPushButton(parent=self.rule_editor)
        self.delete_rule_button.setGeometry(QtCore.QRect(460, 140, 41, 28))
        self.delete_rule_button.setObjectName("delete_rule_button")
        self.delete_rule_button.clicked.connect(self.remove_rule)

        self.seperator_line_2 = QtWidgets.QFrame(parent=self.rule_editor)
        self.seperator_line_2.setGeometry(QtCore.QRect(0, 20, 501, 31))
        self.seperator_line_2.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.seperator_line_2.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.seperator_line_2.setObjectName("seperator_line_2")

        self.system_label_2 = QtWidgets.QLabel(parent=self.rule_editor)
        self.system_label_2.setGeometry(QtCore.QRect(0, 10, 211, 16))
        self.system_label_2.setObjectName("system_label_2")

        self.addTab(self.rule_editor, "")

        self.rule_interference = RuleInterferenceTabWidget(status_bar=self.status_bar)
        self.rule_interference.setObjectName("rule_interference")
        self.addTab(self.rule_interference, "")

    def _retranslate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWhatsThis(_translate("MainWindow", "<html><head/><body><p><br/></p><p><br/></p></body></html>"))
        self.setTabText(self.indexOf(self.fis_plot), _translate("MainWindow", "FIS Plot"))
        self.system_name_label.setText(_translate("MainWindow", "System: Placeholder Name"))
        self.add_all_rules_button.setText(_translate("MainWindow", "Add All Possible Rules"))
        self.setTabText(self.indexOf(self.mf_plot), _translate("MainWindow", "MF Editor"))
        self.clear_rules_button.setText(_translate("MainWindow", "Clear Rules"))
        self.add_rule_button.setText(_translate("MainWindow", "+"))
        self.delete_rule_button.setText(_translate("MainWindow", "X"))
        self.system_label_2.setText(_translate("MainWindow", "System: Placeholder Name"))
        self.setTabText(self.indexOf(self.rule_editor), _translate("MainWindow", "Rule Editor"))
        self.setTabText(self.indexOf(self.rule_interference), _translate("MainWindow", "Rule Interference"))

    #Placeholder bo nie mam danych z back endu jak to generować
    def generateRules(self):
        in_numb = len(self.inputs)
        out_numb = len(self.outputs)

        for i in range(in_numb - 1):
            input1 = self.inputs[i]
            input2 = self.inputs[i + 1]
            for j in range(out_numb):
                output = self.outputs[j]
                input1_mfs = input1.GetMfs()
                input2_mfs = input2.GetMfs()
                output_mfs = output.GetMfs()
                output_index = 0

                for k in range(len(input1_mfs)):
                    for g in range(len(input2_mfs)):
                        new_rule = Rule(input1.GetName(), input1_mfs[k], "1",
                                        input2.GetName(), input2_mfs[g], "2",
                                        output.GetName(), output_mfs[output_index], "3",
                                        "is", "and", "1", f"Rule {len(self.rules) + 1}")
                        self.rules.append(new_rule)
                        output_index += 1
        self.fillTable()
        self.status_bar.showMessage("Last action: added all possible rule combinations.")

    def fillTable(self):
        """Function responsible for filling the rules table with rules.
        Displays as many rows as there are rules in the program"""
        rule_numb = len(self.rules)
        display_type = self.rule_style_dropdown.currentText()
        self.table_widget.setRowCount(rule_numb)
        for i in range(rule_numb):
            if display_type == "Symbolic":
                symbolic_rule = self.rules[i].getRule()
                pattern = r'\b({})\b'.format('|'.join(sorted(re.escape(k) for k in self._symbols)))
                symbolic_rule = re.sub(pattern, lambda m: self._symbols.get(m.group(0)), symbolic_rule)
                symbolic_rule = re.sub(r'(=>)(.*)', _regex_func, symbolic_rule)
                self.table_widget.setItem(i, 0, QtWidgets.QTableWidgetItem(symbolic_rule))
            elif display_type == "Indexed":
                rule = self.rules[i]
                indexed_rule = (f"{rule.getInputMfNumbers()}, {rule.getOutputMfNumbers()}, ({rule.getWeight()}) "
                                f": {rule.getConnector()}")
                self.table_widget.setItem(i, 0, QtWidgets.QTableWidgetItem(indexed_rule))
            else:
                self.table_widget.setItem(i, 0, QtWidgets.QTableWidgetItem(self.rules[i].getRule()))
            self.table_widget.setItem(i, 1, QtWidgets.QTableWidgetItem(self.rules[i].getWeight()))
            self.table_widget.setItem(i, 2, QtWidgets.QTableWidgetItem(self.rules[i].getName()))

    def clearTable(self):
        """Function responsible for clearing the rule table and deleting rules present in the system.
        Sets one empty row as default for aesthetic purposes."""
        self.table_widget.clear()
        self.table_widget.setHorizontalHeaderLabels(["Rule", "Weight", "Name"])
        self.table_widget.setRowCount(1)
        self.table_widget.setColumnCount(3)
        self.rules = []
        self.status_bar.showMessage("Last action: cleared all rules.")

    def add_rule(self):
        """Adds a new rule to the table and data of the application."""
        self.addRuleClicked.emit()
        input1 = self.inputs[0]
        input2 = self.inputs[1]
        output = self.outputs[0]
        input1_mfs = input1.GetMfs()
        input2_mfs = input2.GetMfs()
        output_mfs = output.GetMfs()
        new_rule = Rule(input1.GetName(), input1_mfs[0],
                        input2.GetName(), input2_mfs[0],
                        output.GetName(), output_mfs[0],
                        "is not", "and", "1", f"Rule {len(self.rules) + 1}")
        self.rules.append(new_rule)
        self.fillTable()
        self.status_bar.showMessage("Last action: added new rule.")

    def remove_rule(self):
        """Removes selected rule from the table and data of the application."""
        row = self.table_widget.currentRow()

        del self.rules[row]
        self.fillTable()
        self.deleteRuleClicked.emit()
        self.status_bar.showMessage("Last action: removed a rule.")

    def _update_rule_style(self):
        self.table_widget.clear()
        self.table_widget.setHorizontalHeaderLabels(["Rule", "Weight", "Name"])
        self.table_widget.setColumnCount(3)
        self.fillTable()
