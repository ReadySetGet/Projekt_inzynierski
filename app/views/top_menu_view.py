"""Create a button area element GUI object above the central window of the application.

Classes:
    TopMenu: button area element inheriting from QTabWidget.
"""

from PyQt6 import QtCore, QtWidgets

from app.view_models.top_menu_view_model import TopMenuViewModel
from app.views.area_plot_view import AreaPlot
from app.views.base_tab_view import BaseTabView
from app.views.settings_view import SettingsView


class TopMenu(BaseTabView):
    """Class responsible for the rectangle widget at the top of the window.

    It's main function is to display buttons essential for functioning of the app.
    """

    def __init__(self, parent=None, status_bar=None):
        """Initialize the top menu widget.

        Args:
            parent: Parent widget
            status_bar: Status bar widget
        """
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

        """Area grouping buttons responsible for managing inputs and outputs in the fis system."""
        self.input_output_button_area = QtWidgets.QScrollArea(parent=self.designTab)
        self.input_output_button_area.setGeometry(QtCore.QRect(270, 0, 221, 131))
        self.input_output_button_area.setWidgetResizable(True)
        self.input_output_button_area.setObjectName("input_output_button_area")

        self.scroll_area_widget_contents_3 = QtWidgets.QWidget()
        self.scroll_area_widget_contents_3.setGeometry(QtCore.QRect(0, 0, 219, 129))
        self.scroll_area_widget_contents_3.setObjectName("scroll_area_widget_contents_3")

        self.add_input_button = QtWidgets.QPushButton(parent=self.scroll_area_widget_contents_3)
        self.add_input_button.setGeometry(QtCore.QRect(10, 10, 91, 41))
        self.add_input_button.setObjectName("add_input_button")
        self.add_input_button.clicked.connect(self._add_input_button_clicked)

        self.delete_input_button = QtWidgets.QPushButton(parent=self.scroll_area_widget_contents_3)
        self.delete_input_button.setGeometry(QtCore.QRect(110, 10, 91, 41))
        self.delete_input_button.setObjectName("delete_input_button")
        self.delete_input_button.clicked.connect(self._del_input_button_clicked)

        self.add_output_button = QtWidgets.QPushButton(parent=self.scroll_area_widget_contents_3)
        self.add_output_button.setGeometry(QtCore.QRect(10, 70, 91, 41))
        self.add_output_button.setObjectName("add_output_button")
        self.add_output_button.clicked.connect(self._add_output_button_clicked)

        self.delete_output_button = QtWidgets.QPushButton(parent=self.scroll_area_widget_contents_3)
        self.delete_output_button.setGeometry(QtCore.QRect(110, 70, 95, 41))
        self.delete_output_button.setObjectName("delete_output_button")
        self.delete_output_button.clicked.connect(self._del_output_button_clicked)
        self.input_output_button_area.setWidget(self.scroll_area_widget_contents_3)

        self.help_button = QtWidgets.QPushButton(parent=self.designTab)
        self.help_button.setGeometry(QtCore.QRect(950, 20, 93, 28))
        self.help_button.setObjectName("help_button")
        self.help_button.clicked.connect(self._help_button_clicked)

        self.settings_button = QtWidgets.QPushButton(parent=self.designTab)
        self.settings_button.setGeometry(QtCore.QRect(950, 70, 93, 28))
        self.settings_button.setObjectName("settings_button")
        self.settings_button.clicked.connect(self._show_settings_window)

        self.conversion_button = QtWidgets.QPushButton(parent=self.designTab)
        self.conversion_button.setGeometry(QtCore.QRect(530, 30, 131, 61))
        self.conversion_button.setObjectName("conversion_button")
        self.conversion_button.clicked.connect(self._conversion_button_clicked)

        """Button area grouping buttons responsible for files management."""
        self.files_management_button_area = QtWidgets.QScrollArea(parent=self.designTab)
        self.files_management_button_area.setGeometry(QtCore.QRect(0, 0, 271, 131))
        self.files_management_button_area.setWidgetResizable(True)
        self.files_management_button_area.setObjectName("files_management_button_area")

        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 269, 129))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")

        self.new_button = QtWidgets.QToolButton(parent=self.scrollAreaWidgetContents)
        self.new_button.setGeometry(QtCore.QRect(10, 40, 81, 41))
        self.new_button.setObjectName("new_button")
        self.new_button.clicked.connect(self._new_button_clicked)

        self.import_button = QtWidgets.QToolButton(parent=self.scrollAreaWidgetContents)
        self.import_button.setGeometry(QtCore.QRect(100, 40, 71, 41))
        self.import_button.setObjectName("import_button")
        self.import_button.clicked.connect(self._import_button_clicked)

        self.export_button = QtWidgets.QToolButton(parent=self.scrollAreaWidgetContents)
        self.export_button.setGeometry(QtCore.QRect(180, 41, 81, 41))
        self.export_button.setObjectName("export_button")
        self.export_button.clicked.connect(self._export_button_clicked)

        self.files_management_button_area.setWidget(self.scrollAreaWidgetContents)

        self.surface_button = QtWidgets.QToolButton(parent=self.designTab)
        self.surface_button.setGeometry(QtCore.QRect(700, 30, 101, 61))
        self.surface_button.setObjectName("surface_button")
        self.surface_button.clicked.connect(self._show_area_plot_window)

        self.interpolation_spinbox = QtWidgets.QSpinBox(parent=self.designTab)
        self.interpolation_spinbox.setGeometry(QtCore.QRect(830, 60, 81, 22))
        self.interpolation_spinbox.setObjectName("interpolation_spinbox")

        self.interpolation_label = QtWidgets.QLabel(parent=self.designTab)
        self.interpolation_label.setGeometry(QtCore.QRect(810, 30, 121, 20))
        self.interpolation_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.interpolation_label.setObjectName("interpolation_label")
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
        self.status_bar.showMessage("Last action: Opened area plot window.")
        if self.w is None:
            self.w = AreaPlot()
        self.w.show()

    def _show_settings_window(self):
        """Show and hide the settings window.

        Only one such window can exist at any given time.
        """
        self.status_bar.showMessage("Last action: Opened settings window.")
        if self.s is None:
            self.s = SettingsView()
        self.s.show()

    def _add_input_button_clicked(self):
        self.status_bar.showMessage("Last action: Add input clicked.")
        self.view_model.add_input()

    def _del_input_button_clicked(self):
        self.status_bar.showMessage("Last action: Delete input clicked.")
        self.view_model.delete_input()

    def _add_output_button_clicked(self):
        self.status_bar.showMessage("Last action: Add output clicked.")
        self.view_model.add_output()

    def _del_output_button_clicked(self):
        self.status_bar.showMessage("Last action: Delete output clicked.")
        self.view_model.delete_output()

    def _help_button_clicked(self):
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
        self.status_bar.showMessage(f"Last action: Conversion clicked. System type: {self.system_type}")
        if hasattr(self, "conversion_clicked"):
            self.conversion_clicked.emit()

    def _new_button_clicked(self):
        self.status_bar.showMessage("Last action: New clicked.")
        if hasattr(self, "new_clicked"):
            self.new_clicked.emit()

    def _export_button_clicked(self):
        self.status_bar.showMessage("Last action: Export clicked.")
        if hasattr(self, "export_clicked"):
            self.export_clicked.emit()

    def _import_button_clicked(self):
        self.status_bar.showMessage("Last action: Import clicked.")
        if hasattr(self, "import_clicked"):
            self.import_clicked.emit()
