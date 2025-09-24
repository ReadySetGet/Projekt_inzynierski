"""Create the central GUI window at the center of the application.

    Classes:
        CentralTabWidget: central window of the application displaying all the most important information about the system.
            Inherits from QTabWidget.
"""
from PyQt6 import QtCore, QtGui, QtWidgets
from app.views.rule import Rule


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
                set_rules(list[Rule]): set a new list of rules in the system.

            Attributes:
                fill_table_clicked: pyqtSignal which gets emitted when add_all_rules_button is clicked
                rules: list of rules present in the system
    """
    fill_table_clicked = QtCore.pyqtSignal()
    rules = []

    def __init__(self, parent=None):
        """Initialize a new class instance.

            Parameters:
                parent: The parent widget, in this case main window, to which the widget will be attached.
        """
        super().__init__(parent)
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

        rule1 = Rule("In1", "Mf1", "In2", "Mf2", "Out",
                     "Mf3", "is", "and", "1", "Rule 1")
        rule2 = Rule("In1", "Mf1", "In2", "Mf2", "Out",
                     "Mf3", "is", "and", "1", "Rule 2")
        rule3 = Rule("In1", "Mf1", "In2", "Mf2", "Out",
                     "Mf3", "is", "and", "1", "Rule 3")
        self.rules.append(rule1)
        self.rules.append(rule2)
        self.rules.append(rule3)

        self.add_all_rules_button = QtWidgets.QPushButton(parent=self.rule_editor)
        self.add_all_rules_button.setGeometry(QtCore.QRect(20, 60, 140, 28))
        self.add_all_rules_button.setObjectName("add_all_rules")
        self.add_all_rules_button.clicked.connect(self._fill_table)

        self.addTab(self.rule_editor, "")

    def _retranslate_ui(self):
        """Add text to all the respective GUI elements."""
        _translate = QtCore.QCoreApplication.translate
        self.setWhatsThis(_translate("MainWindow", "<html><head/><body><p><br/></p><p><br/></p></body></html>"))
        self.setTabText(self.indexOf(self.fis_plot), _translate("MainWindow", "FIS Plot"))
        self.system_name_label.setText(_translate("MainWindow", "System: Placeholder Name"))
        self.setTabText(self.indexOf(self.mf_plot), _translate("MainWindow", "MF Editor"))
        self.setTabText(self.indexOf(self.rule_editor), _translate("MainWindow", "Rule Editor"))
        self.add_all_rules_button.setText(_translate("MainWindow", "Add All Possible Rules"))

    def _fill_table(self):
        """Fill the table with all the rules, emit the signal."""
        self.fill_table_clicked.emit()
        rule_numb = len(self.rules)
        self.table_widget.setRowCount(rule_numb)
        for i in range(rule_numb):
            self.table_widget.setItem(i, 0, QtWidgets.QTableWidgetItem(self.rules[i].getRule()))
            self.table_widget.setItem(i, 1, QtWidgets.QTableWidgetItem(self.rules[i].getWeight()))
            self.table_widget.setItem(i, 2, QtWidgets.QTableWidgetItem(self.rules[i].getName()))

    def set_rules(self, rules):
        """Set new rules for the system."""
        self.rules = rules
