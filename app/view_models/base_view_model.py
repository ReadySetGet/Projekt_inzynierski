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
    global_update_requested = pyqtSignal()
    data_changed = pyqtSignal()

    @classmethod
    def set_context_provider(cls, provider: Callable[[], AppContext]) -> None:
        """Set the class-level context provider for dependency injection.

        Args:
            provider (Callable[[], AppContext]): A function returning the AppContext.
        """
        cls._context_provider = provider

    def __init__(
        self, context: AppContext | None = None, parent: QObject | None = None
    ) -> None:
        """Initialize the BaseViewModel with an optional context.

        Args:
            context (optional): The AppContext instance. If not provided, uses the
                provider.
            parent (Optional[QObject]): The parent QObject, if any.

        Raises:
            RuntimeError: If no context is provided or set as provider.
        """
        super().__init__(parent)
        if context is not None:
            self.context = context
        elif self._context_provider is not None:
            self.context = self._context_provider()
        else:
            raise RuntimeError(
                "No AppContext provided or set as provider for BaseViewModel."
            )

    def request_global_update(self) -> None:
        """Request a global update across all components."""
        self.global_update_requested.emit()

    def notify_data_changed(self) -> None:
        """Notify that data has changed and needs to be refreshed."""
        self.data_changed.emit()

    def update_data(self) -> None:
        """Update data from the model. Override in subclasses."""
        pass

    def refresh_data(self) -> None:
        """Refresh all data and notify of changes."""
        self.update_data()
        self.notify_data_changed()
