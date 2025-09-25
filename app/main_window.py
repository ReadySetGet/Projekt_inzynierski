from PyQt6.QtWidgets import QMainWindow

from app.app_context import AppContext
from app.models.counter_model import CounterModel
from app.utils.paths import local_path
from app.utils.shortcut_manager import ShortcutManager, register_default_shortcuts
from app.view_models.main_view_model import MainViewModel
from app.views.main_view.main_view import MainView


class MainWindow(QMainWindow):
    """Main application window for the PyQt app. xdf"""

    def __init__(self, context: AppContext) -> None:
        """Initialize the Main-Window.

        Args:
            context (AppContext): The application context.
        """
        super().__init__()
        self.context = context
        # Window-Settings
        self.setWindowTitle(self.context.config.app_name())
        self.resize(
            self.context.config.window_width(), self.context.config.window_height()
        )

        model = CounterModel()
        view_model = MainViewModel(model)
        view = MainView(view_model)
        self.setCentralWidget(view)
        view.show()

        # Theme support
        self.context.theme_manager.theme_changed.connect(self.reload_stylesheet)
        self.reload_stylesheet()

        # Shortcut Manager integration
        self.shortcut_manager = ShortcutManager(self)
        register_default_shortcuts(
            self.shortcut_manager, view_model, self._toggle_theme
        )

    def _toggle_theme(self):
        """Toggle between available themes (example logic)."""
        themes = self.context.theme_manager.available_themes()
        current = self.context.theme_manager.current_theme()
        if themes:
            idx = themes.index(current) if current in themes else 0
            next_idx = (idx + 1) % len(themes)
            self.context.theme_manager.set_theme(themes[next_idx])

    def list_shortcuts(self):
        """List all registered shortcuts in the manager.

        Returns:
            list: List of (key_sequence, action) tuples for registered shortcuts.
        """
        return self.shortcut_manager.list_shortcuts()

    def update_shortcut(self, old_seq: str, new_seq: str) -> bool:
        """Update a shortcut at runtime.

        Args:
            old_seq (str): The old key sequence.
            new_seq (str): The new key sequence.

        Returns:
            bool: True if updated, False otherwise.
        """
        return self.shortcut_manager.update_shortcut(old_seq, new_seq)

    def remove_shortcut(self, seq: str) -> bool:
        """Remove a shortcut at runtime.

        Args:
            seq (str): The key sequence to remove.

        Returns:
            bool: True if removed, False otherwise.
        """
        return self.shortcut_manager.remove_shortcut(seq)

    def reload_stylesheet(self) -> None:
        """Reload the stylesheet for the main window."""
        qss_path = local_path(__file__, "stylesheet.qss")
        qss = self.context.theme_manager.load_stylesheet_with_theme(str(qss_path))
        self.setStyleSheet(qss)
