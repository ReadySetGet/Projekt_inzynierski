"""View model for the settings view."""

from PyQt6.QtCore import pyqtSignal

from app.view_models.base_view_model import BaseViewModel


class SettingsViewModel(BaseViewModel):
    """View model for the settings view.

    Manages theme and language settings, providing a clean interface
    between the settings UI and the underlying services.
    """

    # Signals
    theme_list_changed = pyqtSignal(list)  # Emits list of available themes
    language_list_changed = pyqtSignal(list)  # Emits list of available languages
    current_theme_changed = pyqtSignal(str)  # Emits current theme name
    current_language_changed = pyqtSignal(str)  # Emits current language code

    def __init__(self) -> None:
        """Initialize the SettingsViewModel."""
        super().__init__()

        # Connect to service signals
        if self.theme_manager:
            self.theme_manager.theme_changed.connect(self._on_theme_changed_internal)

        if self.translate_manager:
            self.translate_manager.language_changed.connect(self._on_language_changed_internal)

    def get_available_themes(self) -> list[str]:
        """Get list of available themes.

        Returns:
            list[str]: List of theme names.
        """
        if self.theme_manager:
            return self.theme_manager.available_themes()
        return []

    def get_available_languages(self) -> list[str]:
        """Get list of available languages.

        Returns:
            list[str]: List of language codes.
        """
        if self.translate_manager:
            return self.translate_manager.available_languages()
        return []

    def get_current_theme(self) -> str:
        """Get the current theme name.

        Returns:
            str: Current theme name or empty string if not set.
        """
        if self.theme_manager:
            current = self.theme_manager.get_current_theme()
            return current if current else ""
        return ""

    def get_current_language(self) -> str:
        """Get the current language code.

        Returns:
            str: Current language code.
        """
        if self.translate_manager:
            return self.translate_manager.current_language
        return "en"

    def set_theme(self, theme_name: str) -> bool:
        """Set the application theme.

        Args:
            theme_name (str): The name of the theme to apply.

        Returns:
            bool: True if successful, False otherwise.
        """
        if self.theme_manager:
            success = self.theme_manager.set_theme(theme_name)
            if success:
                # Save to config if available
                if hasattr(self.context, "config") and self.context.config:
                    self.context.config.set_value("theme", "current", theme_name)
            return success
        return False

    def set_language(self, language_code: str) -> bool:
        """Set the application language.

        Args:
            language_code (str): The language code to set (e.g., 'en', 'pl').

        Returns:
            bool: True if successful, False otherwise.
        """
        if self.translate_manager:
            success = self.translate_manager.set_language(language_code)
            if success:
                # Save to config if available
                if hasattr(self.context, "config") and self.context.config:
                    self.context.config.set_value("language", "current", language_code)
                # Emit signal to notify all views to update their translations
                self.notify_data_changed.emit()
            return success
        return False

    def _on_theme_changed_internal(self) -> None:
        """Handle theme change from theme manager."""
        current_theme = self.get_current_theme()
        self.current_theme_changed.emit(current_theme)
        # Propagate to base class handler
        self._on_theme_changed()

    def _on_language_changed_internal(self) -> None:
        """Handle language change from translate manager."""
        current_language = self.get_current_language()
        self.current_language_changed.emit(current_language)

    def refresh_data(self) -> None:
        """Refresh settings data - updates internal state from services."""
        # Emit current states to update UI
        themes = self.get_available_themes()
        languages = self.get_available_languages()

        if themes:
            self.theme_list_changed.emit(themes)
        if languages:
            self.language_list_changed.emit(languages)

        current_theme = self.get_current_theme()
        if current_theme:
            self.current_theme_changed.emit(current_theme)

        current_lang = self.get_current_language()
        if current_lang:
            self.current_language_changed.emit(current_lang)
