"""Create the central GUI window at the center of the application.

Classes:
    CentralTabWidget: central window of the application displaying all the most
        important information about the system. Inherits from QTabWidget.
"""

import pyqtgraph as pg
from PyQt6 import QtCore, QtWidgets

from app.view_models.base_view_model import BaseViewModel
from app.views.base_tab_view import BaseTabView


class CentralTabWidget(BaseTabView):
    """Class inheriting from QTabWidget.

    Allows user interaction via QPushButton GUI elements.

    Displays four tabs with information about different aspects of the system:
        Fis plot: tab responsible for displaying the plots of all the inputs and
            outputs in the system.
        MF plot: tab responsible for displaying individual input or output and
            interaction with the membership functions.
        Rule editor: tab responsible for adding and deleting rules from the system
            and displaying them in a table.
        Interference tab: tab responsible for showing the user the end result of
            rule interference.

    Methods:
        __init__(view_model, parent): create an instance of CentralTabWidget
            and bind it to the parent window.

    Attributes:
        clear_rules_clicked: pyqtSignal which gets emitted to back end when
            clear_rules_button is clicked.
        rules: a list of all the rules in the system.
    """

    clear_rules_clicked = QtCore.pyqtSignal()
    rules = []
    view_model: BaseViewModel

    def __init__(self, view_model: BaseViewModel, parent=None):
        """Initialize a new class instance.

        Args:
            view_model (BaseViewModel): The view model for the central tab
                widget.
            parent (QWidget, optional): The parent widget, in this case main
                window, to which the widget will be attached. Defaults to None.
        """
        super().__init__(parent=parent)
        self._view_model = view_model
        self._plotting = False
        self.setObjectName("centralTab")
        self._setup_ui()
        self._retranslate_ui()

    def _setup_ui(self):
        """Set up all the GUI sub elements."""
        # Use shared fuzzy service from context
        if hasattr(self, "context") and self.context:
            self.fuzzy_service = self.context.fuzzy_service
        else:
            # Fallback: create a new service if no context is available
            from app.services.fuzzy_calculation_service import FuzzyCalculationService

            self.fuzzy_service = FuzzyCalculationService("mamdani")

        self._view_model.set_fuzzy_service(self.fuzzy_service)

        self.fis_plot = QtWidgets.QWidget()
        self.fis_plot.setObjectName("fis_plot")

        self.graph_frame = QtWidgets.QFrame(parent=self.fis_plot)
        self.graph_frame.setGeometry(QtCore.QRect(-1, 49, 461, 471))
        self.graph_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.graph_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.graph_frame.setObjectName("graph_frame")

        self.fis_graph_widget = pg.PlotWidget(parent=self.graph_frame)
        self.fis_graph_widget.setGeometry(QtCore.QRect(5, 5, 451, 461))
        self.fis_graph_widget.setLabel("left", "Value")
        self.fis_graph_widget.setLabel("bottom", "Input")
        self.fis_graph_widget.setTitle("FIS Plot")
        self.fis_graph_widget.showGrid(x=True, y=True)
        self.fis_graph_widget.setBackground("w")

        self.addTab(self.fis_plot, "")

        self.mf_plot = QtWidgets.QWidget()
        self.mf_plot.setObjectName("mf_plot")

        self.plot_frame = QtWidgets.QFrame(parent=self.mf_plot)
        self.plot_frame.setGeometry(QtCore.QRect(0, 60, 531, 551))
        self.plot_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.plot_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.plot_frame.setObjectName("plot_frame")

        self.mf_graph_widget = pg.PlotWidget(parent=self.plot_frame)
        self.mf_graph_widget.setGeometry(QtCore.QRect(5, 5, 521, 541))
        self.mf_graph_widget.setLabel("left", "Membership Degree")
        self.mf_graph_widget.setLabel("bottom", "Value")
        self.mf_graph_widget.setTitle("Membership Functions")
        self.mf_graph_widget.showGrid(x=True, y=True)
        self.mf_graph_widget.setBackground("w")

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
        self.clear_rules_button.clicked.connect(self._clear_rules)

        self.seperator_line_2 = QtWidgets.QFrame(parent=self.rule_editor)
        self.seperator_line_2.setGeometry(QtCore.QRect(0, 20, 501, 31))
        self.seperator_line_2.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.seperator_line_2.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.seperator_line_2.setObjectName("seperator_line_2")

        self.system_label_2 = QtWidgets.QLabel(parent=self.rule_editor)
        self.system_label_2.setGeometry(QtCore.QRect(0, 10, 211, 16))
        self.system_label_2.setObjectName("system_label_2")

        self.addTab(self.rule_editor, "")

    def _retranslate_ui(self):
        """Add text to all the respective GUI elements."""
        self.setWhatsThis("<html><head/><body><p><br/></p><p><br/></p></body></html>")
        self.setTabText(self.indexOf(self.fis_plot), self.t("FIS Plot"))
        self.system_name_label.setText(self.t("System: Placeholder Name"))
        self.clear_rules_button.setText(self.t("Clear Rules"))
        self.setTabText(self.indexOf(self.mf_plot), self.t("MF Editor"))
        self.setTabText(self.indexOf(self.rule_editor), self.t("Rule Editor"))

    def _clear_rules(self):
        """Clear all the rules from the system. Emit a signal to the backend."""
        self.table_widget.clear()
        self.table_widget.setHorizontalHeaderLabels(["Rule", "Weight", "Name"])
        self.table_widget.setRowCount(1)
        self.table_widget.setColumnCount(3)
        self.rules = []
        self.clear_rules_clicked.emit()

    def _connect_view_model_signals(self):
        """Connect view model signals to UI update methods."""
        self._view_model.membership_functions_data_ready.connect(
            self._on_membership_functions_data_ready
        )
        self._view_model.fis_plot_data_ready.connect(self._on_fis_plot_data_ready)
        self._view_model.inference_data_ready.connect(self._on_inference_data_ready)
        self._view_model.system_name_changed.connect(self._on_system_name_changed)

    def _setup_sample_data(self):
        """Set up sample data for demonstration."""
        self.fuzzy_service.add_membership_function(
            "Input1", "low", "trojkatna", [0, 2, 4]
        )
        self.fuzzy_service.add_membership_function(
            "Input1", "high", "trojkatna", [6, 8, 10]
        )
        self.fuzzy_service.add_membership_function(
            "Output1", "low", "trojkatna", [0, 2, 4]
        )
        self.fuzzy_service.add_membership_function(
            "Output1", "high", "trojkatna", [6, 8, 10]
        )
        self.fuzzy_service.add_rule([1, 1], [1, 1, 1, 1])
        self._view_model._update_membership_functions_plot()

    def _on_membership_functions_data_ready(
        self, variable_name, x_data, y_data_list, colors
    ):
        """Handle membership functions plot data from view model."""
        if self._plotting:
            return
        self._plotting = True
        try:
            self.mf_graph_widget.clear()

            if not y_data_list:
                return

            import numpy as np

            x = np.array(x_data)

            for i, y_data in enumerate(y_data_list):
                color = colors[i % len(colors)]
                y = np.array(y_data)
                self.mf_graph_widget.plot(x, y, pen=pg.mkPen(color, width=2))

            self.mf_graph_widget.setXRange(x.min(), x.max())
            self.mf_graph_widget.setYRange(0, 1.1)
            self.mf_graph_widget.setTitle(f"Membership Functions: {variable_name}")
        finally:
            self._plotting = False

    def _on_fis_plot_data_ready(self, x_data, y_data):
        """Handle FIS plot data from view model."""
        self.fis_graph_widget.clear()

        if x_data and y_data:
            import numpy as np

            x = np.array(x_data)
            y = np.array(y_data)
            self.fis_graph_widget.plot(x, y, pen=pg.mkPen("b", width=2))

    def _on_inference_data_ready(self, inputs, outputs):
        """Handle inference results data from view model."""
        if inputs and outputs:
            self.fis_graph_widget.plot(
                inputs, outputs, pen=pg.mkPen("r", width=2), symbol="o", symbolSize=8
            )

    def _on_system_name_changed(self, system_name):
        """Handle system name changes from view model."""
        self.system_name_label.setText(system_name)

    def get_fuzzy_service(self):
        """Get the fuzzy calculation service."""
        return self.fuzzy_service

    def connect_mf_editor(self, mf_editor):
        """Connect the MF Editor to update the plot when properties change.

        Args:
            mf_editor: The MF Editor widget to connect
        """
        self._view_model.connect_mf_editor(mf_editor)

    def refresh_ui(self) -> None:
        """Refresh the UI elements."""
        # Only refresh if we have a valid view model
        if hasattr(self, "_view_model") and self._view_model:
            self._view_model._update_membership_functions_plot()

    def update_ui(self) -> None:
        """Update UI elements."""
        pass

    def handle_global_update(self) -> None:
        """Handle global update request."""
        # Don't trigger global updates from global updates to avoid circular calls
        pass
