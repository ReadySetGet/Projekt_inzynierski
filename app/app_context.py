from typing import Optional

from app.services.theme_manager import ThemeManager
from app.services.translate_manager import TranslateManager
from app.utils.config import AppConfig
from app.utils.paths import LOCALES_DIR, THEMES_DIR


class AppContext:
    """Singleton context for global app services."""

    _instance: "Optional[AppContext]" = None
    _initialized: bool

    def __new__(cls, *args: object, **kwargs: object) -> "AppContext":
        """Create or return the singleton AppContext instance.

        Args:
            *args: Positional arguments.
            **kwargs: Keyword arguments.

        Returns:
            AppContext: The singleton instance.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """Initialize the AppContext with config, translation, and theme manager."""
        if hasattr(self, "_initialized") and self._initialized:
            return
        # Initialize config
        AppConfig.initialize()
        self.config = AppConfig

        # Initialize translation manager
        self.translate_manager = TranslateManager(
            str(LOCALES_DIR), default_language="en"
        )
        self.translate = self.translate_manager.t

        # Theme manager (not global)
        self.theme_manager = ThemeManager(str(THEMES_DIR))

        self._initialized = True


def get_app_context() -> AppContext:
    """Return the singleton AppContext instance.

    Returns:
        AppContext: The singleton instance.
    """
    return AppContext()
