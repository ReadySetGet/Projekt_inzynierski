from PyQt6 import QtWidgets

from app.view_models.settings_view_model import SettingsViewModel
from app.views.base_widget_view import BaseWidgetView


class SettingsView(BaseWidgetView):
    """Class used to display settings window widget.

    It does not have a Parent attribute as to be displayed in a separate window.
    """

    styles = ["Light", "Dark", "Blue", "Red", "Green"]

    def __init__(self, view_model: SettingsViewModel = None):
        """Initialize the settings view widget.

        Args:
            view_model (SettingsViewModel, optional): The view model for this view.
        """
        super().__init__()
        self.setObjectName("settings")
        self.view_model = view_model if view_model else SettingsViewModel()
        self._setup_ui()
        self._setup_connections()
        self._retranslate_ui()
        self._load_initial_data()

    def _setup_ui(self):
        self.resize(400, 150)
        self.setWindowTitle(self.t("SETTINGS"))

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        form_layout = QtWidgets.QFormLayout()
        form_layout.setSpacing(15)

        self.theme_label = QtWidgets.QLabel()
        self.theme_label.setObjectName("theme_label")
        self.theme_dropdown = QtWidgets.QComboBox()
        self.theme_dropdown.setObjectName("theme_dropdown")
        form_layout.addRow(self.theme_label, self.theme_dropdown)

        self.language_label = QtWidgets.QLabel()
        self.language_label.setObjectName("language_label")
        self.language_dropdown = QtWidgets.QComboBox()
        self.language_dropdown.setObjectName("language_dropdown")
        form_layout.addRow(self.language_label, self.language_dropdown)

        main_layout.addLayout(form_layout)

        self.apply_button = QtWidgets.QPushButton()
        self.apply_button.setObjectName("apply_button")
        main_layout.addWidget(self.apply_button)

    def _retranslate_ui(self):
        self.theme_label.setText(self.t("THEME"))
        self.language_label.setText(self.t("LANGUAGE"))
        self.apply_button.setText(self.t("APPLY"))

    def _setup_connections(self):
        """Setup connections between view and view model."""
        # Connect dropdown changes to handlers
        self.apply_button.clicked.connect(self._on_apply_settings)

        # Connect view model signals to update UI
        self.view_model.theme_list_changed.connect(self._update_theme_list)
        self.view_model.language_list_changed.connect(self._update_language_list)
        self.view_model.current_theme_changed.connect(self._on_current_theme_changed)
        self.view_model.current_language_changed.connect(self._on_current_language_changed)

    def _load_initial_data(self):
        """Load initial data from view model."""
        # Load available themes and languages
        themes = self.view_model.get_available_themes()
        languages = self.view_model.get_available_languages()

        self._update_theme_list(themes)
        self._update_language_list(languages)

        # Set current selections
        current_theme = self.view_model.get_current_theme()
        current_language = self.view_model.get_current_language()

        if current_theme:
            index = self.theme_dropdown.findText(current_theme)
            if index >= 0:
                self.theme_dropdown.setCurrentIndex(index)

        if current_language:
            index = self.language_dropdown.findText(current_language)
            if index >= 0:
                self.language_dropdown.setCurrentIndex(index)

    def _update_theme_list(self, themes: list[str]):
        """Update the theme dropdown with available themes.

        Args:
            themes (list[str]): List of available theme names.
        """
        current_text = self.theme_dropdown.currentText()
        self.theme_dropdown.clear()
        self.theme_dropdown.addItems(themes)

        # Restore selection if possible
        if current_text:
            index = self.theme_dropdown.findText(current_text)
            if index >= 0:
                self.theme_dropdown.setCurrentIndex(index)

    def _update_language_list(self, languages: list[str]):
        """Update the language dropdown with available languages.

        Args:
            languages (list[str]): List of available language codes.
        """
        current_text = self.language_dropdown.currentText()
        self.language_dropdown.clear()
        self.language_dropdown.addItems(languages)

        # Restore selection if possible
        if current_text:
            index = self.language_dropdown.findText(current_text)
            if index >= 0:
                self.language_dropdown.setCurrentIndex(index)

    def _on_apply_settings(self):
        """Apply the selected theme and language settings."""
        selected_theme = self.theme_dropdown.currentText()
        selected_language = self.language_dropdown.currentText()

        if selected_theme:
            self.view_model.set_theme(selected_theme)

        if selected_language:
            self.view_model.set_language(selected_language)
            # Update all UI text after language change
            self._retranslate_ui()

    def _on_current_theme_changed(self, theme_name: str):
        """Handle theme change from view model.

        Args:
            theme_name (str): The new theme name.
        """
        index = self.theme_dropdown.findText(theme_name)
        if index >= 0:
            self.theme_dropdown.setCurrentIndex(index)

    def _on_current_language_changed(self, language_code: str):
        """Handle language change from view model.

        Args:
            language_code (str): The new language code.
        """
        index = self.language_dropdown.findText(language_code)
        if index >= 0:
            self.language_dropdown.setCurrentIndex(index)
        # Update all UI text after language change
        self._retranslate_ui()
