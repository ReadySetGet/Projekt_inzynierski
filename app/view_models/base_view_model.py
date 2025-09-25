from typing import Callable, Optional

from PyQt6.QtCore import QObject

from app.app_context import AppContext


class BaseViewModel(QObject):
    """Base class for all view models.

    Uses a class-level context provider for dependency injection. You can
    override the context by passing it explicitly.
    """

    _context_provider: Optional[Callable[[], AppContext]] = None

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
