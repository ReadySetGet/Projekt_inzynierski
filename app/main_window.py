import os

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
        self.resize(1200, 800)

        # Create central widget with main layout
        self.central_widget = QtWidgets.QWidget(parent=self)
        self.central_widget.setObjectName("centralwidget")
        self.setCentralWidget(self.central_widget)

        # Create main vertical layout
        main_layout = QtWidgets.QVBoxLayout(self.central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Status bar
        self.statusBar = QtWidgets.QStatusBar(parent=self)
        self.statusBar.setObjectName("statusbar")
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Started application")

        # Top menu (fixed height)
        self.upMenuTab = TopMenu(parent=self.central_widget, status_bar=self.statusBar)
        self.upMenuTab.setFixedHeight(160)
        main_layout.addWidget(self.upMenuTab)

        # Create horizontal splitter for main content area
        main_splitter = QtWidgets.QSplitter(QtCore.Qt.Orientation.Horizontal)
        main_splitter.setObjectName("main_splitter")

        # Left panel (browser frame)
        self.browserFrame = BrowserFrameWidget(parent=main_splitter, status_bar=self.statusBar)
        self.browserFrame.setMinimumWidth(250)
        self.browserFrame.setMaximumWidth(400)

        # Center panel (plot tabs)
        self.plotTabs = CentralTabWidget(parent=main_splitter, status_bar=self.statusBar)
        self.plotTabs.setMinimumWidth(400)

        # Right panel (editor)
        self.editorTab = EditorTabWidget(parent=main_splitter, status_bar=self.statusBar)
        self.editorTab.setMinimumWidth(250)
        self.editorTab.setMaximumWidth(400)

        # Add panels to splitter
        main_splitter.addWidget(self.browserFrame)
        main_splitter.addWidget(self.plotTabs)
        main_splitter.addWidget(self.editorTab)

        # Set splitter proportions (left:center:right = 1:2:1)
        main_splitter.setSizes([300, 600, 300])

        # Add splitter to main layout
        main_layout.addWidget(main_splitter)

        """Sets up the default tabs of tab widgets."""
        self.plotTabs.setCurrentIndex(0)
        self.upMenuTab.setCurrentIndex(0)
        self.editorTab.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(self)

        # Connect view models to widgets
        self._connect_view_models()
        self._connect_actions()

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

    def _connect_actions(self) -> None:
        """Connect UI actions like import/export buttons."""
        if hasattr(self, "upMenuTab"):
            self.upMenuTab.import_clicked.connect(self._handle_import_clicked)
            self.upMenuTab.export_clicked.connect(self._handle_export_clicked)

    def _handle_import_clicked(self) -> None:
        """Handle importing a FIS model from file."""
        title = "Import FIS Model"
        if self.context and self.context.translate_manager:
            title = self.context.translate_manager.t("IMPORT")

        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            title,
            "",
            "FIS Files (*.fis);;All Files (*)",
        )

        if not file_path:
            return

        success = self.top_menu_view_model.import_model(file_path)
        if success:
            if hasattr(self, "statusBar") and self.statusBar:
                filename = os.path.basename(file_path)
                self.statusBar.showMessage(f"Imported model from {filename}", 5000)
        else:
            QtWidgets.QMessageBox.warning(
                self,
                "Import Failed",
                "The selected file could not be imported.",
            )

    def _handle_export_clicked(self) -> None:
        """Handle exporting the current FIS model to file."""
        title = "Export FIS Model"
        if self.context and self.context.translate_manager:
            title = self.context.translate_manager.t("EXPORT")

        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self,
            title,
            "",
            "FIS Files (*.fis);;All Files (*)",
        )

        if not file_path:
            return

        if not file_path.lower().endswith(".fis"):
            file_path = f"{file_path}.fis"

        success = self.top_menu_view_model.export_model(file_path)
        if success:
            if hasattr(self, "statusBar") and self.statusBar:
                filename = os.path.basename(file_path)
                self.statusBar.showMessage(f"Exported model to {filename}", 5000)
        else:
            QtWidgets.QMessageBox.warning(
                self,
                "Export Failed",
                "The model could not be exported to the selected file.",
            )
