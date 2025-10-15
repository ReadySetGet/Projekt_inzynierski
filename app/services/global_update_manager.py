"""Global update manager for coordinating updates across all components."""

from typing import List, Optional

from PyQt6.QtCore import QObject, pyqtSignal

from app.view_models.base_view_model import BaseViewModel
from app.views.base_tab_view import BaseTabView  # noqa: F401
from app.views.base_view import BaseView


class GlobalUpdateManager(QObject):
    """Manages global updates across all views and view models."""

    # Global update signals
    system_wide_update_requested = pyqtSignal()
    data_refresh_requested = pyqtSignal()
    ui_refresh_requested = pyqtSignal()

    def __init__(self, parent: Optional[QObject] = None) -> None:
        """Initialize the GlobalUpdateManager.

        Args:
            parent: Parent QObject
        """
        super().__init__(parent)
        self._registered_view_models: List[BaseViewModel] = []
        self._registered_views: List[BaseView] = []

    def register_view_model(self, view_model: BaseViewModel) -> None:
        """Register a view model for global updates.

        Args:
            view_model: The view model to register
        """
        if view_model not in self._registered_view_models:
            self._registered_view_models.append(view_model)
            # Connect the view model's signals to our global signals
            view_model.global_update_requested.connect(
                self._on_view_model_update_requested
            )
            view_model.data_changed.connect(self._on_view_model_data_changed)

    def register_view(self, view) -> None:
        """Register a view for global updates.

        Args:
            view: The view to register (BaseView or BaseTabView)
        """
        if view not in self._registered_views:
            self._registered_views.append(view)
            # Connect the view's signals to our global signals
            if hasattr(view, "global_update_requested"):
                view.global_update_requested.connect(self._on_view_update_requested)
            if hasattr(view, "ui_refresh_needed"):
                view.ui_refresh_needed.connect(self._on_view_ui_refresh_needed)

    def unregister_view_model(self, view_model: BaseViewModel) -> None:
        """Unregister a view model from global updates.

        Args:
            view_model: The view model to unregister
        """
        if view_model in self._registered_view_models:
            self._registered_view_models.remove(view_model)
            # Disconnect signals
            try:
                view_model.global_update_requested.disconnect(
                    self._on_view_model_update_requested
                )
                view_model.data_changed.disconnect(self._on_view_model_data_changed)
            except TypeError:
                pass  # Signal was not connected

    def unregister_view(self, view) -> None:
        """Unregister a view from global updates.

        Args:
            view: The view to unregister (BaseView or BaseTabView)
        """
        if view in self._registered_views:
            self._registered_views.remove(view)
            # Disconnect signals
            try:
                if hasattr(view, "global_update_requested"):
                    view.global_update_requested.disconnect(
                        self._on_view_update_requested
                    )
                if hasattr(view, "ui_refresh_needed"):
                    view.ui_refresh_needed.disconnect(self._on_view_ui_refresh_needed)
            except TypeError:
                pass  # Signal was not connected

    def request_system_wide_update(self) -> None:
        """Request a system-wide update across all registered components."""
        self.system_wide_update_requested.emit()
        # Trigger updates on all registered components
        for view_model in self._registered_view_models:
            view_model.refresh_data()
        for view in self._registered_views:
            view.handle_global_update()

    def request_data_refresh(self) -> None:
        """Request a data refresh across all registered view models."""
        self.data_refresh_requested.emit()
        for view_model in self._registered_view_models:
            view_model.refresh_data()

    def request_ui_refresh(self) -> None:
        """Request a UI refresh across all registered views."""
        self.ui_refresh_requested.emit()
        for view in self._registered_views:
            view.handle_global_update()

    def _on_view_model_update_requested(self) -> None:
        """Handle update request from a view model."""
        self.request_system_wide_update()

    def _on_view_model_data_changed(self) -> None:
        """Handle data change notification from a view model."""
        # Don't automatically trigger UI refresh to avoid circular calls
        pass

    def _on_view_update_requested(self) -> None:
        """Handle update request from a view."""
        # Don't automatically trigger system-wide updates to avoid circular calls
        pass

    def _on_view_ui_refresh_needed(self) -> None:
        """Handle UI refresh request from a view."""
        # Don't automatically trigger UI refresh to avoid circular calls
        pass

    def get_registered_count(self) -> dict:
        """Get the count of registered components.

        Returns:
            Dictionary with counts of registered view models and views
        """
        return {
            "view_models": len(self._registered_view_models),
            "views": len(self._registered_views),
        }
