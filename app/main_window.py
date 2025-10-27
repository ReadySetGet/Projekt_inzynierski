from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import QMainWindow

from app.app_context import AppContext

# CentralEventBus is now accessed through context.event_bus
from app.utils.config import AppConfig
from app.utils.paths import local_path
from app.utils.shortcut_manager import ShortcutManager
from app.view_models.browser_frame_view_model import BrowserFrameViewModel
from app.view_models.central_tab_view_model import CentralTabViewModel
from app.view_models.editor_tab_view_model import EditorTabViewModel
from app.view_models.top_menu_view_model import TopMenuViewModel
from app.views.bar_menu_view import BarMenuWidget
from app.views.browser_frame_view import BrowserFrameWidget
from app.views.central_tab_view import CentralTabWidget
from app.views.editor_tab_view import EditorTabWidget
from app.views.top_menu_view import TopMenu


class MainWindow(QMainWindow):
    """Main application window for the PyQt app."""

    def __init__(self, context: AppContext = None) -> None:
        """Initialize the Main-Window.

        Args:
            context (AppContext, optional): The application context.
                If None, uses AppConfig.
        """
        super().__init__()
        self.context = context

        # Window-Settings
        if context:
            self.setWindowTitle(context.config.app_name())
            self.resize(context.config.window_width(), context.config.window_height())
        else:
            self.setWindowTitle(AppConfig.app_name())
            self.resize(AppConfig.window_width(), AppConfig.window_height())

        # Initialize UI components if context is available
        if context:
            # Set up the main UI
            self.setupViewModels()
            self.setupUi()

            # Theme support
            self.context.theme_manager.theme_changed.connect(self.reload_stylesheet)
            self.reload_stylesheet()

            # Translation support
            self.context.translate_manager.language_changed.connect(self.retranslate_ui)
            self.context.translate_manager.set_language("en")
            # Shortcut Manager integration
            self.shortcut_manager = ShortcutManager(self)

    def _toggle_theme(self):
        """Toggle between available themes (example logic)."""
        if self.context:
            themes = self.context.theme_manager.available_themes()
            current = self.context.theme_manager.current_theme()
            if themes:
                idx = themes.index(current) if current in themes else 0
                next_idx = (idx + 1) % len(themes)
                self.context.theme_manager.set_theme(themes[next_idx])

    def list_shortcuts(self):
        """List all registered shortcuts in the manager.

        Returns:
            list: List of (key_sequence, action) tuples for registered shortcuts.
        """
        if hasattr(self, "shortcut_manager"):
            return self.shortcut_manager.list_shortcuts()
        return []

    def update_shortcut(self, old_seq: str, new_seq: str) -> bool:
        """Update a shortcut at runtime.

        Args:
            old_seq (str): The old key sequence.
            new_seq (str): The new key sequence.

        Returns:
            bool: True if updated, False otherwise.
        """
        if hasattr(self, "shortcut_manager"):
            return self.shortcut_manager.update_shortcut(old_seq, new_seq)
        return False

    def remove_shortcut(self, seq: str) -> bool:
        """Remove a shortcut at runtime.

        Args:
            seq (str): The key sequence to remove.

        Returns:
            bool: True if removed, False otherwise.
        """
        if hasattr(self, "shortcut_manager"):
            return self.shortcut_manager.remove_shortcut(seq)
        return False

    def setupViewModels(self):
        """Setup the view models for the main window."""
        self.central_tab_view_model = CentralTabViewModel()
        self.editor_tab_view_model = EditorTabViewModel()
        self.browser_frame_view_model = BrowserFrameViewModel()
        self.top_menu_view_model = TopMenuViewModel()

    def setupUi(self):
        """Set up the UI for the main window."""
        self.setObjectName("MainWindow")
        self.resize(1096, 780)
        self.central_widget = QtWidgets.QWidget(parent=self)
        self.central_widget.setObjectName("centralwidget")

        self.statusBar = QtWidgets.QStatusBar(parent=self)
        self.statusBar.setObjectName("statusbar")
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Started application")

        self.plotTabs = CentralTabWidget(parent=self.central_widget, status_bar=self.statusBar)
        self.plotTabs.setGeometry(QtCore.QRect(310, 160, 531, 601))

        self.browserFrame = BrowserFrameWidget(parent=self.central_widget, status_bar=self.statusBar)
        self.browserFrame.setGeometry(QtCore.QRect(0, 160, 301, 641))

        self.upMenuTab = TopMenu(parent=self.central_widget, status_bar=self.statusBar)
        self.upMenuTab.setGeometry(QtCore.QRect(0, 0, 1081, 161))

        self.editorTab = EditorTabWidget(parent=self.central_widget, status_bar=self.statusBar)
        self.editorTab.setGeometry(QtCore.QRect(820, 160, 281, 641))

        self.setCentralWidget(self.central_widget)

        self.menuBar = BarMenuWidget(parent=self)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1096, 26))

        """Sets up the default tabs of tab widgets."""
        self.plotTabs.setCurrentIndex(0)
        self.upMenuTab.setCurrentIndex(0)
        self.editorTab.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(self)

        # Connect view models to widgets
        self._connect_view_models()

    def retranslate_ui(self):
        """Retranslate all UI elements when language changes."""
        # Retranslate main window
        if hasattr(self, "context") and self.context:
            self.setWindowTitle(self.context.translate_manager.t("MainWindow"))
        else:
            _translate = QtCore.QCoreApplication.translate
            self.setWindowTitle(_translate("MainWindow", "MainWindow"))

        # Retranslate all child widgets that have _retranslate_ui method
        self._retranslate_widget(self)

    def _retranslate_widget(self, widget):
        """Recursively retranslate all child widgets."""
        if hasattr(widget, "_retranslate_ui"):
            widget._retranslate_ui()

        for child in widget.findChildren(QtWidgets.QWidget):
            if hasattr(child, "_retranslate_ui"):
                child._retranslate_ui()

    def retranslateUi(self):
        """Retranslate the UI text."""
        if hasattr(self, "context") and self.context:
            self.setWindowTitle(self.context.translate("MainWindow"))
        else:
            _translate = QtCore.QCoreApplication.translate
            self.setWindowTitle(_translate("MainWindow", "MainWindow"))

    def reload_stylesheet(self) -> None:
        """Reload the stylesheet for the main window."""
        if self.context:
            qss_path = local_path(__file__, "stylesheet.qss")
            qss = self.context.theme_manager.load_stylesheet_with_theme(str(qss_path))
            self.setStyleSheet(qss)

    def _connect_view_models(self) -> None:
        """Connect view models to their respective widgets."""
        # Properly connect view models to widgets using set_view_model method
        self.plotTabs.set_view_model(self.central_tab_view_model)
        self.browserFrame.set_view_model(self.browser_frame_view_model)
        self.upMenuTab.set_view_model(self.top_menu_view_model)
        self.editorTab.set_view_model(self.editor_tab_view_model)
