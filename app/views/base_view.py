"""Base class for all views with dependency injection for AppContext."""

import os
from typing import Callable, Optional

from PyQt6.QtWidgets import QWidget

from app.app_context import AppContext
from app.utils.paths import local_path


class BaseView(QWidget):
    """Base class for all views with AppContext dependency injection.

    - Uses a class-level context provider for dependency injection.
    - Applies local stylesheet if exists and updates on theme change.
    - Sets up translation function (self.t) from AppContext.
    - Subclasses should call super().__init__(context, qss_filename) and use self.t
      for translations.
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
        self,
        context: AppContext | None = None,
        qss_filename: Optional[str] = None,
        parent: QWidget | None = None,
    ) -> None:
        """Initialize the BaseView with an optional context and QSS filename.

        Args:
            context (optional): The AppContext instance. If not provided, uses the
                provider.
            qss_filename (Optional[str]): The QSS file to use for styling.
            parent (Optional[QWidget]): The parent QWidget, if any.

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
                "No AppContext provided or set as provider for BaseView."
            )
        self.theme_manager = self.context.theme_manager
        self.qss_filename = qss_filename
        # Translation function from context
        self.t = self.context.translate
        # Theme support
        if self.theme_manager:
            self.theme_manager.theme_changed.connect(self.reload_stylesheet)
            self.reload_stylesheet()

    def reload_stylesheet(self) -> None:
        """Reload and apply the local stylesheet if qss_filename is set and exists."""
        if self.qss_filename:
            # Use absolute path if provided, otherwise resolve relative to this file
            if os.path.isabs(self.qss_filename) and os.path.exists(self.qss_filename):
                qss_path = self.qss_filename
            else:
                qss_path = str(local_path(__file__, self.qss_filename))
            if os.path.exists(qss_path):
                qss = self.theme_manager.load_stylesheet_with_theme(qss_path)
                if qss:
                    self.setStyleSheet(qss)
                else:
                    self.setStyleSheet("")
            else:
                self.setStyleSheet("")
        else:
            self.setStyleSheet("")
