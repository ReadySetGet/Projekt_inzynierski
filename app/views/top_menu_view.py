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
        self.system_type = "Mamdani"
        self._setup_ui()
        self._retranslate_ui()
        self._update_system_type_from_model()

        if self.view_model:
            self.view_model.notify_data_changed.connect(self._on_data_changed)

    def _setup_ui(self):
        """Set up all the GUI sub elements."""
        self.designTab = QtWidgets.QWidget()
        self.designTab.setObjectName("designTab")

        # Create main layout for design tab
        main_layout = QtWidgets.QHBoxLayout(self.designTab)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # Left section - File management buttons
        files_group = QtWidgets.QGroupBox(self.t("FILE_MANAGEMENT"))
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
        io_group = QtWidgets.QGroupBox(self.t("INPUT_OUTPUT_MANAGEMENT"))
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
        control_group = QtWidgets.QGroupBox(self.t("CONTROLS"))
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
        self.interpolation_spinbox.setMinimum(10)
        self.interpolation_spinbox.setMaximum(1000)
        self.interpolation_spinbox.setValue(self.view_model.get_interpolation_points())
        self.interpolation_spinbox.valueChanged.connect(self._interpolation_spinbox_changed)
        interpolation_layout.addWidget(self.interpolation_spinbox)

        control_layout.addLayout(interpolation_layout)
        main_layout.addWidget(control_group)

        # Right section - Help and Settings
        help_group = QtWidgets.QGroupBox(self.t("HELP_SETTINGS"))
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

    def _retranslate_ui(self):
        self.add_input_button.setText(self.t("ADD_INPUT"))
        self.delete_input_button.setText(self.t("DELETE_INPUT"))
        self.add_output_button.setText(self.t("ADD_OUTPUT"))
        self.delete_output_button.setText(self.t("DELETE_OUTPUT"))
        self.setTabText(self.indexOf(self.designTab), self.t("DESIGN"))
        self.help_button.setText(self.t("HELP"))
        self.settings_button.setText(self.t("SETTINGS"))
        self._update_conversion_button_text()
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
            self.status_bar.showMessage(self.t("LAST_ACTION_OPENED_AREA_PLOT"))
        if self.w is None:
            self.w = AreaPlot()
        self.w.show()

    def _show_settings_window(self):
        """Show and hide the settings window.

        Only one such window can exist at any given time.
        """
        if self.status_bar:
            self.status_bar.showMessage(self.t("LAST_ACTION_OPENED_SETTINGS"))
        if self.s is None:
            self.s = SettingsView()
        self.s.show()

    def _add_input_button_clicked(self):
        if self.status_bar:
            self.status_bar.showMessage(self.t("LAST_ACTION_ADD_INPUT"))
        self.view_model.add_input()

    def _del_input_button_clicked(self):
        if self.status_bar:
            self.status_bar.showMessage(self.t("LAST_ACTION_DELETE_INPUT"))
        self.view_model.delete_input()

    def _add_output_button_clicked(self):
        if self.status_bar:
            self.status_bar.showMessage(self.t("LAST_ACTION_ADD_OUTPUT"))
        self.view_model.add_output()

    def _del_output_button_clicked(self):
        if self.status_bar:
            self.status_bar.showMessage(self.t("LAST_ACTION_DELETE_OUTPUT"))
        self.view_model.delete_output()

    def _help_button_clicked(self):
        if self.status_bar:
            self.status_bar.showMessage(self.t("LAST_ACTION_HELP"))
        if hasattr(self, "help_clicked"):
            self.help_clicked.emit()

    def _conversion_button_clicked(self):
        """Convert system from Mamdani to Sugeno and vice versa."""
        if not hasattr(self, "system_type"):
            self.system_type = "Mamdani"

        success = self.view_model.convert_inference_system()
        if success:
            self._update_system_type_from_model()
            self._update_conversion_button_text()
            if self.status_bar:
                self.status_bar.showMessage(f"{self.t('LAST_ACTION_CONVERSION_SUCCESS')} {self.system_type}", 5000)
        else:
            if self.status_bar:
                self.status_bar.showMessage(self.t("LAST_ACTION_CONVERSION_FAILED"), 5000)

        if hasattr(self, "conversion_clicked"):
            self.conversion_clicked.emit()

    def _update_system_type_from_model(self):
        """Update system_type from the FIS model."""
        try:
            fis_type = self.view_model.get_fis_type()
            if fis_type.lower() == "sugeno":
                self.system_type = "Sugeno"
            else:
                self.system_type = "Mamdani"
        except Exception:
            self.system_type = "Mamdani"

    def _update_conversion_button_text(self):
        """Update the conversion button text based on current system type."""
        if self.system_type == "Mamdani":
            self.conversion_button.setText(self.t("MAMDANI_TO_SUGENO"))
        elif self.system_type == "Sugeno":
            self.conversion_button.setText(self.t("SUGENO_TO_MAMDANI"))
        else:
            self.conversion_button.setText(self.t("ERROR"))

    def _on_data_changed(self):
        """Handle data changed signal from view model."""
        self._update_system_type_from_model()
        self._update_conversion_button_text()
        self._update_interpolation_spinbox()

    def _interpolation_spinbox_changed(self, value: int):
        """Handle interpolation spinbox value change."""
        self.view_model.set_interpolation_points(value)
        if self.status_bar:
            self.status_bar.showMessage(f"{self.t('INTERPOLATION_POINTS_SET_TO')} {value}", 2000)

    def _update_interpolation_spinbox(self):
        """Update interpolation spinbox value from model."""
        current_value = self.view_model.get_interpolation_points()
        if self.interpolation_spinbox.value() != current_value:
            self.interpolation_spinbox.blockSignals(True)
            self.interpolation_spinbox.setValue(current_value)
            self.interpolation_spinbox.blockSignals(False)

    def _new_button_clicked(self):
        if self.status_bar:
            self.status_bar.showMessage(self.t("LAST_ACTION_NEW"))
        if hasattr(self, "new_clicked"):
            self.new_clicked.emit()

    def _export_button_clicked(self):
        if self.status_bar:
            self.status_bar.showMessage(self.t("LAST_ACTION_EXPORT"))
        self.export_clicked.emit()

    def _import_button_clicked(self):
        if self.status_bar:
            self.status_bar.showMessage(self.t("LAST_ACTION_IMPORT"))
        if hasattr(self, "import_clicked"):
            self.import_clicked.emit()
