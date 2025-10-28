"""Create the central GUI window at the center of the application.

Classes:
    CentralTabWidget: central window of the application displaying all the most
        important information about the system. Inherits from QTabWidget.
"""

import re

import numpy as np
import pyqtgraph as pg
from PyQt6 import QtCore, QtWidgets

from app.view_models.central_tab_view_model import CentralTabViewModel
from app.views.base_tab_view import BaseTabView
from app.views.bell_plot import BellPlot
from app.views.fis_tab_view import FisTabView
from app.views.gauss_plot import GaussPlot
from app.views.in_output import InOutput
from app.views.rule import Rule
from app.views.rule_interference_view import RuleInterferenceTabWidget
from app.views.trapezoid_plot import TrapezoidPlot
from app.views.triangle_plot import TrianglePlot


def _regex_func(match) -> str:
    """Function responsible for substituting the antecedent ==.

    Substitutes with consequent = after the => symbol.

    Args:
        match: Regex match object.

    Returns:
        Modified string.
    """
    then = match.group(1)
    after = match.group(2)
    consequent = re.sub(r"==", r"=", after)
    return then + consequent


class CentralTabWidget(BaseTabView):
    """Central tab of the program.

    Responsible for displaying MF plots, input/output plots, rule interference plots
    and all the rules present in the program.
    """

    addRuleClicked = QtCore.pyqtSignal()
    deleteRuleClicked = QtCore.pyqtSignal()
    _symbols = {"is": "==", "is not": "~=", "then": "=>", "and": "&", "or": "|"}
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
    output = InOutput(
        "wysokie drzewa",
        [
            "niski obiekt",
            "średni obiekt",
            "wysoki obiekt",
            "niskie drzewo",
            "średnie drzewo",
            "wysokie drzewo",
        ],
    )
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
        """Initialize the central tab widget.

        Args:
            parent: Parent widget
            status_bar: Status bar widget
        """
        super().__init__(parent=parent)
        pg.setConfigOption("background", "w")
        self.setObjectName("centralTab")
        self.status_bar = status_bar

        self.view_model = CentralTabViewModel()
        self.view_model.setParent(self)

        # Store MF plots
        self.mf_plots = []

        self._setup_ui()
        self._retranslate_ui()
        self._connect_view_model_signals()

    def _setup_ui(self):
        self.fis_plot = FisTabView()
        self.fis_plot.setObjectName("fis_plot")
        self.addTab(self.fis_plot, "")

        self.mf_plot = QtWidgets.QWidget()
        self.mf_plot.setObjectName("mf_plot")

        # Creation of the plot frame in which membership functions will be displayed.
        self.plot_frame = QtWidgets.QFrame(parent=self.mf_plot)
        self.plot_frame.setGeometry(QtCore.QRect(-5, 40, 521, 521))
        self.plot_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.plot_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.plot_frame.setObjectName("plot_frame")

        # Creating layout and binding it to the frame.
        frame_layout = QtWidgets.QVBoxLayout(self.plot_frame)

        # Creation of plot widget which is responsible for plotting
        # the membership functions.
        self.mf_plot_graph = pg.PlotWidget()
        self.mf_plot_graph.setXRange(0, 100)

        # Plots will be created dynamically based on selected variable's MFs
        # Placeholder plots removed - will be loaded from fuzzy service

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

        self._connect_view_model_signals()
        self._setup_sample_data()

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
        self.rule_style_dropdown.addItems(["Verbose", "Symbolic", "Indexed"])
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
        self.setWhatsThis(self.t("<html><head/><body><p><br/></p><p><br/></p></body></html>"))
        self.setTabText(self.indexOf(self.fis_plot), self.t("FIS_PLOT"))
        self.system_name_label.setText(self.t("SYSTEM_PLACEHOLDER_NAME"))
        self.add_all_rules_button.setText(self.t("ADD_ALL_POSSIBLE_RULES"))
        self.setTabText(self.indexOf(self.mf_plot), self.t("MF_EDITOR"))
        self.clear_rules_button.setText(self.t("CLEAR_RULES"))
        self.add_rule_button.setText(self.t("PLUS"))
        self.delete_rule_button.setText(self.t("X"))
        self.system_label_2.setText(self.t("SYSTEM_PLACEHOLDER_NAME"))
        self.setTabText(self.indexOf(self.rule_editor), self.t("RULE_EDITOR"))
        self.setTabText(
            self.indexOf(self.rule_interference),
            self.t("RULE_INTERFERENCE"),
        )

    # Placeholder bo nie mam danych z back endu jak to generować
    def generateRules(self):
        """Generate all possible rules based on inputs and outputs."""
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
                        new_rule = Rule(
                            input1.GetName(),
                            input1_mfs[k],
                            "1",
                            input2.GetName(),
                            input2_mfs[g],
                            "2",
                            output.GetName(),
                            output_mfs[output_index],
                            "3",
                            "is",
                            "and",
                            "1",
                            f"Rule {len(self.rules) + 1}",
                        )
                        self.rules.append(new_rule)
                        output_index += 1
        self.fillTable()
        self.status_bar.showMessage("Last action: added all possible rule combinations.")

    def fillTable(self):
        """Fill the rules table with rules.

        Displays as many rows as there are rules in the program.
        """
        rule_numb = len(self.rules)
        display_type = self.rule_style_dropdown.currentText()
        self.table_widget.setRowCount(rule_numb)
        for i in range(rule_numb):
            if display_type == "Symbolic":
                symbolic_rule = self.rules[i].getRule()
                pattern = r"\b({})\b".format("|".join(sorted(re.escape(k) for k in self._symbols)))
                symbolic_rule = re.sub(pattern, lambda m: self._symbols.get(m.group(0)), symbolic_rule)
                symbolic_rule = re.sub(r"(=>)(.*)", _regex_func, symbolic_rule)
                self.table_widget.setItem(i, 0, QtWidgets.QTableWidgetItem(symbolic_rule))
            elif display_type == "Indexed":
                rule = self.rules[i]
                indexed_rule = (
                    f"{rule.getInputMfNumbers()}, {rule.getOutputMfNumbers()}, "
                    f" ({rule.getWeight()}) : {rule.getConnector()}"
                )
                self.table_widget.setItem(i, 0, QtWidgets.QTableWidgetItem(indexed_rule))
            else:
                self.table_widget.setItem(i, 0, QtWidgets.QTableWidgetItem(self.rules[i].getRule()))
            self.table_widget.setItem(i, 1, QtWidgets.QTableWidgetItem(self.rules[i].getWeight()))
            self.table_widget.setItem(i, 2, QtWidgets.QTableWidgetItem(self.rules[i].getName()))

    def clearTable(self):
        """Clear the rule table and delete rules present in the system.

        Sets one empty row as default for aesthetic purposes.
        """
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
        new_rule = Rule(
            input1.GetName(),
            input1_mfs[0],
            0,  # mf1_numb
            input2.GetName(),
            input2_mfs[0],
            0,  # mf2_numb
            output.GetName(),
            output_mfs[0],
            0,  # mf3_numb
            "is not",
            "and",
            "1",
            f"Rule {len(self.rules) + 1}",
        )
        self.rules.append(new_rule)
        self.fillTable()
        self.status_bar.showMessage("Last action: added new rule.")

    def remove_rule(self):
        """Removes selected rule from the table and data of the application."""
        row = self.table_widget.currentRow()

        if row < 0 or row >= len(self.rules):
            self.status_bar.showMessage("No rule selected to remove.")
            return

        del self.rules[row]
        self.fillTable()
        self.deleteRuleClicked.emit()
        self.status_bar.showMessage("Last action: removed a rule.")

    def _update_rule_style(self):
        self.table_widget.clear()
        self.table_widget.setHorizontalHeaderLabels(["Rule", "Weight", "Name"])
        self.table_widget.setColumnCount(3)
        self.fillTable()

    def _connect_view_model_signals(self):
        """Connect view model signals to widget slots."""
        if hasattr(self.view_model, "data_changed"):
            self.view_model.data_changed.connect(self._on_data_changed)

        # Initial load of MF plots
        self._load_mf_plots()

    def _on_data_changed(self):
        """Handle data changed signal from view model."""
        self._load_mf_plots()

    def _load_mf_plots(self):
        """Load and display membership function plots for the selected input or output variable."""
        self._clear_mf_plots()

        fuzzy_service = self.view_model.fuzzy_service if hasattr(self.view_model, "fuzzy_service") else None
        if not fuzzy_service:
            return

        # Check for selected input or output
        selected_input_name = fuzzy_service.get_selected_input_name()
        selected_output_name = fuzzy_service.get_selected_output_name()

        variable_name = None
        variable_type = None
        variable_data = None

        if selected_input_name:
            # Input is selected
            variable_name = selected_input_name
            variable_type = "input"
            variable_data = fuzzy_service.get_selected_input_data()
        elif selected_output_name:
            # Output is selected
            variable_name = selected_output_name
            variable_type = "output"
            variable_data = fuzzy_service.get_selected_output_data()
        else:
            # No selection - don't force a selection, just return
            return

        if not variable_data:
            return

        mfs = variable_data.get("membership_functions", [])
        var_range = variable_data.get("range", [0, 100])

        self.mf_plot_graph.setXRange(var_range[0], var_range[1])

        var_type_label = "Input" if variable_type == "input" else "Output"
        self.mf_plot_graph.setLabel("bottom", f"{var_type_label} variable: {variable_name}", color="black")

        # Define colors for different MFs
        colors = [
            "b",
            "r",
            "#22B14C",
            "#B14D04",
            "#FF00FF",
            "#00FFFF",
            "#FFFF00",
            "#FF8800",
        ]

        for i, mf in enumerate(mfs):
            mf_type = mf.get("type", "trimf")
            mf_name = mf.get("name", f"MF{i}")
            mf_params = mf.get("parameters", [])
            color = colors[i % len(colors)]

            plot_obj = self._create_mf_plot(mf_type, mf_name, mf_params, var_range, color, i)
            if plot_obj:
                self.mf_plots.append(
                    {
                        "plot": plot_obj,
                        "mf_index": i,
                        "mf_name": mf_name,
                        "variable_name": variable_name,
                        "variable_type": variable_type,
                        "var_range": var_range,
                    }
                )

    def _create_mf_plot(self, mf_type, mf_name, mf_params, var_range, color, mf_index):
        """Create a membership function plot based on its type.

        Args:
            mf_type: Type of MF (trimf, trapmf, gaussmf, gbellmf)
            mf_name: Name of the MF
            mf_params: Parameters of the MF
            var_range: Range of the variable [min, max]
            color: Color for the plot
            mf_index: Index of the MF

        Returns:
            Plot object or None if type not supported
        """
        try:
            if mf_type == "trimf" and len(mf_params) >= 3:
                # Triangle MF: [a, b, c]
                a, b, c = mf_params[0], mf_params[1], mf_params[2]
                x_data = [var_range[0], a, b, c, var_range[1]]
                y_data = [0.0, 0, 1, 0, 0]
                central_x = b

                plot = TrianglePlot(
                    plot_widget=self.mf_plot_graph,
                    x_data=x_data,
                    y_data=y_data,
                    color=color,
                    central_x=central_x,
                )
                self._connect_plot_to_fuzzy_service(plot, mf_index, "trimf")
                return plot

            elif mf_type == "trapmf" and len(mf_params) >= 4:
                # Trapezoid MF: [a, b, c, d]
                a, b, c, d = mf_params[0], mf_params[1], mf_params[2], mf_params[3]
                x_data = [var_range[0], a, b, c, d, var_range[1]]
                y_data = [0.0, 0, 1, 1, 0, 0]
                central_x = (b + c) / 2

                plot = TrapezoidPlot(
                    plot_widget=self.mf_plot_graph,
                    x_data=x_data,
                    y_data=y_data,
                    color=color,
                    central_x=central_x,
                )
                self._connect_plot_to_fuzzy_service(plot, mf_index, "trapmf")
                return plot

            elif mf_type == "gaussmf" and len(mf_params) >= 2:
                # Gaussian MF: [sigma, mu]
                sigma, mu = mf_params[0], mf_params[1]
                x_data = np.linspace(var_range[0], var_range[1], 400)
                y_data = np.exp(-(1 / 2) * ((x_data - mu) / sigma) ** 2)

                plot = GaussPlot(
                    plot_widget=self.mf_plot_graph,
                    x_data=x_data,
                    y_data=y_data,
                    sigma_data=sigma,
                    mu_data=mu,
                    color=color,
                )
                self._connect_plot_to_fuzzy_service(plot, mf_index, "gaussmf")
                return plot

            elif mf_type == "gbellmf" and len(mf_params) >= 3:
                # Bell MF: [a, b, c]
                a, b, c = mf_params[0], mf_params[1], mf_params[2]
                x_data = np.linspace(var_range[0], var_range[1], 200)
                y_data = 1 / (1 + np.abs((x_data - c) / a) ** (2 * b))

                plot = BellPlot(
                    plot_widget=self.mf_plot_graph,
                    x_data=x_data,
                    y_data=y_data,
                    a_data=a,
                    b_data=b,
                    c_data=c,
                    color=color,
                )
                self._connect_plot_to_fuzzy_service(plot, mf_index, "gbellmf")
                return plot

        except Exception as e:
            print(f"Error creating MF plot: {e}")
            return None

        return None

    def _connect_plot_to_fuzzy_service(self, plot, mf_index, mf_type):
        """Connect plot anchor changes to update fuzzy service.

        Args:
            plot: The plot object
            mf_index: Index of the MF
            mf_type: Type of the MF
        """
        if mf_type == "trimf":
            if hasattr(plot, "triangle_left_anchor"):
                plot.triangle_left_anchor.sigPositionChangeFinished.connect(
                    lambda: self._on_triangle_anchor_changed(plot, mf_index)
                )
            if hasattr(plot, "triangle_central_anchor"):
                plot.triangle_central_anchor.sigPositionChangeFinished.connect(
                    lambda: self._on_triangle_anchor_changed(plot, mf_index)
                )
            if hasattr(plot, "triangle_right_anchor"):
                plot.triangle_right_anchor.sigPositionChangeFinished.connect(
                    lambda: self._on_triangle_anchor_changed(plot, mf_index)
                )
            if hasattr(plot, "position_anchor"):
                plot.position_anchor.sigPositionChangeFinished.connect(
                    lambda: self._on_triangle_anchor_changed(plot, mf_index)
                )
        elif mf_type == "trapmf":
            if hasattr(plot, "trapezoid_left_anchor"):
                plot.trapezoid_left_anchor.sigPositionChangeFinished.connect(
                    lambda: self._on_trapezoid_anchor_changed(plot, mf_index)
                )
            if hasattr(plot, "trapezoid_left_top_anchor"):
                plot.trapezoid_left_top_anchor.sigPositionChangeFinished.connect(
                    lambda: self._on_trapezoid_anchor_changed(plot, mf_index)
                )
            if hasattr(plot, "trapezoid_right_top_anchor"):
                plot.trapezoid_right_top_anchor.sigPositionChangeFinished.connect(
                    lambda: self._on_trapezoid_anchor_changed(plot, mf_index)
                )
            if hasattr(plot, "trapezoid_right_anchor"):
                plot.trapezoid_right_anchor.sigPositionChangeFinished.connect(
                    lambda: self._on_trapezoid_anchor_changed(plot, mf_index)
                )
            if hasattr(plot, "position_anchor"):
                plot.position_anchor.sigPositionChangeFinished.connect(
                    lambda: self._on_trapezoid_anchor_changed(plot, mf_index)
                )
        elif mf_type == "gaussmf":
            if hasattr(plot, "mu_anchor"):
                plot.mu_anchor.sigPositionChangeFinished.connect(lambda: self._on_gauss_anchor_changed(plot, mf_index))
            if hasattr(plot, "sigma_anchor"):
                plot.sigma_anchor.sigPositionChangeFinished.connect(
                    lambda: self._on_gauss_anchor_changed(plot, mf_index)
                )
            if hasattr(plot, "position_anchor"):
                plot.position_anchor.sigPositionChangeFinished.connect(
                    lambda: self._on_gauss_anchor_changed(plot, mf_index)
                )
        elif mf_type == "gbellmf":
            if hasattr(plot, "c_anchor"):
                plot.c_anchor.sigPositionChangeFinished.connect(lambda: self._on_bell_anchor_changed(plot, mf_index))
            if hasattr(plot, "a_anchor"):
                plot.a_anchor.sigPositionChangeFinished.connect(lambda: self._on_bell_anchor_changed(plot, mf_index))
            if hasattr(plot, "b_anchor"):
                plot.b_anchor.sigPositionChangeFinished.connect(lambda: self._on_bell_anchor_changed(plot, mf_index))
            if hasattr(plot, "position_anchor"):
                plot.position_anchor.sigPositionChangeFinished.connect(
                    lambda: self._on_bell_anchor_changed(plot, mf_index)
                )

    def _on_triangle_anchor_changed(self, plot, mf_index):
        """Handle triangle anchor position changes and update fuzzy service."""
        # Extract parameters from plot data: [a, b, c]
        # tri_x format: [range_min, a, b, c, range_max]
        if hasattr(plot, "tri_x") and len(plot.tri_x) >= 5:
            var_range = self._get_variable_range_for_mf(mf_index)
            if not var_range:
                return

            # Clamp values within range
            a = max(var_range[0], min(var_range[1], round(plot.tri_x[1], 2)))
            b = max(var_range[0], min(var_range[1], round(plot.tri_x[2], 2)))
            c = max(var_range[0], min(var_range[1], round(plot.tri_x[3], 2)))

            # Ensure proper ordering: a <= b <= c
            a = min(a, b)
            c = max(b, c)

            new_params = [a, b, c]
            self._update_mf_parameters(mf_index, new_params)

    def _on_trapezoid_anchor_changed(self, plot, mf_index):
        """Handle trapezoid anchor position changes and update fuzzy service."""
        # Extract parameters from plot data: [a, b, c, d]
        # trap_x format: [range_min, a, b, c, d, range_max]
        if hasattr(plot, "trap_x") and len(plot.trap_x) >= 6:
            var_range = self._get_variable_range_for_mf(mf_index)
            if not var_range:
                return

            # Clamp values within range
            a = max(var_range[0], min(var_range[1], round(plot.trap_x[1], 2)))
            b = max(var_range[0], min(var_range[1], round(plot.trap_x[2], 2)))
            c = max(var_range[0], min(var_range[1], round(plot.trap_x[3], 2)))
            d = max(var_range[0], min(var_range[1], round(plot.trap_x[4], 2)))

            # Ensure proper ordering: a <= b <= c <= d
            a = min(a, b)
            b = min(b, c)
            c = max(b, c)
            d = max(c, d)

            new_params = [a, b, c, d]
            self._update_mf_parameters(mf_index, new_params)

    def _on_gauss_anchor_changed(self, plot, mf_index):
        """Handle Gaussian anchor position changes and update fuzzy service."""
        # Extract parameters: [sigma, mu]
        if hasattr(plot, "sigma_data") and hasattr(plot, "mu_data"):
            var_range = self._get_variable_range_for_mf(mf_index)
            if not var_range:
                return

            # Clamp mu within range (sigma can be any positive value)
            sigma = max(0.01, round(plot.sigma_data, 2))  # Ensure sigma is positive
            mu = max(var_range[0], min(var_range[1], round(plot.mu_data, 2)))

            new_params = [sigma, mu]
            self._update_mf_parameters(mf_index, new_params)

    def _on_bell_anchor_changed(self, plot, mf_index):
        """Handle Bell anchor position changes and update fuzzy service."""
        # Extract parameters: [a, b, c]
        if hasattr(plot, "a_data") and hasattr(plot, "b_data") and hasattr(plot, "c_data"):
            var_range = self._get_variable_range_for_mf(mf_index)
            if not var_range:
                return

            # Clamp c (center) within range, a and b are shape parameters (positive)
            a = max(0.01, round(plot.a_data, 2))  # Ensure a is positive
            b = max(0.01, round(plot.b_data, 2))  # Ensure b is positive
            c = max(var_range[0], min(var_range[1], round(plot.c_data, 2)))

            new_params = [a, b, c]
            self._update_mf_parameters(mf_index, new_params)

    def _get_variable_range_for_mf(self, mf_index):
        """Get the variable range for a specific MF by its index.

        Args:
            mf_index: Index of the MF

        Returns:
            List [min, max] or None if not found
        """
        for mf_plot_info in self.mf_plots:
            if mf_plot_info.get("mf_index") == mf_index:
                return mf_plot_info.get("var_range")
        return None

    def _update_mf_parameters(self, mf_index, new_params):
        """Update MF parameters in fuzzy service.

        Args:
            mf_index: Index of the MF to update
            new_params: New parameters for the MF
        """
        fuzzy_service = self.view_model.fuzzy_service if hasattr(self.view_model, "fuzzy_service") else None
        if not fuzzy_service:
            return

        # Determine which variable (input or output) is selected
        selected_input_name = fuzzy_service.get_selected_input_name()
        selected_output_name = fuzzy_service.get_selected_output_name()

        variable_name = None
        variable_type = None

        if selected_input_name:
            variable_name = selected_input_name
            variable_type = "input"
        elif selected_output_name:
            variable_name = selected_output_name
            variable_type = "output"
        else:
            return

        success = fuzzy_service.update_membership_function_parameters(
            variable_name, mf_index, new_params, variable_type
        )

        if success:
            # Optionally show status message
            if hasattr(self, "status_bar") and self.status_bar:
                self.status_bar.showMessage(f"Updated MF parameters: {new_params}")

            if hasattr(self.view_model, "notify_data_changed"):
                self.view_model.notify_data_changed.emit()

    def _clear_mf_plots(self):
        """Clear all existing MF plots from the graph."""
        for mf_plot_info in self.mf_plots:
            plot_obj = mf_plot_info.get("plot")
            if plot_obj:
                if hasattr(plot_obj, "plot_widget"):
                    plot_obj.plot_widget.clear()

        self.mf_plots = []

    def _setup_sample_data(self):
        """Set up sample data for the widget."""
        # This method will be implemented when needed
        # For now, it's a placeholder to prevent AttributeError
        pass

    def get_fuzzy_service(self):
        """Get the fuzzy calculation service."""
        # This method will be implemented when fuzzy service is connected
        # For now, return None to prevent AttributeError
        return None

    def connect_mf_editor(self, mf_editor):
        """Connect the MF editor to this widget."""
        # This method will be implemented when MF editor integration is needed
        # For now, it's a placeholder to prevent AttributeError
        pass
