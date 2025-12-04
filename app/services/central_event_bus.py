"""Global update manager for coordinating updates across all components."""

from typing import TYPE_CHECKING, List, Optional

from PyQt6.QtCore import QObject, pyqtSignal

if TYPE_CHECKING:
    from app.view_models.base_view_model import BaseViewModel


class CentralEventBus(QObject):
    """Manages global updates across all views and view models."""

    # Global update signals
    data_refresh_requested = pyqtSignal()

    def __init__(self, parent: Optional[QObject] = None) -> None:
        """Initialize the GlobalUpdateManager.

        Args:
            parent: Parent QObject
        """
        super().__init__(parent)
        self._registered_view_models: List["BaseViewModel"] = []

    def register_view_model(self, view_model: "BaseViewModel") -> None:
        """Register a view model for global updates.

        Args:
            view_model: The view model to register
        """
        if view_model not in self._registered_view_models:
            self._registered_view_models.append(view_model)
            view_model.notify_data_changed.connect(self._request_data_refresh)

    def _request_data_refresh(self) -> None:
        """Request a data refresh across all registered view models."""
        for view_model in self._registered_view_models:
            view_model.data_changed.emit()
