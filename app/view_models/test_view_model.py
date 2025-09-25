from typing import Any

from app.view_models.base_view_model import BaseViewModel


class TestViewModel(BaseViewModel):
    """A simple test view model for demonstration purposes."""

    model: Any

    def __init__(self, model: Any) -> None:
        """Initialize the TestViewModel.

        Args:
            model (Any): The model instance for the test view.
        """
        super().__init__()
        self._model = model
        # Add any additional initialization or properties as needed
