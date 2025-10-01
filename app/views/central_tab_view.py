"""Create the central GUI window at the center of the application.

Classes:
    CentralTabWidget: central window of the application displaying all the most
        important information about the system. Inherits from QTabWidget.
"""

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
        self.setObjectName("centralTab")
        self._setup_ui()
        self._retranslate_ui()

    def _setup_ui(self):
        """Set up all the GUI sub elements."""
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
        self.plot_frame.setGeometry(QtCore.QRect(0, 60, 531, 551))
        self.plot_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.plot_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.plot_frame.setObjectName("plot_frame")

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
