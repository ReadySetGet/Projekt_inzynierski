import os

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QMainWindow

from app.app_context import AppContext
from app.utils.config import AppConfig
from app.utils.paths import IMAGES_DIR, local_path
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

        if context:
            self.setWindowTitle(context.config.app_name())
            self.resize(context.config.window_width(), context.config.window_height())
        else:
            self.setWindowTitle(AppConfig.app_name())
            self.resize(AppConfig.window_width(), AppConfig.window_height())

        if context:
            self.shortcut_manager = ShortcutManager(self)
            self.setupViewModels()
            self.setupUi()
            self._set_window_icon()
            self.context.theme_manager.theme_changed.connect(self.reload_stylesheet)
            self.reload_stylesheet()
            self.context.translate_manager.language_changed.connect(self.retranslate_ui)
            self.context.translate_manager.set_language("en")

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

        self.central_widget = QtWidgets.QWidget(parent=self)
        self.central_widget.setObjectName("centralwidget")
        self.setCentralWidget(self.central_widget)

        main_layout = QtWidgets.QVBoxLayout(self.central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.statusBar = QtWidgets.QStatusBar(parent=self)
        self.statusBar.setObjectName("statusbar")
        self.setStatusBar(self.statusBar)
        if self.context and self.context.translate_manager:
            self.statusBar.showMessage(self.context.translate_manager.t("STARTED_APPLICATION"))
        else:
            self.statusBar.showMessage("Started application")

        self.upMenuTab = TopMenu(parent=self.central_widget, status_bar=self.statusBar)
        self.upMenuTab.setFixedHeight(160)
        main_layout.addWidget(self.upMenuTab)

        main_splitter = QtWidgets.QSplitter(QtCore.Qt.Orientation.Horizontal)
        main_splitter.setObjectName("main_splitter")

        self.browserFrame = BrowserFrameWidget(parent=main_splitter, status_bar=self.statusBar)
        self.browserFrame.setMinimumWidth(250)
        self.browserFrame.setMaximumWidth(400)

        self.plotTabs = CentralTabWidget(parent=main_splitter, status_bar=self.statusBar)
        self.plotTabs.setMinimumWidth(400)

        self.editorTab = EditorTabWidget(parent=main_splitter, status_bar=self.statusBar)
        self.editorTab.setMinimumWidth(250)
        self.editorTab.setMaximumWidth(400)

        main_splitter.addWidget(self.browserFrame)
        main_splitter.addWidget(self.plotTabs)
        main_splitter.addWidget(self.editorTab)

        main_splitter.setSizes([300, 600, 300])
        main_layout.addWidget(main_splitter)

        self.plotTabs.setCurrentIndex(0)
        self.upMenuTab.setCurrentIndex(0)
        self.editorTab.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(self)

        self._connect_view_models()
        self._connect_actions()
        self._register_shortcuts()

    def retranslate_ui(self):
        """Retranslate all UI elements when language changes."""
        if hasattr(self, "context") and self.context:
            self.setWindowTitle(self.context.translate_manager.t("MainWindow"))
        else:
            _translate = QtCore.QCoreApplication.translate
            self.setWindowTitle(_translate("MainWindow", "MainWindow"))

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
        self.plotTabs.set_view_model(self.central_tab_view_model)
        self.browserFrame.set_view_model(self.browser_frame_view_model)
        self.upMenuTab.set_view_model(self.top_menu_view_model)
        self.editorTab.set_view_model(self.editor_tab_view_model)

    def _connect_actions(self) -> None:
        """Connect UI actions like import/export buttons."""
        if hasattr(self, "upMenuTab"):
            self.upMenuTab.import_clicked.connect(self._handle_import_clicked)
            self.upMenuTab.export_clicked.connect(self._handle_export_clicked)
            self.upMenuTab.new_clicked.connect(self._handle_new_clicked)

    def _handle_import_clicked(self) -> None:
        """Handle importing a FIS model from file."""
        if self.context and self.context.translate_manager:
            title = self.context.translate_manager.t("IMPORT_FIS_MODEL")
        else:
            title = "Import FIS Model"

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
            if hasattr(self, "browser_frame_view_model") and self.browser_frame_view_model:
                self.browser_frame_view_model.add_imported_project(file_path)

            if hasattr(self, "statusBar") and self.statusBar:
                filename = os.path.basename(file_path)
                if self.context and self.context.translate_manager:
                    msg = f"{self.context.translate_manager.t('IMPORTED_MODEL_FROM')} {filename}"
                    self.statusBar.showMessage(msg, 5000)
                else:
                    self.statusBar.showMessage(f"Imported model from {filename}", 5000)
        else:
            if self.context and self.context.translate_manager:
                QtWidgets.QMessageBox.warning(
                    self,
                    self.context.translate_manager.t("IMPORT_FAILED"),
                    self.context.translate_manager.t("IMPORT_FAILED_MESSAGE"),
                )
            else:
                QtWidgets.QMessageBox.warning(
                    self,
                    "Import Failed",
                    "The selected file could not be imported.",
                )

    def _handle_new_clicked(self) -> None:
        """Handle creating a new FIS project."""
        if not hasattr(self, "browser_frame_view_model") or not self.browser_frame_view_model:
            return

        if self.context and self.context.translate_manager:
            title = self.context.translate_manager.t("NEW_PROJECT")
            mamdani_text = self.context.translate_manager.t("MAMDANI")
            sugeno_text = self.context.translate_manager.t("SUGENO")
            name_prompt = self.context.translate_manager.t("NEW_PROJECT_NAME")
        else:
            title = "New Project"
            mamdani_text = "Mamdani"
            sugeno_text = "Sugeno"
            name_prompt = "Project Name:"

        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle(title)
        dialog.setModal(True)

        layout = QtWidgets.QVBoxLayout(dialog)

        name_label = QtWidgets.QLabel(name_prompt)
        layout.addWidget(name_label)

        name_input = QtWidgets.QLineEdit()
        name_input.setPlaceholderText("MyProject")
        layout.addWidget(name_input)

        type_label = QtWidgets.QLabel("Type:")
        layout.addWidget(type_label)

        type_group = QtWidgets.QButtonGroup(dialog)
        mamdani_radio = QtWidgets.QRadioButton(mamdani_text)
        mamdani_radio.setChecked(True)
        sugeno_radio = QtWidgets.QRadioButton(sugeno_text)
        type_group.addButton(mamdani_radio, 0)
        type_group.addButton(sugeno_radio, 1)

        type_layout = QtWidgets.QHBoxLayout()
        type_layout.addWidget(mamdani_radio)
        type_layout.addWidget(sugeno_radio)
        layout.addLayout(type_layout)

        buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.StandardButton.Ok | QtWidgets.QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)

        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            project_name = name_input.text().strip()
            if not project_name:
                if self.context and self.context.translate_manager:
                    QtWidgets.QMessageBox.warning(
                        self,
                        self.context.translate_manager.t("ERROR"),
                        self.context.translate_manager.t("PROJECT_NAME_REQUIRED"),
                    )
                else:
                    QtWidgets.QMessageBox.warning(self, "Error", "Project name is required.")
                return

            fis_type = "mamdani" if mamdani_radio.isChecked() else "sugeno"
            success = self.browser_frame_view_model.create_new_project(project_name, fis_type)

            if success:
                if hasattr(self, "statusBar") and self.statusBar:
                    if self.context and self.context.translate_manager:
                        msg = f"{self.context.translate_manager.t('CREATED_PROJECT')} {project_name}"
                        self.statusBar.showMessage(msg, 5000)
                    else:
                        self.statusBar.showMessage(f"Created project {project_name}", 5000)
            else:
                if self.context and self.context.translate_manager:
                    QtWidgets.QMessageBox.warning(
                        self,
                        self.context.translate_manager.t("ERROR"),
                        self.context.translate_manager.t("CREATE_PROJECT_FAILED"),
                    )
                else:
                    QtWidgets.QMessageBox.warning(self, "Error", "Failed to create project. Name may already exist.")

    def _handle_export_clicked(self) -> None:
        """Handle exporting the current FIS model to file."""
        from app.utils.paths import PROJECTS_DIR

        if self.context and self.context.translate_manager:
            title = self.context.translate_manager.t("EXPORT_FIS_MODEL")
        else:
            title = "Export FIS Model"

        default_name = "exported_model.fis"
        if hasattr(self, "browser_frame_view_model") and self.browser_frame_view_model:
            current_project = self.browser_frame_view_model.current_project_name
            if current_project:
                default_name = f"{current_project}.fis"
            else:
                try:
                    fis_name = self.top_menu_view_model.fuzzy_service.get_system_name()
                    if fis_name:
                        default_name = f"{fis_name}.fis"
                except Exception:
                    pass

        default_path = str(PROJECTS_DIR / default_name)

        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self,
            title,
            default_path,
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
                if self.context and self.context.translate_manager:
                    msg = f"{self.context.translate_manager.t('EXPORTED_MODEL_TO')} {filename}"
                    self.statusBar.showMessage(msg, 5000)
                else:
                    self.statusBar.showMessage(f"Exported model to {filename}", 5000)
        else:
            if self.context and self.context.translate_manager:
                QtWidgets.QMessageBox.warning(
                    self,
                    self.context.translate_manager.t("EXPORT_FAILED"),
                    self.context.translate_manager.t("EXPORT_FAILED_MESSAGE"),
                )
            else:
                QtWidgets.QMessageBox.warning(
                    self,
                    "Export Failed",
                    "The model could not be exported to the selected file.",
                )

    def _register_shortcuts(self) -> None:
        """Register keyboard shortcuts."""
        if hasattr(self, "shortcut_manager"):
            self.shortcut_manager.register_shortcut(
                "Ctrl+S",
                self._handle_export_clicked,
                description="Save/Export FIS Model",
            )

    def _set_window_icon(self) -> None:
        """Set the window icon for the application."""
        app_icon = QtWidgets.QApplication.instance().windowIcon()
        if not app_icon.isNull():
            self.setWindowIcon(app_icon)
        else:
            icon_path = IMAGES_DIR / "app_icon.ico"

            if icon_path.exists():
                icon = QtGui.QIcon(str(icon_path))
            else:
                icon_path = IMAGES_DIR / "app_icon.png"
                if icon_path.exists():
                    icon = QtGui.QIcon(str(icon_path))
                else:
                    icon = MainWindow._create_default_icon()

            self.setWindowIcon(icon)

    @staticmethod
    def _create_default_icon() -> QtGui.QIcon:
        """Create a default fuzzy logic icon programmatically."""
        pixmap = QtGui.QPixmap(64, 64)
        pixmap.fill(QtCore.Qt.GlobalColor.transparent)

        painter = QtGui.QPainter(pixmap)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        pen = QtGui.QPen(QtGui.QColor(70, 130, 180), 3)
        painter.setPen(pen)
        brush = QtGui.QBrush(QtGui.QColor(70, 130, 180, 200))
        painter.setBrush(brush)

        center_x, center_y = 32, 32

        for i in range(3):
            radius = 20 - i * 5
            alpha = 150 + i * 30
            brush.setColor(QtGui.QColor(70, 130, 180, alpha))
            painter.setBrush(brush)
            painter.drawEllipse(center_x - radius, center_y - radius, radius * 2, radius * 2)

        painter.end()

        icon = QtGui.QIcon(pixmap)
        return icon
