from PyQt6 import QtCore, QtWidgets

from app.views.base_frame_view import BaseFrameView


class BrowserFrameWidget(BaseFrameView):
    """Class responsible for displaying the system browser.

    Displays the system browser in the left window of the program.
    """

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
        self._system_items = []
        self._design_items = []
        self._input_item_map = {}
        self._output_item_map = {}
        self._setup_ui()
        self._retranslate_ui()

    def set_view_model(self, view_model) -> None:
        """Set the view model and subscribe to its signals."""
        super().set_view_model(view_model)
        if not view_model:
            return

        view_model.system_browser_updated.connect(self._populate_system_items)
        view_model.design_browser_updated.connect(self._populate_design_items)
        view_model.system_item_selected.connect(self._on_system_item_selected)
        view_model.design_item_selected.connect(self._on_design_item_selected)

        view_model.refresh_browser()

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
        self.tree_data_output = QtWidgets.QTreeWidgetItem(["Outputs"])
        self.tree.insertTopLevelItem(1, self.tree_data_output)

        self.tree_data_rules = QtWidgets.QTreeWidgetItem(["Rules"])
        self.tree.insertTopLevelItem(2, self.tree_data_rules)

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

    def selection_changed(self):
        """Handle selection change in the tree widget."""
        items = self.tree.selectedItems()
        if len(items) != 0:
            item = items[0]
            payload = item.data(0, QtCore.Qt.ItemDataRole.UserRole)
            if isinstance(payload, dict):
                category = payload.get("category")
                name = payload.get("name", item.text(0))
                data = payload.get("data", {})
                if self.view_model:
                    if category == "system":
                        self.view_model.select_system_item(name, data)
                    elif category == "design":
                        self.view_model.select_design_item(name, data)
            self.status_bar.showMessage(f"Last action: selected item {item.text(0)}")

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

    def _populate_system_items(self, items: list) -> None:
        """Populate tree with system-level items."""
        self._system_items = items or []
        self._input_item_map = {}
        self._output_item_map = {}
        self._clear_children(self.tree_data_input)
        self._clear_children(self.tree_data_output)
        self._clear_children(self.tree_data_rules)

        for entry in self._system_items:
            item_type = entry.get("type")
            name = entry.get("name", "")
            tree_item = QtWidgets.QTreeWidgetItem([name])
            tree_item.setData(
                0,
                QtCore.Qt.ItemDataRole.UserRole,
                {"category": "system", "name": name, "data": entry},
            )

            if item_type == "input":
                self.tree_data_input.addChild(tree_item)
                self._input_item_map[name] = tree_item
            elif item_type == "output":
                self.tree_data_output.addChild(tree_item)
                self._output_item_map[name] = tree_item
            elif item_type == "rule":
                self.tree_data_rules.addChild(tree_item)

        self.tree.expandAll()

    def _populate_design_items(self, items: list) -> None:
        """Populate tree with design items (membership functions)."""
        self._design_items = items or []

        for parent in self._input_item_map.values():
            self._clear_children(parent)
        for parent in self._output_item_map.values():
            self._clear_children(parent)

        for entry in self._design_items:
            item_type = entry.get("type")
            name = entry.get("name", "")
            variable_name = entry.get("variable_name", "")
            parent_item = None

            if item_type == "input_mf":
                parent_item = self._input_item_map.get(variable_name)
            elif item_type == "output_mf":
                parent_item = self._output_item_map.get(variable_name)

            if not parent_item:
                continue

            display_name = name
            tree_item = QtWidgets.QTreeWidgetItem([display_name])
            tree_item.setData(
                0,
                QtCore.Qt.ItemDataRole.UserRole,
                {"category": "design", "name": name, "data": entry},
            )
            parent_item.addChild(tree_item)

        self.tree.expandAll()

    def _clear_children(self, parent_item: QtWidgets.QTreeWidgetItem) -> None:
        """Remove all children from the given tree item."""
        while parent_item.childCount():
            child = parent_item.child(0)
            parent_item.removeChild(child)
            del child

    def _on_system_item_selected(self, item_name: str, item_data: dict) -> None:
        """Highlight a system item based on view-model selection."""
        self._select_item_by_name(self.tree_data_input, item_name)
        self._select_item_by_name(self.tree_data_output, item_name)
        self._select_item_by_name(self.tree_data_rules, item_name)

    def _on_design_item_selected(self, item_name: str, item_data: dict) -> None:
        """Highlight a design item based on view-model selection."""
        if not isinstance(item_data, dict):
            return

        variable_name = item_data.get("variable_name")
        item_type = item_data.get("type")

        parent_item = None
        if item_type == "input_mf":
            parent_item = self._input_item_map.get(variable_name)
        elif item_type == "output_mf":
            parent_item = self._output_item_map.get(variable_name)

        if parent_item:
            child = self._find_child_by_name(parent_item, item_name)
            if child:
                self.tree.setCurrentItem(child)

    def _find_child_by_name(
        self, parent_item: QtWidgets.QTreeWidgetItem, name: str
    ) -> QtWidgets.QTreeWidgetItem | None:
        """Return the first direct child whose label matches the given name."""
        for i in range(parent_item.childCount()):
            child = parent_item.child(i)
            if child.text(0) == name:
                return child
        return None

    def _select_item_by_name(self, parent_item: QtWidgets.QTreeWidgetItem, name: str) -> bool:
        """Select the first child whose label contains the provided name."""
        for i in range(parent_item.childCount()):
            child = parent_item.child(i)
            text = child.text(0)
            if name in text:
                self.tree.setCurrentItem(child)
                return True
            if self._select_item_by_name(child, name):
                return True
        return False
