from PyQt6 import QtCore, QtWidgets

from app.views.base_frame_view import BaseFrameView
from app.views.in_output import InOutput
from app.views.mf import MembershipFunction
from app.views.rule import Rule


def populate_inoutputs(data_inoutputs, tree_parent):
    """Populate tree widget with input/output data.

    Args:
        data_inoutputs: List of input/output objects.
        tree_parent: Parent tree widget item.
    """
    for inout in data_inoutputs:
        tree_child_inp = QtWidgets.QTreeWidgetItem([inout.GetName()])
        mfs = inout.GetMfs()
        for mf in mfs:
            mf_child_inp = QtWidgets.QTreeWidgetItem(["MF"])
            tree_child_inp.addChild(mf_child_inp)
        tree_parent.addChild(tree_child_inp)


class BrowserFrameWidget(BaseFrameView):
    """Class responsible for displaying the system browser.

    Displays the system browser in the left window of the program.
    """

    mf1 = MembershipFunction(1, 1)
    mf2 = MembershipFunction(2, 2)
    mfs = [mf1, mf2]
    inoutput = InOutput(name="Input 1", mfs=mfs)
    inoutputs = [inoutput]
    rule1 = Rule(
        "Input1",
        "MF1",
        "1",
        "Input2",
        "MF2",
        "2",
        "Output",
        "MF3",
        "if",
        "1",
        "and",
        "1",
        "Rule 1",
    )
    rule2 = Rule(
        "Input1",
        "MF1",
        "3",
        "Input2",
        "MF2",
        "1",
        "Output",
        "MF3",
        "2",
        "if",
        "and",
        "1",
        "Rule 2",
    )
    rules = [rule1, rule2]

    del_inputs = QtCore.pyqtSignal()
    del_outputs = QtCore.pyqtSignal()

    def __init__(self, parent=None, status_bar=None):
        """Initialize the browser frame widget.

        Args:
            parent: Parent widget
            status_bar: Status bar widget
        """
        super().__init__(parent=parent)
        self.setObjectName("browserFrane")
        self.status_bar = status_bar
        self._setup_ui()
        self._retranslate_ui()

    def _setup_ui(self):
        self.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.setObjectName("browserFrame")

        # Create main layout
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # Design browser label
        self.design_browser_label = QtWidgets.QLabel()
        self.design_browser_label.setObjectName("design_browser_label")
        main_layout.addWidget(self.design_browser_label)

        # System browser label
        self.system_browser_label = QtWidgets.QLabel()
        self.system_browser_label.setObjectName("system_browser_label")
        main_layout.addWidget(self.system_browser_label)

        # Tree view
        self.system_browser_tree_view = QtWidgets.QTreeView()
        self.system_browser_tree_view.setObjectName("system_browser_tree_view")

        self.tree = QtWidgets.QTreeWidget()
        self.tree.setHeaderHidden(True)
        self.tree.itemSelectionChanged.connect(self.selection_changed)

        # Add tree items
        self.tree_data_input = QtWidgets.QTreeWidgetItem(["Inputs"])
        self.tree.insertTopLevelItem(0, self.tree_data_input)
        populate_inoutputs(data_inoutputs=self.inoutputs, tree_parent=self.tree_data_input)

        self.tree_data_output = QtWidgets.QTreeWidgetItem(["Outputs"])
        self.tree.insertTopLevelItem(1, self.tree_data_output)
        populate_inoutputs(data_inoutputs=self.inoutputs, tree_parent=self.tree_data_output)

        self.tree_data_rules = QtWidgets.QTreeWidgetItem(["Rules"])
        self.tree.insertTopLevelItem(2, self.tree_data_rules)
        self.populate_rules(self.rules)

        # Add tree to layout
        main_layout.addWidget(self.tree)

        # Button layout
        button_layout = QtWidgets.QHBoxLayout()

        self.delete_all_inputs_button = QtWidgets.QPushButton()
        self.delete_all_inputs_button.setObjectName("del_inputs_buttons")
        self.delete_all_inputs_button.clicked.connect(self.clear_inputs)
        button_layout.addWidget(self.delete_all_inputs_button)

        self.delete_all_outputs_button = QtWidgets.QPushButton()
        self.delete_all_outputs_button.setObjectName("del_outputs_buttons")
        self.delete_all_outputs_button.clicked.connect(self.clear_outputs)
        button_layout.addWidget(self.delete_all_outputs_button)

        main_layout.addLayout(button_layout)

    def _retranslate_ui(self):
        self.system_browser_label.setText(self.t("SYSTEM_BROWSER"))
        self.delete_all_inputs_button.setText(self.t("CLEAR_INPUTS"))
        self.delete_all_outputs_button.setText(self.t("CLEAR_OUTPUTS"))
        self.design_browser_label.setText(self.t("DESIGN_BROWSER"))

    def populate_rules(self, rules):
        """Populate tree widget with rules.

        Args:
            rules: List of rule objects.
        """
        for rule in rules:
            rule_child = QtWidgets.QTreeWidgetItem([rule.getName()])
            self.tree_data_rules.addChild(rule_child)

    def selection_changed(self):
        """Handle selection change in the tree widget."""
        items = self.tree.selectedItems()
        if len(items) != 0:
            self.status_bar.showMessage(f"Last action: selected item {items[0].text(0)}")

    def clear_inputs(self):
        """Clear all inputs from the tree widget."""
        for i in range(self.tree_data_input.childCount()):
            self.tree_data_input.removeChild(self.tree_data_input.child(0))
        self.del_inputs.emit()

    def clear_outputs(self):
        """Clear all outputs from the tree widget."""
        for i in range(self.tree_data_output.childCount()):
            self.tree_data_output.removeChild(self.tree_data_output.child(0))
        self.del_outputs.emit()
