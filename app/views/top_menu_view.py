"""Create a button area element GUI object above the central window of the application."""

import typing

from PyQt6 import QtCore, QtWidgets

from app.view_models.top_menu_view_model import TopMenuViewModel
from app.views.area_plot_view import AreaPlot
from app.views.base_tab_view import BaseTabView
from app.views.settings_view import SettingsView


class TopMenu(BaseTabView):
    """Class responsible for the rectangle widget at the top of the window.

    Its main function is to display buttons essential for functioning of the app.
    """

    new_clicked = QtCore.pyqtSignal()
    import_clicked = QtCore.pyqtSignal()
    help_clicked = QtCore.pyqtSignal()
    conversion_clicked = QtCore.pyqtSignal()
    export_clicked = QtCore.pyqtSignal()

    def __init__(self, parent: typing.Optional[QtWidgets.QWidget] = None, status_bar=None):
        """Initialize the top menu widget."""
        super().__init__(parent=parent)

        self.view_model = TopMenuViewModel()
        self.view_model.setParent(self)
        self.set_view_model(self.view_model)

        self.s = None
        self.setObjectName("topMenu")
        self.w = None
        self.status_bar = status_bar
        self._setup_ui()
        self._retranslate_ui()

    def _setup_ui(self):
        """Set up all the GUI sub elements."""
        self.designTab = QtWidgets.QWidget()
        self.designTab.setObjectName("designTab")

        # Create main layout for design tab
        main_layout = QtWidgets.QHBoxLayout(self.designTab)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # Left section - File management buttons
        files_group = QtWidgets.QGroupBox("File Management")
        files_layout = QtWidgets.QVBoxLayout(files_group)
        files_layout.setContentsMargins(5, 5, 5, 5)

        self.new_button = QtWidgets.QToolButton()
        self.new_button.setObjectName("new_button")
        self.new_button.clicked.connect(self._new_button_clicked)
        files_layout.addWidget(self.new_button)

        self.import_button = QtWidgets.QToolButton()
        self.import_button.setObjectName("import_button")
        self.import_button.clicked.connect(self._import_button_clicked)
        files_layout.addWidget(self.import_button)

        self.export_button = QtWidgets.QToolButton()
        self.export_button.setObjectName("export_button")
        self.export_button.clicked.connect(self._export_button_clicked)
        files_layout.addWidget(self.export_button)

        files_group.setMaximumWidth(200)
        main_layout.addWidget(files_group)

        # Center section - Input/Output management
        io_group = QtWidgets.QGroupBox("Input/Output Management")
        io_layout = QtWidgets.QVBoxLayout(io_group)
        io_layout.setContentsMargins(5, 5, 5, 5)

        # Create grid for IO buttons
        io_grid = QtWidgets.QGridLayout()

        self.add_input_button = QtWidgets.QPushButton()
        self.add_input_button.setObjectName("add_input_button")
        self.add_input_button.clicked.connect(self._add_input_button_clicked)
        io_grid.addWidget(self.add_input_button, 0, 0)

        self.delete_input_button = QtWidgets.QPushButton()
        self.delete_input_button.setObjectName("delete_input_button")
        self.delete_input_button.clicked.connect(self._del_input_button_clicked)
        io_grid.addWidget(self.delete_input_button, 0, 1)

        self.add_output_button = QtWidgets.QPushButton()
        self.add_output_button.setObjectName("add_output_button")
        self.add_output_button.clicked.connect(self._add_output_button_clicked)
        io_grid.addWidget(self.add_output_button, 1, 0)

        self.delete_output_button = QtWidgets.QPushButton()
        self.delete_output_button.setObjectName("delete_output_button")
        self.delete_output_button.clicked.connect(self._del_output_button_clicked)
        io_grid.addWidget(self.delete_output_button, 1, 1)

        io_layout.addLayout(io_grid)
        main_layout.addWidget(io_group)

        # Center-right section - Conversion and surface
        control_group = QtWidgets.QGroupBox("Controls")
        control_layout = QtWidgets.QVBoxLayout(control_group)
        control_layout.setContentsMargins(5, 5, 5, 5)

        self.conversion_button = QtWidgets.QPushButton()
        self.conversion_button.setObjectName("conversion_button")
        self.conversion_button.clicked.connect(self._conversion_button_clicked)
        control_layout.addWidget(self.conversion_button)

        self.surface_button = QtWidgets.QToolButton()
        self.surface_button.setObjectName("surface_button")
        self.surface_button.clicked.connect(self._show_area_plot_window)
        control_layout.addWidget(self.surface_button)

        # Interpolation controls
        interpolation_layout = QtWidgets.QHBoxLayout()
        self.interpolation_label = QtWidgets.QLabel()
        self.interpolation_label.setObjectName("interpolation_label")
        self.interpolation_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        interpolation_layout.addWidget(self.interpolation_label)

        self.interpolation_spinbox = QtWidgets.QSpinBox()
        self.interpolation_spinbox.setObjectName("interpolation_spinbox")
        interpolation_layout.addWidget(self.interpolation_spinbox)

        control_layout.addLayout(interpolation_layout)
        main_layout.addWidget(control_group)

        # Right section - Help and Settings
        help_group = QtWidgets.QGroupBox("Help & Settings")
        help_layout = QtWidgets.QVBoxLayout(help_group)
        help_layout.setContentsMargins(5, 5, 5, 5)

        self.help_button = QtWidgets.QPushButton()
        self.help_button.setObjectName("help_button")
        self.help_button.clicked.connect(self._help_button_clicked)
        help_layout.addWidget(self.help_button)

        self.settings_button = QtWidgets.QPushButton()
        self.settings_button.setObjectName("settings_button")
        self.settings_button.clicked.connect(self._show_settings_window)
        help_layout.addWidget(self.settings_button)

        help_group.setMaximumWidth(150)
        main_layout.addWidget(help_group)

        # Add stretch to push everything to the left
        main_layout.addStretch()

        self.addTab(self.designTab, "")
        self.tuningTab = QtWidgets.QWidget()
        self.tuningTab.setObjectName("tuningTab")
        self.addTab(self.tuningTab, "")

    def _retranslate_ui(self):
        self.add_input_button.setText(self.t("ADD_INPUT"))
        self.delete_input_button.setText(self.t("DELETE_INPUT"))
        self.add_output_button.setText(self.t("ADD_OUTPUT"))
        self.delete_output_button.setText(self.t("DELETE_OUTPUT"))
        self.setTabText(self.indexOf(self.designTab), self.t("DESIGN"))
        self.setTabText(self.indexOf(self.tuningTab), self.t("TUNING"))
        self.help_button.setText(self.t("HELP"))
        self.settings_button.setText(self.t("SETTINGS"))
        if hasattr(self, "system_type") and self.system_type == "Mamdani":
            self.conversion_button.setText(self.t("MAMDANI_TO_SUGENO"))
        elif hasattr(self, "system_type") and self.system_type == "Sugeno":
            self.conversion_button.setText(self.t("SUGENO_TO_MAMDANI"))
        else:
            self.conversion_button.setText(self.t("ERROR"))
        self.new_button.setText(self.t("NEW"))
        self.import_button.setText(self.t("IMPORT"))
        self.export_button.setText(self.t("EXPORT"))
        self.surface_button.setText(self.t("CONTROL_SURFACE"))
        self.interpolation_label.setText(self.t("INTERPOLATION_POINTS"))

    def _show_area_plot_window(self):
        """Show and hide the Area Plot window.

        Only one such window can exist at any given time.
        """
        if self.status_bar:
            self.status_bar.showMessage("Last action: Opened area plot window.")
        if self.w is None:
            self.w = AreaPlot()
        self.w.show()

    def _show_settings_window(self):
        """Show and hide the settings window.

        Only one such window can exist at any given time.
        """
        if self.status_bar:
            self.status_bar.showMessage("Last action: Opened settings window.")
        if self.s is None:
            self.s = SettingsView()
        self.s.show()

    def _add_input_button_clicked(self):
        if self.status_bar:
            self.status_bar.showMessage("Last action: Add input clicked.")
        self.view_model.add_input()

    def _del_input_button_clicked(self):
        if self.status_bar:
            self.status_bar.showMessage("Last action: Delete input clicked.")
        self.view_model.delete_input()

    def _add_output_button_clicked(self):
        if self.status_bar:
            self.status_bar.showMessage("Last action: Add output clicked.")
        self.view_model.add_output()

    def _del_output_button_clicked(self):
        if self.status_bar:
            self.status_bar.showMessage("Last action: Delete output clicked.")
        self.view_model.delete_output()

    def _help_button_clicked(self):
        if self.status_bar:
            self.status_bar.showMessage("Last action: Help clicked.")
        if hasattr(self, "help_clicked"):
            self.help_clicked.emit()

    def _conversion_button_clicked(self):
        """Convert system from Mamdani to Sugeno and vice versa."""
        if not hasattr(self, "system_type"):
            self.system_type = "Mamdani"
        if self.system_type == "Mamdani":
            self.system_type = "Sugeno"
            self.conversion_button.setText("Sugeno to Mamdani")
        else:
            self.system_type = "Mamdani"
            self.conversion_button.setText("Mamdani to Sugeno")
        if self.status_bar:
            self.status_bar.showMessage(f"Last action: Conversion clicked. System type: {self.system_type}")
        if hasattr(self, "conversion_clicked"):
            self.conversion_clicked.emit()

    def _new_button_clicked(self):
        if self.status_bar:
            self.status_bar.showMessage("Last action: New clicked.")
        if hasattr(self, "new_clicked"):
            self.new_clicked.emit()

    def _export_button_clicked(self):
        if self.status_bar:
            self.status_bar.showMessage("Last action: Export clicked.")
        self.export_clicked.emit()

    def _import_button_clicked(self):
        if self.status_bar:
            self.status_bar.showMessage("Last action: Import clicked.")
        if hasattr(self, "import_clicked"):
            self.import_clicked.emit()
