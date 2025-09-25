from typing import Any

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QApplication, QWidget

from app.app_context import AppContext
from app.services.theme_manager import ThemeManager
from app.services.translate_manager import TranslateManager
from app.view_models.base_view_model import BaseViewModel
from app.view_models.counter_view_model import CounterViewModel
from app.view_models.test_view_model import TestViewModel
from app.views.counter_view.counter_view import CounterView
from app.views.test_view.test_view import TestView


class MainViewModel(BaseViewModel):
    """View model for the main view."""

    current_view_changed = pyqtSignal(QWidget)
    language_changed = pyqtSignal(str)

    _model: Any
    home_vm: CounterViewModel
    home_view: CounterView
    test_vm: TestViewModel
    test_view: TestView
    theme_manager: ThemeManager
    translate_manager: TranslateManager

    def __init__(self, model: Any, context: AppContext | None = None) -> None:
        """Initialize the main view model.

        Args:
            model (Any): The main model.
            context (Optional[AppContext]): The application context instance.
        """
        super().__init__(context)
        self._model = model
        self.theme_manager = self.context.theme_manager
        self.translate_manager = self.context.translate_manager

        self.home_vm = CounterViewModel(self._model)
        self.home_view = CounterView(self.home_vm)

        self.test_vm = TestViewModel(self._model)
        self.test_view = TestView(self._model)

    @property
    def available_languages(self) -> list[str]:
        """Return the list of available languages.

        Returns:
            list[str]: List of available languages.
        """
        return self.translate_manager.available_languages()

    @property
    def available_themes(self) -> list[str]:
        """Return the list of available themes.

        Returns:
            list[str]: List of available themes.
        """
        return self.theme_manager.available_themes()

    @property
    def current_theme(self) -> str:
        """Return the name of the current theme.

        Returns:
            str: The name of the current theme.
        """
        return self.theme_manager.get_current_theme() or ""

    @property
    def home_label(self) -> str:
        """Return the label for the home view.

        Returns:
            str: The label for the home view.
        """
        return "Home"

    @property
    def settings_label(self) -> str:
        """Return the label for the settings view.

        Returns:
            str: The label for the settings view.
        """
        return "Settings"

    def set_current_view(self, name: str) -> None:
        """Set the current view based on the given name.

        Args:
            name (str): The name of the view to display.
        """
        if name == "home":
            self.current_view_changed.emit(self.home_view)
        elif name == "settings":
            self.current_view_changed.emit(self.test_view)

    def set_language(self, language_code: str) -> None:
        """Set the application language.

        Args:
            language_code (str): The language code to set.
        """
        self.translate_manager.load_language(language_code)
        self.language_changed.emit(language_code)

    def set_theme(self, theme_name: str, app: QApplication | None = None) -> None:
        """Set the application theme by name.

        Args:
            theme_name (str): The name of the theme to apply.
            app: The QApplication instance (optional, only needed if changing app-wide
                theme).
        """
        if self.theme_manager:
            self.theme_manager.set_theme(theme_name, app)
