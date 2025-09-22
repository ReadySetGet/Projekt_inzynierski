from PyQt6 import QtCore, QtGui, QtWidgets
from app.views.in_output import InOutput
from app.views.rule import Rule
from app.views.mf import MembershipFunction


class BrowserFrameWidget(QtWidgets.QFrame):
    """Class responsible for displaying the system browser in the left window of the program."""
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

    def __init__(self, parent=None, status_bar=None):
        super().__init__(parent)
        self.setObjectName("browserFrane")
        self.status_bar = status_bar
        self._setup_ui()
        self._retranslate_ui()

    def _setup_ui(self):
        self.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.setObjectName("browserFrame")

        self.system_browser_tree_view = QtWidgets.QTreeView(parent=self)
        self.system_browser_tree_view.setGeometry(QtCore.QRect(0, 300, 301, 295))
        self.system_browser_tree_view.setObjectName("system_browser_tree_view")

        self.tree = QtWidgets.QTreeWidget(parent=self.system_browser_tree_view)
        self.tree.resize(301, 295)
        self.tree.setHeaderHidden(True)

        self.tree.itemSelectionChanged.connect(self.selection_changed)

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
        _translate = QtCore.QCoreApplication.translate
        self.system_browser_label.setText(_translate("MainWindow", "SYSTEM BROWSER"))
        self.design_browser_label.setText(_translate("MainWindow", "DESIGN BROWSER"))

    def populate_inoutputs(self, data_inoutputs, tree_parent):
        for inout in data_inoutputs:
            tree_child_inp = QtWidgets.QTreeWidgetItem([inout.GetName()])
            mfs = inout.GetMfs()
            for mf in mfs:
                mf_child_inp = QtWidgets.QTreeWidgetItem(['MF'])
                tree_child_inp.addChild(mf_child_inp)
            tree_parent.addChild(tree_child_inp)

    def populate_rules(self, rules):
        for rule in rules:
            rule_child = QtWidgets.QTreeWidgetItem([rule.getName()])
            self.tree_data_rules.addChild(rule_child)

    def selection_changed(self):
        items = self.tree.selectedItems()
        self.status_bar.showMessage(f"Last action: selected item {items[0].text(0)}")
