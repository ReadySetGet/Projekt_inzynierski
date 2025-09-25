from PyQt6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from app.view_models.main_view_model import MainViewModel
from app.views.base_view import BaseView


class MainView(BaseView):
    """Main view for the application UI."""

    _view_model: MainViewModel
    _main_layout: QVBoxLayout
    _stacked_widget: QStackedWidget
    _button_home: QPushButton
    _button_settings: QPushButton
    _language_selector: QComboBox
    _theme_selector: QComboBox

    def __init__(self, view_model: MainViewModel) -> None:
        """Initialize the main view.

        Args:
            view_model (MainViewModel): The view model for the main view.
        """
        super().__init__(qss_filename="main_view/main_view.qss")
        self._view_model = view_model
        self.t = self.context.translate

        # Connect Signals to Slots
        self._view_model.current_view_changed.connect(self.change_view)
        if hasattr(self._view_model, "language_changed"):
            self._view_model.language_changed.connect(self.update_translations)

        # Initialize the UI
        self.init_ui()

    def init_ui(self) -> None:
        """Initialize the UI components for the main view."""
        self._main_layout = QVBoxLayout()  # Vertical layout
        self.setLayout(self._main_layout)

        # Create Widgets
        navbar_layout = self.init_navbar()
        self._stacked_widget = QStackedWidget()

        # Add Widgets to View
        self._main_layout.addWidget(navbar_layout)
        self._main_layout.addWidget(self._stacked_widget)

    def init_navbar(self) -> QWidget:
        """Initialize the navigation bar for the main view.

        Returns:
            QWidget: The navigation bar widget.
        """
        navbar_layout = QHBoxLayout()

        # Create Widgets
        self._button_home = QPushButton(self.t(self._view_model.home_label))
        self._button_settings = QPushButton(self.t(self._view_model.settings_label))

        # Language selector
        self._language_selector = QComboBox()
        self._language_selector.addItems(self._view_model.available_languages)
        self._language_selector.currentTextChanged.connect(
            self._view_model.set_language
        )

        # Theme selector
        self._theme_selector = QComboBox()
        self._theme_selector.addItems(self._view_model.available_themes)
        self._theme_selector.currentTextChanged.connect(self._view_model.set_theme)
        # Set current theme if available
        current_theme = self._view_model.current_theme
        if current_theme:
            idx = self._theme_selector.findText(current_theme)
            if idx >= 0:
                self._theme_selector.setCurrentIndex(idx)

        # Bind Commands
        self._button_home.clicked.connect(
            lambda: self._view_model.set_current_view("home")
        )
        self._button_settings.clicked.connect(
            lambda: self._view_model.set_current_view("settings")
        )

        # Add Widgets to Layout
        navbar_layout.addWidget(self._button_home)
        navbar_layout.addWidget(self._button_settings)
        navbar_layout.addStretch()
        navbar_layout.addWidget(self._language_selector)
        navbar_layout.addWidget(self._theme_selector)

        # Encapsulate in QWidget
        navbar_widget = QWidget()
        navbar_widget.setLayout(navbar_layout)
        navbar_widget.setFixedHeight(100)

        return navbar_widget

    def change_view(self, widget: QWidget) -> None:
        """Change the current view in the stacked widget.

        Args:
            widget (QWidget): The widget to display.
        """
        index = self._stacked_widget.indexOf(widget)
        if index == -1:
            self._stacked_widget.addWidget(widget)
            index = self._stacked_widget.indexOf(widget)
        self._stacked_widget.setCurrentIndex(index)

    def update_translations(self, language_code: str) -> None:
        """Update UI text when language changes.

        Args:
            language_code (str): The new language code.
        """
        self._button_home.setText(self.t(self._view_model.home_label))
        self._button_settings.setText(self.t(self._view_model.settings_label))
