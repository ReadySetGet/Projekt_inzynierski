"""Base class for all views with MVVM architecture."""

import os
from typing import Optional

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget

from app.utils.paths import local_path


class BaseWidgetView(QWidget):
    """Base class for all views with MVVM architecture.

    - Expects a view model to be set after initialization.
    - Applies local stylesheet if exists and updates on theme change.
    - Subclasses should set a view model and connect to its signals.

    All subclasses should implement the abstract methods to ensure proper
    MVVM architecture and global update functionality.
    """

    # Global update signals
    global_update_requested = pyqtSignal()
    ui_refresh_needed = pyqtSignal()

    def __init__(
        self,
        qss_filename: Optional[str] = None,
        parent: QWidget | None = None,
    ) -> None:
        """Initialize the BaseWidgetView with an optional QSS filename.

        Args:
            qss_filename (Optional[str]): The QSS file to use for styling.
            parent (Optional[QWidget]): The parent QWidget, if any.
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
        if self.view_model:
            self.view_model.theme_changed.connect(self.reload_stylesheet)
            self.view_model.data_changed.connect(self.refresh_ui)
            self.view_model.notify_data_changed.connect(self.update_ui)
            self.view_model.translate_manager.language_changed.connect(self._on_language_changed)
            # Initial stylesheet load
            self.reload_stylesheet()

    def reload_stylesheet(self) -> None:
        """Reload and apply the local stylesheet if qss_filename is set and exists."""
        if self.qss_filename and self.view_model:
            # Use absolute path if provided, otherwise resolve relative to this file
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
        if self.view_model:
            return self.view_model.t(key)
        return key

    def request_global_update(self) -> None:
        """Request a global update across all components."""
        self.global_update_requested.emit()

    def notify_ui_refresh_needed(self) -> None:
        """Notify that UI needs to be refreshed."""
        self.ui_refresh_needed.emit()

    def refresh_ui(self) -> None:
        """Refresh the UI. Override in subclasses."""
        pass

    def update_ui(self) -> None:
        """Update UI elements. Override in subclasses."""
        pass

    def handle_global_update(self) -> None:
        """Handle global update request."""
        self.refresh_ui()
        self.update_ui()

    def _on_language_changed(self) -> None:
        """Handle language change event."""
        if hasattr(self, "_retranslate_ui"):
            self._retranslate_ui()


# Alias for backward compatibility
BaseWidget = BaseWidgetView
