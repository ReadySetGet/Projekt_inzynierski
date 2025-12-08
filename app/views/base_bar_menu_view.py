"""Base class for all frame views with MVVM architecture."""

import os
from typing import Optional

from PyQt6.QtWidgets import QMenuBar

from app.utils.paths import local_path


class BaseBarMenuView(QMenuBar):
    """Base class for all frame views with MVVM architecture.

    - Expects a view model to be set after initialization.
    - Applies local stylesheet if exists and updates on theme change.
    - Subclasses should set a view model and connect to its signals.
    """

    def __init__(
        self,
        qss_filename: Optional[str] = None,
        parent: QMenuBar | None = None,
    ) -> None:
        """Initialize the BaseFrameView with an optional QSS filename.

        Args:
            qss_filename (Optional[str]): The QSS file to use for styling.
            parent (Optional[QMenuBar]): The parent widget, if any.
        """
        super().__init__(parent=parent)
        self.qss_filename = qss_filename
        self.view_model = None

    def set_view_model(self, view_model) -> None:
        """Set the view model and connect to its signals.

        Args:
            view_model: The view model instance.
        """
        self.view_model = view_model
        self.view_model.theme_changed.connect(self.reload_stylesheet)
        self.view_model.translate_manager.language_changed.connect(self._on_language_changed)
        self.reload_stylesheet()

    def reload_stylesheet(self) -> None:
        """Reload and apply the local stylesheet if qss_filename is set and exists."""
        if self.qss_filename and self.view_model:
            if os.path.isabs(self.qss_filename) and os.path.exists(self.qss_filename):
                qss_path = self.qss_filename
            else:
                qss_path = str(local_path(__file__, self.qss_filename))
            if os.path.exists(qss_path):
                qss = self.view_model.load_stylesheet_with_theme(qss_path)
                if qss:
                    self.setStyleSheet(qss)
                else:
                    self.setStyleSheet("")
            else:
                self.setStyleSheet("")
        else:
            self.setStyleSheet("")

    def t(self, key: str) -> str:
        """Get translation for a key via view model."""
        return self.view_model.t(key)

    def handle_global_update(self) -> None:
        """Handle global update request."""
        self.refresh_ui()
        self.update_ui()

    def _on_language_changed(self) -> None:
        """Handle language change event."""
        self._retranslate_ui()
