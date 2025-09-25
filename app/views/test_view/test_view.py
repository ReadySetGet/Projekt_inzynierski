from app.view_models.base_view_model import BaseViewModel
from app.views.base_view import BaseView


class TestView(BaseView):
    """A simple test view for demonstration purposes."""

    view_model: BaseViewModel

    def __init__(self, view_model: BaseViewModel):
        """Initialize the test view.

        Args:
            view_model: The view model for the test view.
        """
        super().__init__(qss_filename="test_view/test_view.qss")
        self._view_model = view_model
        # Use self.t for translations and self.theme_manager for theming as needed
