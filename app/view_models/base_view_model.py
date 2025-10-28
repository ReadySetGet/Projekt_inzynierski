from typing import Callable, Optional

from PyQt6.QtCore import QObject, pyqtSignal

from app.app_context import AppContext


class BaseViewModel(QObject):
    """Base class for all view models.

    Uses a class-level context provider for dependency injection. You can
    override the context by passing it explicitly.

    All subclasses should implement the abstract methods to ensure proper
    MVVM architecture and global update functionality.
    """

    _context_provider: Optional[Callable[[], AppContext]] = None

    # Global update signals
    data_changed = pyqtSignal()
    notify_data_changed = pyqtSignal()
    theme_changed = pyqtSignal()
    stylesheet_updated = pyqtSignal(str)  # Emits the stylesheet content

    @classmethod
    def set_context_provider(cls, provider: Callable[[], AppContext]) -> None:
        """Set the class-level context provider for dependency injection.

        Args:
            provider (Callable[[], AppContext]): A function returning the AppContext.
        """
        cls._context_provider = provider

    def __init__(self, parent: QObject | None = None) -> None:
        """Initialize the BaseViewModel.

        Args:
            parent (Optional[QObject]): The parent QObject, if any.
        """
        super().__init__(parent)
        self.data_changed.connect(self.refresh_data)

        # Register with event bus for global updates
        if self._context_provider:
            context = self._context_provider()
            if context and context.event_bus:
                context.event_bus.register_view_model(self)

        if self._context_provider:
            context = self._context_provider()
            if context and context.theme_manager:
                context.theme_manager.theme_changed.connect(self._on_theme_changed)

    @property
    def context(self) -> AppContext:
        """Get the AppContext via the context provider."""
        if self._context_provider is None:
            raise RuntimeError("No context provider set for BaseViewModel")
        return self._context_provider()

    @property
    def fuzzy_service(self):
        """Get the fuzzy calculation service."""
        return self.context.fuzzy_service

    @property
    def event_bus(self):
        """Get the central event bus."""
        return self.context.event_bus

    @property
    def theme_manager(self):
        """Get the theme manager."""
        return self.context.theme_manager

    @property
    def translate_manager(self):
        """Get the translation manager."""
        return self.context.translate_manager

    def t(self, key: str) -> str:
        """Get the translation for a key."""
        return self.translate_manager.t(key)

    def load_stylesheet_with_theme(self, qss_path: str) -> str:
        """Load stylesheet with current theme applied."""
        if self.theme_manager:
            return self.theme_manager.load_stylesheet_with_theme(qss_path)
        return ""

    def _on_theme_changed(self) -> None:
        """Handle theme change events."""
        self.theme_changed.emit()

    def refresh_data(self) -> None:
        """Refresh all data.

        Should only update logic, never emit notify_data_changed.
        This method should be overridden by subclasses.
        It should only update internal state/logic, not emit signals.
        """
        pass
