"""Create the browser GUI window at the left of the application.

    Classes:
        BrowserFrameWidget: left window of the application displaying all the present inputs, outputs and rules in the
            system as well as their hierarchy. Inherits from QFrame.
"""
from PyQt6 import QtCore, QtGui, QtWidgets
from app.views.in_output import InOutput
from app.views.rule import Rule
from app.views.mf import MembershipFunction


class BrowserFrameWidget(QtWidgets.QFrame):
    """Class inheriting from QFrame.
        Displays the information about the fis system via hierarchical QTreeView widget. Allows user interaction
        via QTreeWidgetItems elements.

            Methods:
                __init__(QtWidget.*): create an instance of BrowserFrameWidget and bind it to the parent widget.

            Attributes:
                selected_item: pyqtSignal which gets emitted to the backend whenever the user selects a new item
                placeholder attributes for testing purposes
    """
    selected_item = QtCore.pyqtSignal()

    #Placeholders
    mf1 = MembershipFunction(1, 1)
    mf2 = MembershipFunction(2, 2)
    mfs = [mf1, mf2]
    inoutput = InOutput(name="Input 1", mfs=mfs)
    inoutputs = [inoutput]
    rule1 = Rule("Input1", "MF1", "Input2", "MF2", "Output", "MF3",
                 "if", "and", "1", "Rule 1")
    rule2 = Rule("Input1", "MF1", "Input2", "MF2", "Output", "MF3",
                 "if", "and", "1", "Rule 2")
    rules = [rule1, rule2]

    def __init__(self, parent=None):
        """Initialize a new class instance.

            Parameters:
                parent: The parent QtWidget, in this case centralwidget, to which the widget will be attached.
        """
        super().__init__(parent)
        self.setObjectName("browserFrane")
        self._setup_ui()
        self._retranslate_ui()

    def _setup_ui(self):
        """Set up all the GUI sub elements."""
        self.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.setObjectName("browserFrame")

        self.system_browser_tree_view = QtWidgets.QTreeView(parent=self)
        self.system_browser_tree_view.setGeometry(QtCore.QRect(0, 300, 301, 295))
        self.system_browser_tree_view.setObjectName("system_browser_tree_view")

        self.tree = QtWidgets.QTreeWidget(parent=self.system_browser_tree_view)
        self.tree.resize(301, 295)
        self.tree.setHeaderHidden(True)

        self.tree.itemSelectionChanged.connect(self._selection_changed)

        self.tree_data_input = QtWidgets.QTreeWidgetItem(["Inputs"])
        self.tree.insertTopLevelItem(0, self.tree_data_input)
        self.populate_inoutputs(data_inoutputs=self.inoutputs, tree_parent=self.tree_data_input)

        self.tree_data_output = QtWidgets.QTreeWidgetItem(["Outputs"])
        self.tree.insertTopLevelItem(1, self.tree_data_output)
        self.populate_inoutputs(data_inoutputs=self.inoutputs, tree_parent=self.tree_data_output)

        self.tree_data_rules = QtWidgets.QTreeWidgetItem(["Rules"])
        self.tree.insertTopLevelItem(2, self.tree_data_rules)
        self.populate_rules(self.rules)

        self.system_browser_label = QtWidgets.QLabel(parent=self)
        self.system_browser_label.setGeometry(QtCore.QRect(4, 274, 281, 21))
        self.system_browser_label.setObjectName("system_browser_label")

        self.design_browser_label = QtWidgets.QLabel(parent=self)
        self.design_browser_label.setGeometry(QtCore.QRect(10, 10, 111, 16))
        self.design_browser_label.setObjectName("design_browser_label")

    def _retranslate_ui(self):
        """Add text to all the respective GUI elements."""
        _translate = QtCore.QCoreApplication.translate
        self.system_browser_label.setText(_translate("MainWindow", "SYSTEM BROWSER"))
        self.design_browser_label.setText(_translate("MainWindow", "DESIGN BROWSER"))

    def populate_inoutputs(self, data_inoutputs, tree_parent) -> None:
        """
        Function which populates the inputs and outputs portion of the system browser.
        :param data_inoutputs: list[in_output] the list of all the inputs or outputs in the system which will be
            displayed on the tree view as QTreeItemWidgets
        :param tree_parent: QTreeWidget to which the QTreeItemWidgets will get attached depending on whether they
            are inputs or outputs
        :return: None
        """
        for inout in data_inoutputs:
            tree_child_inp = QtWidgets.QTreeWidgetItem([inout.GetName()])
            mem_funcs = inout.GetMfs()
            for mf in mem_funcs:
                mf_child_inp = QtWidgets.QTreeWidgetItem(['MF'])
                tree_child_inp.addChild(mf_child_inp)
            tree_parent.addChild(tree_child_inp)

    def populate_rules(self, rules) -> None:
        """
        Populate the rules portion of the system browser
        :param rules: list[rule] list of rules present in the system
        :return: None
        """
        for rule in rules:
            rule_child = QtWidgets.QTreeWidgetItem([rule.getName()])
            self.tree_data_rules.addChild(rule_child)

    def _selection_changed(self) -> None:
        """Emit a signal to the backend that selected item has changed."""
        items = self.tree.selectedItems()
        self.selected_item.emit()
