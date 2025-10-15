from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import QMainWindow

from app.app_context import AppContext
from app.services.global_update_manager import GlobalUpdateManager
from app.utils.config import AppConfig
from app.utils.paths import local_path
from app.utils.shortcut_manager import ShortcutManager
from app.view_models.browser_frame_view_model import BrowserFrameViewModel
from app.view_models.central_tab_view_model import CentralTabViewModel
from app.view_models.editor_tab_view_model import EditorTabViewModel
from app.view_models.top_menu_view_model import TopMenuViewModel
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
            self.setupUi()

            # Initialize the new view system (keeping for compatibility)
            # view_model = MainViewModel(model)
            # Note: We're not setting MainView as central widget since we
            # have our own UI

            # Theme support
            self.context.theme_manager.theme_changed.connect(self.reload_stylesheet)
            self.reload_stylesheet()

            # Shortcut Manager integration
            self.shortcut_manager = ShortcutManager(self)
            # register_default_shortcuts(
            #    self.shortcut_manager, view_model, self._toggle_theme
            # )

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

    def setupUi(self):
        """Set up the UI for the main window."""
        self.setObjectName("MainWindow")
        self.resize(1096, 830)

        self.centralwidget = QtWidgets.QWidget(parent=self)
        self.centralwidget.setObjectName("centralwidget")

        # Create global update manager
        self.global_update_manager = GlobalUpdateManager(self)

        # Create view models first
        self.top_menu_view_model = TopMenuViewModel(self.context)
        self.browser_frame_view_model = BrowserFrameViewModel(self.context)
        self.central_tab_view_model = CentralTabViewModel(self.context)
        self.editor_tab_view_model = EditorTabViewModel(self.context)

        # Create widgets with their respective view models
        self.plotTabs = CentralTabWidget(
            self.central_tab_view_model, parent=self.centralwidget
        )
        self.plotTabs.setGeometry(QtCore.QRect(310, 160, 531, 641))

        self.browserFrame = BrowserFrameWidget(
            self.browser_frame_view_model, parent=self.centralwidget
        )
        self.browserFrame.setGeometry(QtCore.QRect(0, 160, 301, 641))

        self.upMenuTab = TopMenu(self.top_menu_view_model, parent=self.centralwidget)
        self.upMenuTab.setGeometry(QtCore.QRect(0, 0, 1081, 161))

        self.editorTab = EditorTabWidget(
            self.editor_tab_view_model, parent=self.centralwidget
        )
        self.editorTab.setGeometry(QtCore.QRect(820, 160, 281, 641))

        if hasattr(self.editorTab, "mf_properties_tab"):
            central_fuzzy_service = self.plotTabs.get_fuzzy_service()
            if hasattr(self.editorTab.mf_properties_tab, "fuzzy_service"):
                self.editorTab.mf_properties_tab.fuzzy_service = central_fuzzy_service
                fis_model = central_fuzzy_service.get_fis_model()
                self.editorTab.mf_properties_tab.view_model.model = fis_model
                self.editorTab.mf_properties_tab._connect_fuzzy_service_signals()

            self.plotTabs.connect_mf_editor(self.editorTab.mf_properties_tab)

        # Register components with global update manager
        self.global_update_manager.register_view_model(self.central_tab_view_model)
        self.global_update_manager.register_view(self.plotTabs)
        if hasattr(self.editorTab, "mf_properties_tab"):
            self.global_update_manager.register_view_model(
                self.editorTab.mf_properties_tab.view_model
            )
            self.global_update_manager.register_view(self.editorTab.mf_properties_tab)

        self.setCentralWidget(self.centralwidget)

        self.retranslateUi()
        self.plotTabs.setCurrentIndex(2)
        self.upMenuTab.setCurrentIndex(0)
        self.editorTab.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(self)

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
