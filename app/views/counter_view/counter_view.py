from PyQt6.QtWidgets import QLabel, QPushButton, QVBoxLayout

from app.view_models.base_view_model import BaseViewModel
from app.view_models.counter_view_model import CounterViewModel
from app.views.base_view import BaseView


class CounterView(BaseView):
    """View for displaying and interacting with the counter."""

    view_model: BaseViewModel
    layout_: QVBoxLayout
    label: QLabel
    button: QPushButton

    def __init__(self, view_model: CounterViewModel):
        """Initialize the counter view.

        Args:
            view_model (CounterViewModel): The view model for the counter view.
        """
        super().__init__(qss_filename="counter_view/counter_view.qss")
        self._view_model = view_model
        # Use self.t for translations and self.theme_manager for theming as needed
        self.init_ui()

    def init_ui(self) -> None:
        """Initialize the UI components for the counter view."""
        self.layout_ = QVBoxLayout()
        self.label = QLabel("0")
        self.button = QPushButton("Increment")
        self.button.clicked.connect(self._view_model.increment)
        self.layout_.addWidget(self.label)
        self.layout_.addWidget(self.button)
        self.setLayout(self.layout_)

    def update_label(self, count: int) -> None:
        """Update the label to show the current count.

        Args:
            count (int): The current count value.
        """
        self.label.setText(str(count))

    def update_button(self, is_enabled: bool) -> None:
        """Enable or disable the increment button.

        Args:
            is_enabled (bool): Whether the button should be enabled.
        """
        self.button.setEnabled(is_enabled)
