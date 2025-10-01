from PyQt6 import QtWidgets

from app.view_models.base_view_model import BaseViewModel
from app.views.base_tab_view import BaseTabView
from app.views.mf_editor_tab import MFPropertiesWidget
from app.views.rules_editor_tab import RulesEditorTab


class EditorTabWidget(BaseTabView):
    """Editor tab widget for editing system properties."""

    view_model: BaseViewModel

    def __init__(self, view_model: BaseViewModel, parent=None):
        """Initialize the editor tab widget.

        Args:
            view_model: The view model for the editor tab widget.
            parent: The parent widget.
        """
        super().__init__(parent=parent)
        self._view_model = view_model
        self.setObjectName("editorTab")
        self._setup_ui()
        self._retranslate_ui()

    def _setup_ui(self):
        self.fis_properties_tab = QtWidgets.QWidget()
        self.fis_properties_tab.setObjectName("fis_properties_tab")

        self.addTab(self.fis_properties_tab, "fis_properties_tab")

        self.mf_properties_tab = MFPropertiesWidget()
        self.mf_properties_tab.setObjectName("mf_properties_tab")

        self.addTab(self.mf_properties_tab, "mf_properties_tab")

        self.rule_editor_tab = RulesEditorTab(parent=self)
        self.rule_editor_tab.setObjectName("rule_editor_tab")

        self.addTab(self.rule_editor_tab, "rule_editor_tab")

        self._retranslate_ui()

    def _retranslate_ui(self):
        self.setTabText(
            self.indexOf(self.fis_properties_tab),
            self.t("fisPropertiesTab"),
        )
        self.setTabText(
            self.indexOf(self.mf_properties_tab),
            self.t("mfPropertiesTab"),
        )
        self.setTabText(
            self.indexOf(self.rule_editor_tab),
            self.t("rulePropertiesTab"),
        )
