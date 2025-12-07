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

    def unregister_view_model(self, view_model: "BaseViewModel") -> None:
        """Unregister a view model from global updates.

        Args:
            view_model: The view model to unregister
        """
        if view_model in self._registered_view_models:
            try:
                view_model.notify_data_changed.disconnect(self._request_data_refresh)
            except Exception:
                pass
            self._registered_view_models.remove(view_model)

    def _request_data_refresh(self) -> None:
        """Request a data refresh across all registered view models."""
        view_models_to_remove = []
        for view_model in self._registered_view_models:
            try:
                view_model.data_changed.emit()
            except RuntimeError:
                view_models_to_remove.append(view_model)
        for view_model in view_models_to_remove:
            self._registered_view_models.remove(view_model)
