"""Create a tab GUI object to insert into editor tab on the right of main window.

Classes:
    RulesEditorTab: button area element inheriting from QTabWidget.
"""

import re

from PyQt6 import QtCore, QtWidgets

from app.view_models.rules_editor_view_model import RulesEditorViewModel
from app.views.base_widget_view import BaseWidgetView


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


class RulesEditorTab(BaseWidgetView):
    """Class inheriting from QWidget.

    Allows user interaction via QPushButton, QLineEdit and QComboBox GUI elements.
    The class allows to change the parameters of the rules interference logic.

    Methods:
        __init__(parent): create an instance of RulesEditorTab and bind it to the
            parent window.
    """

    _symbols = {"is": "==", "is not": "~=", "then": "=>", "and": "&", "or": "|"}

    def __init__(self, parent=None):
        """Initialize a new class instance.

        Args:
            parent (QWidget, optional): The parent widget, in this case editor
                tab, to which the widget will be attached. Defaults to None.
        """
        super().__init__(parent=parent)
        self.setObjectName("rules_properties_tab")

        self.view_model = RulesEditorViewModel()
        self.view_model.setParent(self)
        self.set_view_model(self.view_model)

        self._updating_rule = False
        self._current_rule_index = -1
        self.input_dropdowns = []
        self.input_is_dropdowns = []
        self.output_dropdowns = []
        self.output_is_dropdowns = []

        self._setup_ui()
        self._retranslate_ui()
        self._connect_view_model_signals()
        self._connect_ui_signals()

    def _connect_view_model_signals(self):
        """Connect view model signals to view methods."""
        self.view_model.rules_updated.connect(self._update_rules_list)
        self.view_model.input_mf_options_updated.connect(self._update_input_mf_dropdowns)
        self.view_model.output_mf_options_updated.connect(self._update_output_mf_dropdowns)
        self.view_model.data_changed.connect(self._on_data_changed)

    def _connect_ui_signals(self):
        """Connect UI element signals."""
        self.add_all_rules_button.clicked.connect(self._on_add_all_rules_clicked)
        self.clear_rules_button.clicked.connect(self._on_clear_rules_clicked)
        self.add_rule_button.clicked.connect(self._on_add_rule_clicked)
        self.update_rule_button.clicked.connect(self._on_update_rule_clicked)
        self.delete_rule_button.clicked.connect(self._on_delete_rule_clicked)

        self.rules_list.itemSelectionChanged.connect(self._on_rule_selected)

        self.rule_name_edit.editingFinished.connect(self._on_rule_name_changed)
        self.rule_weight_edit.editingFinished.connect(self._on_rule_weight_changed)

        self.and_radio_button.toggled.connect(self._on_connection_changed)
        self.or_radio_button.toggled.connect(self._on_connection_changed)

        self.display_mode_combo.currentTextChanged.connect(self._on_display_mode_changed)

    def _on_data_changed(self):
        """Handle data changed signal from view model."""
        self._build_rule_editor_dropdowns()
        self._update_rules_list(self.view_model.rules)
        if self._current_rule_index >= 0:
            if self._current_rule_index < len(self.view_model.rules):
                self._load_rule_into_editor(self._current_rule_index)

    def refresh_ui(self) -> None:
        """Refresh the UI elements."""
        self.view_model.refresh_data()

    def update_ui(self) -> None:
        """Update UI elements from view model."""
        pass

    def handle_global_update(self) -> None:
        """Handle global update request."""
        pass

    def _setup_ui(self):
        """Set up all the GUI sub elements."""
        main_layout = QtWidgets.QVBoxLayout(self)

        self.title_label = QtWidgets.QLabel(self.t("RULE_EDITOR"), parent=self)
        self.title_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        main_layout.addWidget(self.title_label)

        self.rules_group = QtWidgets.QGroupBox(self.t("RULES_LIST"), parent=self)
        rules_layout = QtWidgets.QVBoxLayout(self.rules_group)

        display_mode_layout = QtWidgets.QHBoxLayout()
        self.display_mode_label = QtWidgets.QLabel(self.t("DISPLAY_MODE") + ":", parent=self)
        display_mode_layout.addWidget(self.display_mode_label)

        self.display_mode_combo = QtWidgets.QComboBox(parent=self)
        self.display_mode_combo.addItems([self.t("SYMBOLIC"), self.t("INDEXED"), self.t("VERBOSE")])
        display_mode_layout.addWidget(self.display_mode_combo)
        display_mode_layout.addStretch()
        rules_layout.addLayout(display_mode_layout)

        self.rules_list = QtWidgets.QListWidget(parent=self)
        self.rules_list.setMaximumHeight(150)
        rules_layout.addWidget(self.rules_list)

        rules_buttons_layout = QtWidgets.QHBoxLayout()
        self.add_all_rules_button = QtWidgets.QPushButton(self.t("ADD_ALL_RULES"), parent=self)
        self.clear_rules_button = QtWidgets.QPushButton(self.t("CLEAR_RULES"), parent=self)
        rules_buttons_layout.addWidget(self.add_all_rules_button)
        rules_buttons_layout.addWidget(self.clear_rules_button)
        rules_layout.addLayout(rules_buttons_layout)

        main_layout.addWidget(self.rules_group)

        self.rule_editor_group = QtWidgets.QGroupBox(self.t("RULE_EDITOR"), parent=self)
        editor_layout = QtWidgets.QVBoxLayout(self.rule_editor_group)

        name_layout = QtWidgets.QHBoxLayout()
        self.name_label = QtWidgets.QLabel(self.t("NAME") + ":", parent=self)
        name_layout.addWidget(self.name_label)
        self.rule_name_edit = QtWidgets.QLineEdit(parent=self)
        name_layout.addWidget(self.rule_name_edit)
        editor_layout.addLayout(name_layout)

        weight_layout = QtWidgets.QHBoxLayout()
        self.weight_label = QtWidgets.QLabel(self.t("WEIGHT") + ":", parent=self)
        weight_layout.addWidget(self.weight_label)
        self.rule_weight_edit = QtWidgets.QLineEdit(parent=self)
        self.rule_weight_edit.setText("1.0")
        weight_layout.addWidget(self.rule_weight_edit)
        editor_layout.addLayout(weight_layout)

        connection_layout = QtWidgets.QHBoxLayout()
        self.connection_label = QtWidgets.QLabel(self.t("CONNECTION") + ":", parent=self)
        connection_layout.addWidget(self.connection_label)
        self.and_radio_button = QtWidgets.QRadioButton(self.t("AND"), parent=self)
        self.and_radio_button.setChecked(True)
        self.or_radio_button = QtWidgets.QRadioButton(self.t("OR"), parent=self)
        connection_layout.addWidget(self.and_radio_button)
        connection_layout.addWidget(self.or_radio_button)
        connection_layout.addStretch()
        editor_layout.addLayout(connection_layout)

        self.if_label = QtWidgets.QLabel(self.t("IF"), parent=self)
        self.if_label.setStyleSheet("font-weight: bold;")
        editor_layout.addWidget(self.if_label)

        self.antecedent_layout = QtWidgets.QVBoxLayout()
        editor_layout.addLayout(self.antecedent_layout)

        self.then_label = QtWidgets.QLabel(self.t("THEN"), parent=self)
        self.then_label.setStyleSheet("font-weight: bold;")
        editor_layout.addWidget(self.then_label)

        self.consequent_layout = QtWidgets.QVBoxLayout()
        editor_layout.addLayout(self.consequent_layout)

        rule_buttons_layout = QtWidgets.QHBoxLayout()
        self.add_rule_button = QtWidgets.QPushButton(self.t("ADD_RULE"), parent=self)
        self.update_rule_button = QtWidgets.QPushButton(self.t("UPDATE_RULE"), parent=self)
        self.update_rule_button.setVisible(False)
        self.delete_rule_button = QtWidgets.QPushButton(self.t("DELETE_RULE"), parent=self)
        rule_buttons_layout.addWidget(self.add_rule_button)
        rule_buttons_layout.addWidget(self.update_rule_button)
        rule_buttons_layout.addWidget(self.delete_rule_button)
        editor_layout.addLayout(rule_buttons_layout)

        main_layout.addWidget(self.rule_editor_group)
        main_layout.addStretch()

        self._build_rule_editor_dropdowns()

    def _build_rule_editor_dropdowns(self):
        """Build dropdowns for antecedent and consequent based on current variables."""
        if not self.view_model or not self.view_model.fuzzy_service:
            return

        for dropdown in self.input_dropdowns:
            if dropdown:
                dropdown.setParent(None)
                dropdown.deleteLater()
        for dropdown in self.input_is_dropdowns:
            if dropdown:
                dropdown.setParent(None)
                dropdown.deleteLater()
        for dropdown in self.output_dropdowns:
            if dropdown:
                dropdown.setParent(None)
                dropdown.deleteLater()
        for dropdown in self.output_is_dropdowns:
            if dropdown:
                dropdown.setParent(None)
                dropdown.deleteLater()

        while self.antecedent_layout.count():
            item = self.antecedent_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)
                widget.deleteLater()
            layout = item.layout()
            if layout:
                while layout.count():
                    layout_item = layout.takeAt(0)
                    layout_widget = layout_item.widget()
                    if layout_widget:
                        layout_widget.setParent(None)
                        layout_widget.deleteLater()
                layout.setParent(None)

        while self.consequent_layout.count():
            item = self.consequent_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)
                widget.deleteLater()
            layout = item.layout()
            if layout:
                while layout.count():
                    layout_item = layout.takeAt(0)
                    layout_widget = layout_item.widget()
                    if layout_widget:
                        layout_widget.setParent(None)
                        layout_widget.deleteLater()
                layout.setParent(None)

        self.input_dropdowns = []
        self.input_is_dropdowns = []

        input_vars = self.view_model.fuzzy_service.get_input_variables()
        for i, var in enumerate(input_vars):
            var_name = var.get("name", f"Input{i+1}")
            mfs = self.view_model.fuzzy_service.get_membership_functions(var_name, "input")

            row_layout = QtWidgets.QHBoxLayout()
            row_layout.addWidget(QtWidgets.QLabel(f"{var_name}: ", parent=self))

            is_dropdown = QtWidgets.QComboBox(parent=self)
            is_dropdown.addItems([self.t("IS"), self.t("IS_NOT")])
            is_dropdown.currentTextChanged.connect(self._on_antecedent_changed)
            row_layout.addWidget(is_dropdown)
            self.input_is_dropdowns.append(is_dropdown)

            mf_dropdown = QtWidgets.QComboBox(parent=self)
            mf_dropdown.addItem(self.t("NONE"), 0)
            for mf in mfs:
                mf_dropdown.addItem(mf.get("name", ""), mf.get("index", 0) + 1)
            mf_dropdown.currentIndexChanged.connect(self._on_antecedent_changed)
            row_layout.addWidget(mf_dropdown)
            self.input_dropdowns.append(mf_dropdown)

            self.antecedent_layout.addLayout(row_layout)

        self.output_dropdowns = []
        self.output_is_dropdowns = []

        output_vars = self.view_model.fuzzy_service.get_output_variables()
        for i, var in enumerate(output_vars):
            var_name = var.get("name", f"Output{i+1}")
            mfs = self.view_model.fuzzy_service.get_membership_functions(var_name, "output")

            row_layout = QtWidgets.QHBoxLayout()
            row_layout.addWidget(QtWidgets.QLabel(f"{var_name}: ", parent=self))

            is_dropdown = QtWidgets.QComboBox(parent=self)
            is_dropdown.addItems([self.t("IS"), self.t("IS_NOT")])
            is_dropdown.currentTextChanged.connect(self._on_consequent_changed)
            row_layout.addWidget(is_dropdown)
            self.output_is_dropdowns.append(is_dropdown)

            mf_dropdown = QtWidgets.QComboBox(parent=self)
            mf_dropdown.addItem(self.t("NONE"), 0)
            for mf in mfs:
                mf_dropdown.addItem(mf.get("name", ""), mf.get("index", 0) + 1)
            mf_dropdown.currentIndexChanged.connect(self._on_consequent_changed)
            row_layout.addWidget(mf_dropdown)
            self.output_dropdowns.append(mf_dropdown)

            self.consequent_layout.addLayout(row_layout)

    def _update_rules_list(self, rules_list):
        """Update the rules list from view model."""
        self.rules_list.clear()

        if not rules_list:
            return

        display_mode = self.display_mode_combo.currentText()

        for rule in rules_list:
            rule_index = rule.get("index", 0)

            try:
                if display_mode == self.t("SYMBOLIC"):
                    rule_text = self.view_model.get_rule_text(rule_index)
                    if rule_text and not rule_text.startswith("Error:") and not rule_text.startswith("Rule"):
                        pattern = r"\b({})\b".format("|".join(sorted(re.escape(k) for k in self._symbols)))
                        symbolic_rule = re.sub(pattern, lambda m: self._symbols.get(m.group(0)), rule_text)
                        symbolic_rule = re.sub(r"(=>)(.*)", _regex_func, symbolic_rule)
                        if not symbolic_rule or symbolic_rule == rule_text:
                            symbolic_rule = rule_text
                        text = symbolic_rule
                    else:
                        ant = rule.get("antecedent", [])
                        cons = rule.get("consequent", [])
                        ant_str = ",".join(map(str, ant))
                        cons_str = ",".join(map(str, cons))
                        text = f"{self.t('RULE')}{rule_index + 1}: [{ant_str}] -> [{cons_str}]"
                elif display_mode == self.t("INDEXED"):
                    ant = rule.get("antecedent", [])
                    cons = rule.get("consequent", [])
                    ant_str = ",".join(map(str, ant))
                    cons_str = ",".join(map(str, cons))
                    text = f"{self.t('RULE')}{rule_index + 1}: [{ant_str}] -> [{cons_str}]"
                else:
                    text = self.view_model.get_rule_text(rule_index)
                    if not text or text.startswith("Error:"):
                        ant = rule.get("antecedent", [])
                        cons = rule.get("consequent", [])
                        ant_str = ",".join(map(str, ant))
                        cons_str = ",".join(map(str, cons))
                        text = f"{self.t('RULE')}{rule_index + 1}: [{ant_str}] -> [{cons_str}]"
            except Exception:
                ant = rule.get("antecedent", [])
                cons = rule.get("consequent", [])
                ant_str = ",".join(map(str, ant))
                cons_str = ",".join(map(str, cons))
                text = f"{self.t('RULE')}{rule_index + 1}: [{ant_str}] -> [{cons_str}]"

            item = QtWidgets.QListWidgetItem(text)
            item.setData(QtCore.Qt.ItemDataRole.UserRole, rule_index)
            self.rules_list.addItem(item)

    def _update_input_mf_dropdowns(self, input_mf_options):
        """Update input MF dropdowns with new options."""
        self._build_rule_editor_dropdowns()

    def _update_output_mf_dropdowns(self, output_mf_options):
        """Update output MF dropdowns with new options."""
        self._build_rule_editor_dropdowns()

    def _retranslate_ui(self):
        """Add text to all the respective GUI elements."""
        self.name_label.setText(self.t("NAME") + ":")
        self.weight_label.setText(self.t("WEIGHT") + ":")
        self.connection_label.setText(self.t("CONNECTION") + ":")
        self.and_radio_button.setText(self.t("AND"))
        self.or_radio_button.setText(self.t("OR"))
        self.if_label.setText(self.t("IF"))
        self.then_label.setText(self.t("THEN"))
        self.add_rule_button.setText(self.t("ADD_RULE"))
        self.update_rule_button.setText(self.t("UPDATE_RULE"))
        self.delete_rule_button.setText(self.t("DELETE_RULE"))
        self.rules_group.setTitle(self.t("RULES_LIST"))
        self.rule_editor_group.setTitle(self.t("RULE_EDITOR"))
        self.title_label.setText(self.t("RULE_EDITOR"))
        self.display_mode_label.setText(self.t("DISPLAY_MODE") + ":")
        self.add_all_rules_button.setText(self.t("ADD_ALL_RULES"))
        self.clear_rules_button.setText(self.t("CLEAR_RULES"))
        self.display_mode_combo.clear()
        self.display_mode_combo.addItems([self.t("SYMBOLIC"), self.t("INDEXED"), self.t("VERBOSE")])

    def _on_add_all_rules_clicked(self):
        """Handle Add All Rules button click."""
        success = self.view_model.add_all_possible_rules()
        if success:
            QtWidgets.QMessageBox.information(self, self.t("SUCCESS"), self.t("ALL_RULES_ADDED"))

    def _on_clear_rules_clicked(self):
        """Handle Clear Rules button click."""
        reply = QtWidgets.QMessageBox.question(
            self,
            self.t("CONFIRM"),
            self.t("CLEAR_ALL_RULES_CONFIRM"),
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No,
        )

        if reply == QtWidgets.QMessageBox.StandardButton.Yes:
            success = self.view_model.clear_all_rules()
            if success:
                self._clear_rule_editor()

    def _on_add_rule_clicked(self):
        """Handle Add Rule button click."""
        if not self.view_model:
            return

        rule_name = self.rule_name_edit.text() or self.t("NEW_RULE")

        try:
            weight = float(self.rule_weight_edit.text())
        except ValueError:
            weight = 1.0

        connection = 1 if self.and_radio_button.isChecked() else 0

        antecedent = []
        is_mf = []

        for i, dropdown in enumerate(self.input_dropdowns):
            mf_index = dropdown.currentData()
            antecedent.append(mf_index if mf_index is not None else 0)
            is_not = 1 if self.input_is_dropdowns[i].currentText() == self.t("IS") else -1
            is_mf.append(is_not)

        consequent = []
        for i, dropdown in enumerate(self.output_dropdowns):
            mf_index = dropdown.currentData()
            consequent.append(mf_index if mf_index is not None else 0)
            is_not = 1 if self.output_is_dropdowns[i].currentText() == self.t("IS") else -1
            is_mf.append(is_not)

        success = self.view_model.add_rule(
            rule_name=rule_name,
            weight=weight,
            connection=connection,
            antecedent=antecedent,
            consequent=consequent,
            is_mf=is_mf,
        )

        if success:
            self._clear_rule_editor()

    def _on_delete_rule_clicked(self):
        """Handle Delete Rule button click."""
        if not self.view_model:
            return

        selected_items = self.rules_list.selectedItems()
        if not selected_items:
            QtWidgets.QMessageBox.warning(self, self.t("WARNING"), self.t("NO_RULE_SELECTED"))
            return

        rule_index = selected_items[0].data(QtCore.Qt.ItemDataRole.UserRole)

        reply = QtWidgets.QMessageBox.question(
            self,
            self.t("CONFIRM"),
            self.t("DELETE_RULE_CONFIRM"),
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No,
        )

        if reply == QtWidgets.QMessageBox.StandardButton.Yes:
            success = self.view_model.delete_rule(rule_index)
            if success:
                self._current_rule_index = -1
                self.rules_list.clearSelection()
                self._clear_rule_editor()
                self._update_button_states()

    def _on_rule_selected(self):
        """Handle rule selection from list."""
        selected_items = self.rules_list.selectedItems()
        if not selected_items:
            return

        rule_index = selected_items[0].data(QtCore.Qt.ItemDataRole.UserRole)
        self._load_rule_into_editor(rule_index)

    def _load_rule_into_editor(self, rule_index):
        """Load a rule into the editor fields."""
        if not self.view_model or not (0 <= rule_index < len(self.view_model.rules)):
            return

        self._updating_rule = True
        self._current_rule_index = rule_index

        rule = self.view_model.rules[rule_index]

        self.rule_name_edit.setText(rule.get("name", ""))
        self.rule_weight_edit.setText(str(rule.get("weight", 1.0)))

        connection = rule.get("connection", 1)
        if connection == 1:
            self.and_radio_button.setChecked(True)
        else:
            self.or_radio_button.setChecked(True)

        antecedent = rule.get("antecedent", [])
        consequent = rule.get("consequent", [])
        is_mf = rule.get("is_mf", [])

        for i, mf_idx in enumerate(antecedent):
            if i < len(self.input_dropdowns):
                self.input_dropdowns[i].blockSignals(True)
                index = self.input_dropdowns[i].findData(mf_idx)
                if index >= 0:
                    self.input_dropdowns[i].setCurrentIndex(index)
                self.input_dropdowns[i].blockSignals(False)

                if i < len(is_mf):
                    self.input_is_dropdowns[i].blockSignals(True)
                    self.input_is_dropdowns[i].setCurrentText(self.t("IS") if is_mf[i] == 1 else self.t("IS_NOT"))
                    self.input_is_dropdowns[i].blockSignals(False)

        for i, mf_idx in enumerate(consequent):
            if i < len(self.output_dropdowns):
                self.output_dropdowns[i].blockSignals(True)
                index = self.output_dropdowns[i].findData(mf_idx)
                if index >= 0:
                    self.output_dropdowns[i].setCurrentIndex(index)
                self.output_dropdowns[i].blockSignals(False)

                out_is_idx = i + len(antecedent)
                if out_is_idx < len(is_mf):
                    self.output_is_dropdowns[i].blockSignals(True)
                    self.output_is_dropdowns[i].setCurrentText(
                        self.t("IS") if is_mf[out_is_idx] == 1 else self.t("IS_NOT")
                    )
                    self.output_is_dropdowns[i].blockSignals(False)

        self._updating_rule = False
        self._update_button_states()

    def _clear_rule_editor(self):
        """Clear the rule editor fields."""
        self._updating_rule = True
        self._current_rule_index = -1

        self.rule_name_edit.clear()
        self.rule_weight_edit.setText("1.0")
        self.and_radio_button.setChecked(True)

        for dropdown in self.input_dropdowns:
            dropdown.blockSignals(True)
            dropdown.setCurrentIndex(0)
            dropdown.blockSignals(False)
        for dropdown in self.input_is_dropdowns:
            dropdown.blockSignals(True)
            dropdown.setCurrentIndex(0)
            dropdown.blockSignals(False)
        for dropdown in self.output_dropdowns:
            dropdown.blockSignals(True)
            dropdown.setCurrentIndex(0)
            dropdown.blockSignals(False)
        for dropdown in self.output_is_dropdowns:
            dropdown.blockSignals(True)
            dropdown.setCurrentIndex(0)
            dropdown.blockSignals(False)

        self._updating_rule = False
        self._update_button_states()

    def _on_rule_name_changed(self):
        """Handle rule name change."""
        if self._updating_rule or self._current_rule_index < 0:
            return

        new_name = self.rule_name_edit.text()
        self.view_model.update_rule_name(self._current_rule_index, new_name)

    def _on_rule_weight_changed(self):
        """Handle rule weight change."""
        if self._updating_rule or self._current_rule_index < 0:
            return

        try:
            new_weight = float(self.rule_weight_edit.text())
            self.view_model.update_rule_weight(self._current_rule_index, new_weight)
        except ValueError:
            pass

    def _on_connection_changed(self):
        """Handle connection (AND/OR) change."""
        if self._updating_rule or self._current_rule_index < 0:
            return

        new_connection = 1 if self.and_radio_button.isChecked() else 0
        self.view_model.update_rule_connection(self._current_rule_index, new_connection)

    def _on_display_mode_changed(self, mode):
        """Handle display mode change."""
        self._update_rules_list(self.view_model.rules)

    def _update_button_states(self):
        """Update button visibility based on whether we're editing or adding."""
        is_editing = self._current_rule_index >= 0
        self.add_rule_button.setVisible(not is_editing)
        self.update_rule_button.setVisible(is_editing)

    def _on_update_rule_clicked(self):
        """Handle Update Rule button click."""
        if not self.view_model or self._current_rule_index < 0:
            return

        current_rule = self.view_model.rules[self._current_rule_index]
        current_name = current_rule.get("name", "")

        rule_name = self.rule_name_edit.text().strip()
        if not rule_name:
            rule_name = current_name

        try:
            weight = float(self.rule_weight_edit.text())
        except ValueError:
            weight = 1.0

        connection = 1 if self.and_radio_button.isChecked() else 0

        antecedent = []
        is_mf = []

        for i, dropdown in enumerate(self.input_dropdowns):
            mf_index = dropdown.currentData()
            antecedent.append(mf_index if mf_index is not None else 0)
            is_not = 1 if self.input_is_dropdowns[i].currentText() == self.t("IS") else -1
            is_mf.append(is_not)

        consequent = []
        for i, dropdown in enumerate(self.output_dropdowns):
            mf_index = dropdown.currentData()
            consequent.append(mf_index if mf_index is not None else 0)
            is_not = 1 if self.output_is_dropdowns[i].currentText() == self.t("IS") else -1
            is_mf.append(is_not)

        success = self.view_model.update_rule(
            self._current_rule_index,
            antecedent,
            consequent,
            weight,
            connection,
            is_mf,
        )

        if success and rule_name != current_name:
            self.view_model.update_rule_name(self._current_rule_index, rule_name)

    def _on_antecedent_changed(self):
        """Handle antecedent dropdown changes."""
        if self._updating_rule or self._current_rule_index < 0:
            return
        self._on_update_rule_clicked()

    def _on_consequent_changed(self):
        """Handle consequent dropdown changes."""
        if self._updating_rule or self._current_rule_index < 0:
            return
        self._on_update_rule_clicked()
