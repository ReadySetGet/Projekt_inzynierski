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
        view_model.design_projects_updated.connect(self._populate_design_projects)
        view_model.project_switched.connect(self._on_project_switched)

        view_model.refresh_browser()
        view_model.refresh_projects()

        from PyQt6.QtCore import QTimer

        QTimer.singleShot(100, view_model.load_default_project_if_empty)

    def _setup_ui(self):
        """Set up all the GUI sub elements."""
        self.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)

        # Create main layout
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # Design browser label
        self.design_browser_label = QtWidgets.QLabel()
        self.design_browser_label.setObjectName("design_browser_label")
        main_layout.addWidget(self.design_browser_label)

        # Design Browser buttons
        design_buttons_layout = QtWidgets.QHBoxLayout()
        design_buttons_layout.setSpacing(5)

        self.set_active_design_button = QtWidgets.QPushButton()
        self.set_active_design_button.setObjectName("set_active_design_button")
        self.set_active_design_button.clicked.connect(self._set_active_design)
        design_buttons_layout.addWidget(self.set_active_design_button)

        self.duplicate_design_button = QtWidgets.QPushButton()
        self.duplicate_design_button.setObjectName("duplicate_design_button")
        self.duplicate_design_button.clicked.connect(self._duplicate_design)
        design_buttons_layout.addWidget(self.duplicate_design_button)

        self.delete_design_button = QtWidgets.QPushButton()
        self.delete_design_button.setObjectName("delete_design_button")
        self.delete_design_button.clicked.connect(self._delete_design)
        design_buttons_layout.addWidget(self.delete_design_button)

        design_buttons_layout.addStretch()
        main_layout.addLayout(design_buttons_layout)

        # Design Browser table (for projects)
        self.design_table = QtWidgets.QTableWidget()
        self.design_table.setColumnCount(3)
        self.design_table.setHorizontalHeaderLabels([self.t("ACTIVE"), self.t("DESIGN"), self.t("TYPE")])
        self.design_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.design_table.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        self.design_table.setMinimumHeight(150)
        self.design_table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.design_table.itemDoubleClicked.connect(self._on_design_table_double_clicked)
        self.design_table.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.design_table.customContextMenuRequested.connect(self._show_design_context_menu)
        main_layout.addWidget(self.design_table)

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
        self.tree.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self._show_context_menu)

        # Add tree items (will be translated in _retranslate_ui)
        self.tree_data_input = QtWidgets.QTreeWidgetItem()
        self.tree.insertTopLevelItem(0, self.tree_data_input)
        self.tree_data_output = QtWidgets.QTreeWidgetItem()
        self.tree.insertTopLevelItem(1, self.tree_data_output)

        self.tree_data_rules = QtWidgets.QTreeWidgetItem()
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
        self.tree_data_input.setText(0, self.t("INPUTS"))
        self.tree_data_output.setText(0, self.t("OUTPUTS"))
        self.tree_data_rules.setText(0, self.t("RULES"))
        self.set_active_design_button.setText(self.t("SET_ACTIVE_DESIGN"))
        self.duplicate_design_button.setText(self.t("DUPLICATE"))
        self.delete_design_button.setText(self.t("DELETE"))
        self.design_table.setHorizontalHeaderLabels([self.t("ACTIVE"), self.t("DESIGN"), self.t("TYPE")])

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
            if category == "system":
                self.view_model.select_system_item(name, data)
            elif category == "design":
                self.view_model.select_design_item(name, data)
            self.status_bar.showMessage(f"{self.t('LAST_ACTION_SELECTED_ITEM')} {item.text(0)}")

    def clear_inputs(self):
        """Clear all inputs from the FIS model and tree widget."""
        if not self.view_model or not self.view_model.fuzzy_service:
            return

        fis_model = self.view_model.fuzzy_service.get_fis_model()
        if not fis_model or not fis_model._fis:
            return

        input_count = len(fis_model._fis.Inputs)
        for i in range(input_count - 1, -1, -1):
            self.view_model.fuzzy_service.delete_input_variable(i)

        self.view_model.refresh_browser()
        self.view_model.notify_data_changed.emit()
        self.del_inputs.emit()

    def clear_outputs(self):
        """Clear all outputs from the FIS model and tree widget."""
        if not self.view_model or not self.view_model.fuzzy_service:
            return

        fis_model = self.view_model.fuzzy_service.get_fis_model()
        if not fis_model or not fis_model._fis:
            return

        output_count = len(fis_model._fis.Outputs)
        for i in range(output_count - 1, -1, -1):
            self.view_model.fuzzy_service.delete_output_variable(i)

        self.view_model.refresh_browser()
        self.view_model.notify_data_changed.emit()
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

    def _show_context_menu(self, position):
        """Show context menu for the selected item."""
        item = self.tree.itemAt(position)
        if not item:
            return

        # Check if this is a category header (INPUTS, OUTPUTS, RULES)
        if item in [self.tree_data_input, self.tree_data_output, self.tree_data_rules]:
            menu = QtWidgets.QMenu(self)
            if item == self.tree_data_input:
                add_action = menu.addAction(self.t("ADD_INPUT"))
                add_action.triggered.connect(self._add_input_from_menu)
            elif item == self.tree_data_output:
                add_action = menu.addAction(self.t("ADD_OUTPUT"))
                add_action.triggered.connect(self._add_output_from_menu)
            elif item == self.tree_data_rules:
                add_action = menu.addAction(self.t("ADD_RULE"))
                add_action.triggered.connect(self._add_rule_from_menu)
            menu.exec(self.tree.mapToGlobal(position))
            return

        payload = item.data(0, QtCore.Qt.ItemDataRole.UserRole)
        if not isinstance(payload, dict):
            return

        data = payload.get("data", {})
        item_type = data.get("type")

        menu = QtWidgets.QMenu(self)

        if item_type == "input":
            add_mf_action = menu.addAction(self.t("ADD_MF"))
            add_mf_action.triggered.connect(lambda: self._add_mf_to_variable(data))
            menu.addSeparator()
            delete_action = menu.addAction(self.t("DELETE_INPUT"))
            delete_action.triggered.connect(lambda: self._delete_input(data))
            rename_action = menu.addAction(self.t("RENAME"))
            rename_action.triggered.connect(lambda: self._rename_input(data))
            menu.addSeparator()
            edit_action = menu.addAction(self.t("EDIT_PROPERTIES"))
            edit_action.triggered.connect(lambda: self._edit_input_properties(data))

        elif item_type == "output":
            add_mf_action = menu.addAction(self.t("ADD_MF"))
            add_mf_action.triggered.connect(lambda: self._add_mf_to_variable(data))
            menu.addSeparator()
            delete_action = menu.addAction(self.t("DELETE_OUTPUT"))
            delete_action.triggered.connect(lambda: self._delete_output(data))
            rename_action = menu.addAction(self.t("RENAME"))
            rename_action.triggered.connect(lambda: self._rename_output(data))
            menu.addSeparator()
            edit_action = menu.addAction(self.t("EDIT_PROPERTIES"))
            edit_action.triggered.connect(lambda: self._edit_output_properties(data))

        elif item_type == "rule":
            delete_action = menu.addAction(self.t("DELETE_RULE"))
            delete_action.triggered.connect(lambda: self._delete_rule(data))
            menu.addSeparator()
            edit_action = menu.addAction(self.t("EDIT"))
            edit_action.triggered.connect(lambda: self._edit_rule(data))

        elif item_type in ["input_mf", "output_mf"]:
            delete_action = menu.addAction(self.t("REMOVE_MF"))
            delete_action.triggered.connect(lambda: self._delete_mf(data))
            rename_action = menu.addAction(self.t("RENAME"))
            rename_action.triggered.connect(lambda: self._rename_mf(data))
            menu.addSeparator()
            edit_action = menu.addAction(self.t("EDIT_PROPERTIES"))
            edit_action.triggered.connect(lambda: self._edit_mf_properties(data))

        else:
            return

        menu.exec(self.tree.mapToGlobal(position))

    def _delete_input(self, data: dict):
        """Delete an input variable."""
        index = data.get("index")
        if index is not None and self.view_model and self.view_model.fuzzy_service:
            success = self.view_model.fuzzy_service.delete_input_variable(index)
            if success:
                self.view_model.refresh_browser()
                self.view_model.notify_data_changed.emit()

    def _delete_output(self, data: dict):
        """Delete an output variable."""
        index = data.get("index")
        if index is not None and self.view_model and self.view_model.fuzzy_service:
            success = self.view_model.fuzzy_service.delete_output_variable(index)
            if success:
                self.view_model.refresh_browser()
                self.view_model.notify_data_changed.emit()

    def _delete_rule(self, data: dict):
        """Delete a rule."""
        index = data.get("index")
        if index is not None and self.view_model and self.view_model.fuzzy_service:
            success = self.view_model.fuzzy_service.delete_rule(index)
            if success:
                self.view_model.refresh_browser()
                self.view_model.notify_data_changed.emit()

    def _delete_mf(self, data: dict):
        """Delete a membership function."""
        variable_name = data.get("variable_name")
        mf_index = data.get("index")
        item_type = data.get("type")

        if variable_name and mf_index is not None and self.view_model and self.view_model.fuzzy_service:
            variable_type = "input" if item_type == "input_mf" else "output"
            success = self.view_model.fuzzy_service.delete_membership_function(variable_name, mf_index, variable_type)
            if success:
                self.view_model.refresh_browser()
                self.view_model.notify_data_changed.emit()

    def _rename_input(self, data: dict):
        """Rename an input variable."""
        current_name = data.get("name")
        if not current_name or not self.view_model or not self.view_model.fuzzy_service:
            return

        new_name, ok = QtWidgets.QInputDialog.getText(
            self, self.t("RENAME"), self.t("NEW_NAME") + ":", text=current_name
        )
        if ok and new_name and new_name != current_name:
            success = self.view_model.fuzzy_service.update_variable_name(current_name, new_name, "input")
            if success:
                self.view_model.refresh_browser()
                self.view_model.notify_data_changed.emit()

    def _rename_output(self, data: dict):
        """Rename an output variable."""
        current_name = data.get("name")
        if not current_name or not self.view_model or not self.view_model.fuzzy_service:
            return

        new_name, ok = QtWidgets.QInputDialog.getText(
            self, self.t("RENAME"), self.t("NEW_NAME") + ":", text=current_name
        )
        if ok and new_name and new_name != current_name:
            success = self.view_model.fuzzy_service.update_variable_name(current_name, new_name, "output")
            if success:
                self.view_model.refresh_browser()
                self.view_model.notify_data_changed.emit()

    def _rename_mf(self, data: dict):
        """Rename a membership function."""
        variable_name = data.get("variable_name")
        mf_index = data.get("index")
        item_type = data.get("type")
        current_name = data.get("name")

        if not current_name or not variable_name or mf_index is None:
            return
        if not self.view_model or not self.view_model.fuzzy_service:
            return

        new_name, ok = QtWidgets.QInputDialog.getText(
            self, self.t("RENAME"), self.t("NEW_NAME") + ":", text=current_name
        )
        if ok and new_name and new_name != current_name:
            variable_type = "input" if item_type == "input_mf" else "output"
            success = self.view_model.fuzzy_service.update_membership_function_name(
                variable_name, mf_index, new_name, variable_type
            )
            if success:
                self.view_model.refresh_browser()
                self.view_model.notify_data_changed.emit()

    def _add_input_from_menu(self):
        """Add a new input variable from context menu."""
        if self.view_model and self.view_model.fuzzy_service:
            input_count = self.view_model.fuzzy_service.get_input_count()
            success = self.view_model.fuzzy_service.add_input_variable(f"input{input_count + 1}", 0.0, 1.0)
            if success:
                self.view_model.refresh_browser()
                self.view_model.notify_data_changed.emit()

    def _add_output_from_menu(self):
        """Add a new output variable from context menu."""
        if self.view_model and self.view_model.fuzzy_service:
            output_count = self.view_model.fuzzy_service.get_output_count()
            success = self.view_model.fuzzy_service.add_output_variable(f"output{output_count + 1}", 0.0, 1.0)
            if success:
                self.view_model.refresh_browser()
                self.view_model.notify_data_changed.emit()

    def _add_mf_to_variable(self, data: dict):
        """Add a membership function to a variable."""
        variable_name = data.get("name")
        item_type = data.get("type")

        if not variable_name or item_type not in ["input", "output"]:
            return
        if not self.view_model or not self.view_model.fuzzy_service:
            return

        variable_type = item_type
        mfs = data.get("membership_functions", [])

        # Check if this is a Sugeno output
        is_sugeno_output = False
        fis_model = self.view_model.fuzzy_service.get_fis_model()
        if fis_model and fis_model._fis:
            from fuzzylab import sugfis

            if isinstance(fis_model._fis, sugfis) and variable_type == "output":
                is_sugeno_output = True

        # Generate default MF name
        new_mf_name = f"mf{len(mfs) + 1}"

        # Get variable range for default parameters
        var_range = data.get("range", [0, 1])
        range_min, range_max = var_range[0], var_range[1]

        if is_sugeno_output:
            # For Sugeno, default to constant type
            mf_type = "stala"
            default_params = [0.5]
        else:
            # For Mamdani, default to triangle
            mf_type = "trojkatna"
            default_params = [range_min, (range_min + range_max) / 2, range_max]

        success = self.view_model.fuzzy_service.add_membership_function(
            variable_name, new_mf_name, mf_type, default_params, variable_type
        )
        if success:
            self.view_model.refresh_browser()
            self.view_model.notify_data_changed.emit()

    def _edit_input_properties(self, data: dict):
        """Edit input variable properties - navigate to MF Properties tab and select variable."""
        variable_name = data.get("name")
        if not variable_name or not self.view_model or not self.view_model.fuzzy_service:
            return

        # Set the selected input in the fuzzy service
        self.view_model.fuzzy_service.set_selected_input(variable_name)

        # Refresh FIS plot highlighting
        self._refresh_fis_plot_selection()

        # Find the editor tab widget and switch to MF Properties tab (index 1)
        editor_tab = self._find_editor_tab()
        if editor_tab:
            # Activate the main window if possible
            main_window = self._find_main_window()
            if main_window:
                main_window.activateWindow()
                main_window.raise_()

            editor_tab.setCurrentIndex(1)
            editor_tab.setFocus()
            editor_tab.show()

            # Use QTimer to ensure the update happens after tab switch
            QtCore.QTimer.singleShot(50, lambda: self._update_property_editor(editor_tab))

    def _edit_output_properties(self, data: dict):
        """Edit output variable properties - navigate to MF Properties tab and select variable."""
        variable_name = data.get("name")
        if not variable_name or not self.view_model or not self.view_model.fuzzy_service:
            return

        # Set the selected output in the fuzzy service
        self.view_model.fuzzy_service.set_selected_output(variable_name)

        # Refresh FIS plot highlighting
        self._refresh_fis_plot_selection()

        # Find the editor tab widget and switch to MF Properties tab (index 1)
        editor_tab = self._find_editor_tab()
        if editor_tab:
            # Activate the main window if possible
            main_window = self._find_main_window()
            if main_window:
                main_window.activateWindow()
                main_window.raise_()

            editor_tab.setCurrentIndex(1)
            editor_tab.setFocus()
            editor_tab.show()

            # Use QTimer to ensure the update happens after tab switch
            QtCore.QTimer.singleShot(50, lambda: self._update_property_editor(editor_tab))

    def _find_main_window(self):
        """Find the main window widget."""
        parent = self.parent()
        while parent:
            if isinstance(parent, QtWidgets.QMainWindow):
                return parent
            parent = parent.parent()
        return None

    def _refresh_fis_plot_selection(self):
        """Refresh the FIS plot selection highlighting."""
        # Find the central tab widget (contains FIS plot)
        central_tab = self._find_central_tab()
        if central_tab:
            # Find the FIS plot tab (usually index 0)
            fis_plot = None
            for i in range(central_tab.count()):
                widget = central_tab.widget(i)
                if widget and widget.objectName() == "fis_plot":
                    fis_plot = widget
                    break
                # Also check by class name
                if widget and widget.__class__.__name__ == "FisTabView":
                    fis_plot = widget
                    break

            if fis_plot:
                fis_plot.refresh_selection()

    def _find_central_tab(self):
        """Find the central tab widget."""
        # Try to find it in the current widget tree
        central_tab = self.findChild(QtWidgets.QWidget, "centralTab")
        if central_tab:
            return central_tab

        # Traverse up the parent hierarchy
        parent = self.parent()
        while parent:
            if parent.objectName() == "centralTab":
                return parent

            # Check if parent is a splitter and look for central tab in siblings
            if isinstance(parent, QtWidgets.QSplitter):
                for i in range(parent.count()):
                    widget = parent.widget(i)
                    if widget and widget.objectName() == "centralTab":
                        return widget
                    # Also check children
                    if widget:
                        central_tab = widget.findChild(QtWidgets.QWidget, "centralTab")
                        if central_tab:
                            return central_tab

            # Check children of current parent
            if isinstance(parent, QtWidgets.QWidget):
                central_tabs = parent.findChildren(QtWidgets.QWidget, "centralTab")
                if central_tabs:
                    return central_tabs[0]

            parent = parent.parent()

        return None

    def _update_property_editor(self, editor_tab):
        """Update the property editor in the editor tab."""
        if editor_tab:
            editor_tab.update_property_editor()

    def _find_editor_tab(self):
        """Find the editor tab widget by traversing parent hierarchy."""
        # First, try to find it in the current widget tree
        editor_tab = self.findChild(QtWidgets.QWidget, "editorTab")
        if editor_tab:
            return editor_tab

        # Traverse up the parent hierarchy
        parent = self.parent()
        while parent:
            if parent.objectName() == "editorTab":
                return parent

            # Check if parent is a splitter and look for editor tab in siblings
            if isinstance(parent, QtWidgets.QSplitter):
                for i in range(parent.count()):
                    widget = parent.widget(i)
                    if widget and widget.objectName() == "editorTab":
                        return widget
                    # Also check children of splitter widgets
                    if widget:
                        editor_tab = widget.findChild(QtWidgets.QWidget, "editorTab")
                        if editor_tab:
                            return editor_tab

            # Check children of current parent
            if isinstance(parent, QtWidgets.QWidget):
                editor_tabs = parent.findChildren(QtWidgets.QWidget, "editorTab")
                if editor_tabs:
                    return editor_tabs[0]

            parent = parent.parent()

        return None

    def _add_rule_from_menu(self):
        """Add a new rule from context menu."""
        # Find the editor tab widget and switch to Rule Properties tab (index 2)
        editor_tab = self._find_editor_tab()
        if editor_tab:
            # Activate the main window if possible
            main_window = self._find_main_window()
            if main_window:
                main_window.activateWindow()
                main_window.raise_()

            editor_tab.setCurrentIndex(2)
            editor_tab.setFocus()
            editor_tab.show()

            # Find the RulesEditorTab and trigger add rule
            rule_editor_tab = self._find_rule_editor_tab(editor_tab)
            if rule_editor_tab:
                QtCore.QTimer.singleShot(50, lambda: rule_editor_tab._on_add_rule_clicked())

    def _edit_rule(self, data: dict):
        """Edit a rule - navigate to Rule Properties tab and select the rule."""
        rule_index = data.get("index")
        if rule_index is None or not self.view_model or not self.view_model.fuzzy_service:
            return

        # Find the editor tab widget and switch to Rule Properties tab (index 2)
        editor_tab = self._find_editor_tab()
        if editor_tab:
            # Activate the main window if possible
            main_window = self._find_main_window()
            if main_window:
                main_window.activateWindow()
                main_window.raise_()

            editor_tab.setCurrentIndex(2)
            editor_tab.setFocus()
            editor_tab.show()

            # Find the RulesEditorTab and load the rule
            rule_editor_tab = self._find_rule_editor_tab(editor_tab)
            if rule_editor_tab:
                # Use QTimer to ensure the tab is fully loaded before selecting
                QtCore.QTimer.singleShot(100, lambda: self._select_rule_in_editor(rule_editor_tab, rule_index))

    def _find_rule_editor_tab(self, editor_tab):
        """Find the RulesEditorTab widget."""
        if not editor_tab:
            return None

        # Rule Properties tab is at index 2
        if editor_tab.count() > 2:
            rule_tab = editor_tab.widget(2)
            # Check if it's a RulesEditorTab or contains one
            if rule_tab:
                return rule_tab
            # Also check children
            rule_editor = rule_tab.findChild(QtWidgets.QWidget, "rules_properties_tab")
            if rule_editor:
                return rule_editor

        return None

    def _select_rule_in_editor(self, rule_editor_tab, rule_index: int):
        """Select a rule in the rule editor tab."""
        if not rule_editor_tab or not rule_editor_tab.rules_list:
            return

        # Find the rule in the list and select it
        rules_list = rule_editor_tab.rules_list
        if rules_list:
            for i in range(rules_list.count()):
                item = rules_list.item(i)
                if item and item.data(QtCore.Qt.ItemDataRole.UserRole) == rule_index:
                    rules_list.setCurrentItem(item)
                    rules_list.scrollToItem(item)
                    # Load the rule into the editor
                    rule_editor_tab._load_rule_into_editor(rule_index)
                    break

    def _edit_mf_properties(self, data: dict):
        """Edit membership function properties - navigate to MF Properties tab and select variable and MF."""
        variable_name = data.get("variable_name")
        mf_index = data.get("index")
        item_type = data.get("type")

        if not variable_name or mf_index is None or not self.view_model or not self.view_model.fuzzy_service:
            return

        # Determine variable type
        variable_type = "input" if item_type == "input_mf" else "output"

        # Set the selected variable in the fuzzy service
        if variable_type == "input":
            self.view_model.fuzzy_service.set_selected_input(variable_name)
        else:
            self.view_model.fuzzy_service.set_selected_output(variable_name)

        # Refresh FIS plot highlighting
        self._refresh_fis_plot_selection()

        # Find the editor tab widget and switch to MF Properties tab (index 1)
        editor_tab = self._find_editor_tab()
        if editor_tab:
            # Activate the main window if possible
            main_window = self._find_main_window()
            if main_window:
                main_window.activateWindow()
                main_window.raise_()

            editor_tab.setCurrentIndex(1)
            editor_tab.setFocus()
            editor_tab.show()

            # Use QTimer to ensure the update happens after tab switch
            QtCore.QTimer.singleShot(50, lambda: self._update_property_editor(editor_tab))

            # Select the specific MF row in the table
            # Use a longer delay to ensure the table is populated before selecting
            QtCore.QTimer.singleShot(150, lambda: self._select_mf_row(editor_tab, mf_index))

    def _select_mf_row(self, editor_tab, mf_index: int):
        """Select a specific row in the MF table."""
        if not editor_tab:
            return

        # Find the MF table in the editor tab
        mf_table = None
        mf_properties_tab = editor_tab.widget(1) if editor_tab.count() > 1 else None
        if mf_properties_tab:
            # The table is inside editor_frame
            editor_frame = mf_properties_tab.findChild(QtWidgets.QFrame, "editor_frame")
            if editor_frame:
                mf_table = editor_frame.findChild(QtWidgets.QTableWidget, "mf_table")

        if mf_table and 0 <= mf_index < mf_table.rowCount():
            mf_table.selectRow(mf_index)
            mf_table.setCurrentCell(mf_index, 0)

    def _populate_design_projects(self, projects: list) -> None:
        """Populate the design browser table with saved projects."""
        self.design_table.setRowCount(len(projects))
        current_project = self.view_model.current_project_name if self.view_model else None

        for row, project in enumerate(projects):
            project_name = project.get("name", "")
            project_path = project.get("path", "")

            is_active = current_project == project_name.replace(".fis", "")
            active_item = QtWidgets.QTableWidgetItem("✓" if is_active else "")
            active_item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            project_data = {"type": "project", "name": project_name, "data": project}
            active_item.setData(QtCore.Qt.ItemDataRole.UserRole, project_data)
            self.design_table.setItem(row, 0, active_item)

            fis_name = self._get_fis_name_from_file(project_path)
            design_item = QtWidgets.QTableWidgetItem(fis_name if fis_name else project_name.replace(".fis", ""))
            design_item.setData(QtCore.Qt.ItemDataRole.UserRole, project_data)
            self.design_table.setItem(row, 1, design_item)

            fis_type = self._get_fis_type_from_file(project_path)
            type_item = QtWidgets.QTableWidgetItem(fis_type)
            type_item.setData(QtCore.Qt.ItemDataRole.UserRole, project_data)
            self.design_table.setItem(row, 2, type_item)

        self.design_table.resizeColumnsToContents()

    def _on_design_table_double_clicked(self, item: QtWidgets.QTableWidgetItem) -> None:
        """Handle double-click on a design project to load it."""
        payload = item.data(QtCore.Qt.ItemDataRole.UserRole)
        if isinstance(payload, dict) and payload.get("type") == "project":
            project_name = payload.get("name", "")
            success = self.view_model.load_project(project_name)
            if success:
                msg = f"{self.t('LOADED_PROJECT')} {project_name}"
                self.status_bar.showMessage(msg, 3000)
            self.view_model.refresh_projects()

    def _on_project_switched(self, project_name: str) -> None:
        """Handle project switch event."""
        self._update_active_column()
        for row in range(self.design_table.rowCount()):
            item = self.design_table.item(row, 1)
            if item:
                payload = item.data(QtCore.Qt.ItemDataRole.UserRole)
                if isinstance(payload, dict):
                    item_project_name = payload.get("name", "").replace(".fis", "")
                    if item_project_name == project_name:
                        self.design_table.selectRow(row)
                        break

    def _get_fis_name_from_file(self, file_path: str) -> str:
        """Get FIS name from file path."""
        if not file_path:
            return ""

        try:
            from pathlib import Path

            from app.models.fis_reader_writer import FISReaderWriter

            path_str = str(file_path) if isinstance(file_path, Path) else file_path
            reader = FISReaderWriter()
            result = reader.read_fis(path_str)

            if result == 1 and reader.model and reader.model._fis:
                fis_name = reader.model._fis.Name
                return str(fis_name) if fis_name else ""
        except Exception as e:
            print(f"Error reading FIS name from {file_path}: {e}")

        return ""

    def _get_fis_type_from_file(self, file_path: str) -> str:
        """Get FIS type from file path."""
        if not file_path:
            return "Mamdani Type-1"

        try:
            from pathlib import Path

            from app.models.fis_reader_writer import FISReaderWriter

            path_str = str(file_path) if isinstance(file_path, Path) else file_path
            reader = FISReaderWriter()
            result = reader.read_fis(path_str)

            if result == 1 and reader.model and reader.model._fis:
                fis_type_name = type(reader.model._fis).__name__.lower()
                if "sug" in fis_type_name:
                    return "Sugeno Type-1"
                else:
                    return "Mamdani Type-1"
        except Exception as e:
            print(f"Error reading FIS type from {file_path}: {e}")

        return "Mamdani Type-1"

    def _update_active_column(self) -> None:
        """Update the active column to show which project is currently active."""
        current_project = self.view_model.current_project_name if self.view_model else None

        for row in range(self.design_table.rowCount()):
            active_item = self.design_table.item(row, 0)
            design_item = self.design_table.item(row, 1)

            if design_item:
                payload = design_item.data(QtCore.Qt.ItemDataRole.UserRole)
                if isinstance(payload, dict):
                    project_name = payload.get("name", "").replace(".fis", "")
                    is_active = current_project == project_name

                    if active_item:
                        active_item.setText("✓" if is_active else "")

    def _show_design_context_menu(self, position):
        """Show context menu for the design browser table."""
        item = self.design_table.itemAt(position)
        menu = QtWidgets.QMenu(self)

        if item:
            payload = item.data(QtCore.Qt.ItemDataRole.UserRole)
            if isinstance(payload, dict) and payload.get("type") == "project":
                load_action = menu.addAction(self.t("LOAD_PROJECT"))
                load_action.triggered.connect(lambda: self._load_project_from_menu(item))
                menu.addSeparator()
                rename_action = menu.addAction(self.t("RENAME"))
                rename_action.triggered.connect(lambda: self._rename_project_from_menu(item))
                delete_action = menu.addAction(self.t("DELETE_PROJECT"))
                delete_action.triggered.connect(lambda: self._delete_project_from_menu(item))
        else:
            save_action = menu.addAction(self.t("SAVE_CURRENT_PROJECT"))
            save_action.triggered.connect(self._save_current_project_from_menu)

        menu.exec(self.design_table.mapToGlobal(position))

    def _set_active_design(self) -> None:
        """Set the selected design as active (load it)."""
        selected_items = self.design_table.selectedItems()
        if not selected_items:
            self.status_bar.showMessage(self.t("NO_DESIGN_SELECTED"), 3000)
            return

        item = selected_items[0]
        payload = item.data(QtCore.Qt.ItemDataRole.UserRole)
        if isinstance(payload, dict) and payload.get("type") == "project":
            project_name = payload.get("name", "")
            success = self.view_model.load_project(project_name)
            if success:
                msg = f"{self.t('LOADED_PROJECT')} {project_name}"
                self.status_bar.showMessage(msg, 3000)
            self.view_model.refresh_projects()

    def _duplicate_design(self) -> None:
        """Duplicate the selected design."""
        selected_items = self.design_table.selectedItems()
        if not selected_items:
            self.status_bar.showMessage(self.t("NO_DESIGN_SELECTED"), 3000)
            return

        item = selected_items[0]
        payload = item.data(QtCore.Qt.ItemDataRole.UserRole)
        if not isinstance(payload, dict) or payload.get("type") != "project":
            return

        old_name = payload.get("name", "").replace(".fis", "")
        new_name, ok = QtWidgets.QInputDialog.getText(
            self, self.t("DUPLICATE_DESIGN"), self.t("NEW_NAME") + ":", text=f"{old_name}_copy"
        )
        if ok and new_name:
            success = self.view_model.duplicate_project(old_name, new_name)
            if success:
                self.status_bar.showMessage(f"{self.t('DUPLICATED_DESIGN')} {old_name} -> {new_name}", 3000)
            else:
                self.status_bar.showMessage(self.t("DUPLICATE_DESIGN_FAILED"), 3000)

    def _delete_design(self) -> None:
        """Delete the selected design."""
        selected_items = self.design_table.selectedItems()
        if not selected_items:
            self.status_bar.showMessage(self.t("NO_DESIGN_SELECTED"), 3000)
            return

        item = selected_items[0]
        payload = item.data(QtCore.Qt.ItemDataRole.UserRole)
        if not isinstance(payload, dict) or payload.get("type") != "project":
            return

        project_name = payload.get("name", "")
        reply = QtWidgets.QMessageBox.question(
            self,
            self.t("DELETE_PROJECT"),
            f"{self.t('DELETE_PROJECT_CONFIRM')} {project_name}?",
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No,
        )

        if reply == QtWidgets.QMessageBox.StandardButton.Yes:
            success = self.view_model.delete_project(project_name)
            if success:
                self.status_bar.showMessage(f"{self.t('DELETED_PROJECT')} {project_name}", 3000)
            else:
                self.status_bar.showMessage(self.t("DELETE_PROJECT_FAILED"), 3000)

    def _load_project_from_menu(self, item: QtWidgets.QTableWidgetItem) -> None:
        """Load a project from the context menu."""
        payload = item.data(QtCore.Qt.ItemDataRole.UserRole)
        if isinstance(payload, dict) and payload.get("type") == "project":
            project_name = payload.get("name", "")
            success = self.view_model.load_project(project_name)
            if success:
                self.status_bar.showMessage(f"{self.t('LOADED_PROJECT')} {project_name}", 3000)
                self.view_model.refresh_projects()

    def _save_current_project_from_menu(self) -> None:
        """Save the current project from the context menu."""
        if not self.view_model:
            return

        project_name, ok = QtWidgets.QInputDialog.getText(
            self, self.t("SAVE_PROJECT"), self.t("PROJECT_NAME") + ":", text=""
        )
        if ok and project_name:
            success = self.view_model.save_current_project(project_name)
            if success:
                self.status_bar.showMessage(f"{self.t('SAVED_PROJECT')} {project_name}", 3000)
            else:
                self.status_bar.showMessage(self.t("SAVE_PROJECT_FAILED"), 3000)

    def _rename_project_from_menu(self, item: QtWidgets.QTableWidgetItem) -> None:
        """Rename a project from the context menu."""
        payload = item.data(QtCore.Qt.ItemDataRole.UserRole)
        if not isinstance(payload, dict) or payload.get("type") != "project":
            return

        old_name = payload.get("name", "")
        new_name, ok = QtWidgets.QInputDialog.getText(
            self, self.t("RENAME_PROJECT"), self.t("NEW_NAME") + ":", text=old_name.replace(".fis", "")
        )
        if ok and new_name and new_name != old_name.replace(".fis", ""):
            success = self.view_model.rename_project(old_name, new_name)
            if success:
                self.status_bar.showMessage(f"{self.t('RENAMED_PROJECT')} {old_name} -> {new_name}", 3000)
            else:
                self.status_bar.showMessage(self.t("RENAME_PROJECT_FAILED"), 3000)

    def _delete_project_from_menu(self, item: QtWidgets.QTableWidgetItem) -> None:
        """Delete a project from the context menu."""
        payload = item.data(QtCore.Qt.ItemDataRole.UserRole)
        if not isinstance(payload, dict) or payload.get("type") != "project":
            return

        project_name = payload.get("name", "")
        reply = QtWidgets.QMessageBox.question(
            self,
            self.t("DELETE_PROJECT"),
            f"{self.t('DELETE_PROJECT_CONFIRM')} {project_name}?",
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No,
        )

        if reply == QtWidgets.QMessageBox.StandardButton.Yes:
            success = self.view_model.delete_project(project_name)
            if success:
                self.status_bar.showMessage(f"{self.t('DELETED_PROJECT')} {project_name}", 3000)
            else:
                self.status_bar.showMessage(self.t("DELETE_PROJECT_FAILED"), 3000)
