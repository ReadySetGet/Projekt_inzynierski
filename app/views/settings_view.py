from PyQt6 import QtCore, QtWidgets

from app.view_models.settings_view_model import SettingsViewModel
from app.views.base_widget_view import BaseWidgetView


class SettingsView(BaseWidgetView):
    """Class used to display settings window widget.

    It does not have a Parent attribute as to be displayed in a separate window.
    """

    styles = ["Light", "Dark", "Blue", "Red", "Green"]

    def __init__(self, view_model: SettingsViewModel = None):
        """Initialize the settings view widget.

        Args:
            view_model (SettingsViewModel, optional): The view model for this view.
        """
        super().__init__()
        self.setObjectName("settings")
        self.view_model = view_model if view_model else SettingsViewModel()
        self._setup_ui()
        self._setup_connections()
        self._retranslate_ui()
        self._load_initial_data()

    def _setup_ui(self):
        self.resize(800, 600)
        self.setWindowTitle("Settings")

        self.verticalLayoutWidget = QtWidgets.QWidget(parent=self)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 30, 102, 561))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")

        self.settings_buttons = QtWidgets.QFormLayout(self.verticalLayoutWidget)
        self.settings_buttons.setContentsMargins(0, 0, 0, 0)
        self.settings_buttons.setObjectName("settings_buttons")

        self.theme_language_button = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        self.theme_language_button.setObjectName("theme_language_button")
        self.theme_language_button.clicked.connect(self._show_theme_language_tab)
        self.settings_buttons.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.theme_language_button)

        self.colour_button = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        self.colour_button.setObjectName("colour_button")
        self.colour_button.clicked.connect(self._show_color_tab)
        self.settings_buttons.setWidget(1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.colour_button)

        self.text_button = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        self.text_button.setObjectName("text_button")
        self.text_button.clicked.connect(self._show_font_tab)
        self.settings_buttons.setWidget(2, QtWidgets.QFormLayout.ItemRole.LabelRole, self.text_button)

        self.pushButton_6 = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        self.pushButton_6.setObjectName("pushButton_6")
        self.settings_buttons.setWidget(3, QtWidgets.QFormLayout.ItemRole.LabelRole, self.pushButton_6)

        self.pushButton_5 = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        self.pushButton_5.setObjectName("pushButton_5")
        self.settings_buttons.setWidget(4, QtWidgets.QFormLayout.ItemRole.LabelRole, self.pushButton_5)

        self.pushButton_3 = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.settings_buttons.setWidget(5, QtWidgets.QFormLayout.ItemRole.LabelRole, self.pushButton_3)

        self.button_6 = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        self.button_6.setObjectName("button_6")
        self.settings_buttons.setWidget(6, QtWidgets.QFormLayout.ItemRole.LabelRole, self.button_6)

        self.line = QtWidgets.QFrame(parent=self)
        self.line.setGeometry(QtCore.QRect(99, 10, 31, 561))
        self.line.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line.setObjectName("line")

        self.frame = QtWidgets.QFrame(parent=self)
        self.frame.setGeometry(QtCore.QRect(130, 10, 651, 561))
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.frame.setStyleSheet("background-color: #FCFCFC")

        # Theme and Language Tab
        self.theme_language_tab = QtWidgets.QWidget(parent=self.frame)
        self.theme_language_tab.setObjectName("theme_language_tab")

        self.theme_label = QtWidgets.QLabel(parent=self.theme_language_tab)
        self.theme_label.setGeometry(QtCore.QRect(10, 20, 181, 41))
        self.theme_label.setObjectName("theme_label")

        self.theme_dropdown = QtWidgets.QComboBox(parent=self.theme_language_tab)
        self.theme_dropdown.setGeometry(QtCore.QRect(220, 30, 200, 31))
        self.theme_dropdown.setObjectName("theme_dropdown")

        self.language_label = QtWidgets.QLabel(parent=self.theme_language_tab)
        self.language_label.setGeometry(QtCore.QRect(10, 80, 181, 41))
        self.language_label.setObjectName("language_label")

        self.language_dropdown = QtWidgets.QComboBox(parent=self.theme_language_tab)
        self.language_dropdown.setGeometry(QtCore.QRect(220, 90, 200, 31))
        self.language_dropdown.setObjectName("language_dropdown")

        self.apply_button = QtWidgets.QPushButton(parent=self.theme_language_tab)
        self.apply_button.setGeometry(QtCore.QRect(220, 150, 100, 31))
        self.apply_button.setObjectName("apply_button")

        self.colour_tab = QtWidgets.QWidget(parent=self.frame)
        self.colour_tab.setObjectName("colour_tab")
        self.colour_tab.hide()

        self.central_label = QtWidgets.QLabel(parent=self.colour_tab)
        self.central_label.setGeometry(QtCore.QRect(10, 10, 181, 41))
        self.central_label.setObjectName("central_label")

        self.editor_label = QtWidgets.QLabel(parent=self.colour_tab)
        self.editor_label.setGeometry(QtCore.QRect(10, 60, 181, 41))
        self.editor_label.setObjectName("editor_label")

        self.browser_label = QtWidgets.QLabel(parent=self.colour_tab)
        self.browser_label.setGeometry(QtCore.QRect(10, 110, 181, 41))
        self.browser_label.setObjectName("browser_label")

        self.topmenu_label = QtWidgets.QLabel(parent=self.colour_tab)
        self.topmenu_label.setGeometry(QtCore.QRect(10, 160, 181, 41))
        self.topmenu_label.setObjectName("unified_label")

        self.central_color_dropdown = QtWidgets.QComboBox(parent=self.colour_tab)
        self.central_color_dropdown.setGeometry(QtCore.QRect(220, 20, 131, 31))
        self.central_color_dropdown.setObjectName("central_color_dropdown")
        self.central_color_dropdown.addItems(self.styles)
        self.central_color_dropdown.currentTextChanged.connect(self._change_style)

        self.editor_color_dropdown = QtWidgets.QComboBox(parent=self.colour_tab)
        self.editor_color_dropdown.setGeometry(QtCore.QRect(220, 70, 131, 31))
        self.editor_color_dropdown.setObjectName("editor_color_dropdown")
        self.editor_color_dropdown.addItems(self.styles)

        self.browser_color_dropdown = QtWidgets.QComboBox(parent=self.colour_tab)
        self.browser_color_dropdown.setGeometry(QtCore.QRect(220, 120, 131, 31))
        self.browser_color_dropdown.setObjectName("browser_color_dropdown")
        self.browser_color_dropdown.addItems(self.styles)

        self.topmenu_color_dropdown = QtWidgets.QComboBox(parent=self.colour_tab)
        self.topmenu_color_dropdown.setGeometry(QtCore.QRect(220, 170, 131, 31))
        self.topmenu_color_dropdown.setObjectName("topmenu_color_dropdown")
        self.topmenu_color_dropdown.addItems(self.styles)

        self.unified_label = QtWidgets.QLabel(parent=self.colour_tab)
        self.unified_label.setGeometry(QtCore.QRect(10, 240, 181, 41))
        self.unified_label.setObjectName("unified_label")

        self.unified_color_dropdown = QtWidgets.QComboBox(parent=self.colour_tab)
        self.unified_color_dropdown.setGeometry(QtCore.QRect(220, 240, 131, 31))
        self.unified_color_dropdown.setObjectName("unified_color_dropdown")
        self.unified_color_dropdown.addItems(self.styles)
        self.unified_color_dropdown.setDisabled(True)

        self.unified_color_checkbox = QtWidgets.QCheckBox(parent=self.colour_tab)
        self.unified_color_checkbox.setGeometry(QtCore.QRect(400, 250, 111, 20))
        self.unified_color_checkbox.setObjectName("unified_color_checkbox")
        self.unified_color_checkbox.clicked.connect(self._checkbox)

        self.font_tab = QtWidgets.QWidget(parent=self.frame)
        self.font_tab.setObjectName("font_tab")
        self.font_tab.hide()

        self.font_size_label = QtWidgets.QLabel(parent=self.font_tab)
        self.font_size_label.setGeometry(QtCore.QRect(10, 20, 181, 41))
        self.font_size_label.setObjectName("font_size_label")

        self.font_color_label = QtWidgets.QLabel(parent=self.font_tab)
        self.font_color_label.setGeometry(QtCore.QRect(10, 80, 181, 41))
        self.font_color_label.setObjectName("font_color_label")

        self.font_family_label = QtWidgets.QLabel(parent=self.font_tab)
        self.font_family_label.setGeometry(QtCore.QRect(10, 140, 181, 41))
        self.font_family_label.setObjectName("font_style_label")

        self.font_family_dropdown = QtWidgets.QFontComboBox(parent=self.font_tab)
        self.font_family_dropdown.setGeometry(QtCore.QRect(200, 140, 226, 41))
        self.font_family_dropdown.setObjectName("font_style_dropdown")
        self.font_family_dropdown.currentTextChanged.connect(self._font_family)

        self.font_color_dropdown = QtWidgets.QComboBox(parent=self.font_tab)
        self.font_color_dropdown.setGeometry(QtCore.QRect(200, 90, 131, 31))
        self.font_color_dropdown.setObjectName("font_color_dropdown")
        self.font_color_dropdown.addItems(self.styles)

        self.font_size_spinbox = QtWidgets.QSpinBox(parent=self.font_tab)
        self.font_size_spinbox.setGeometry(QtCore.QRect(200, 30, 131, 21))
        self.font_size_spinbox.setObjectName("font_size_spinbox")
        self.font_size_spinbox.setValue(11)
        self.font_size_spinbox.valueChanged.connect(self._font_size)

    def _retranslate_ui(self):
        self.theme_language_button.setText(self.t("THEME_AND_LANGUAGE"))
        self.colour_button.setText(self.t("COLOUR"))
        self.text_button.setText(self.t("TEXT"))
        self.pushButton_6.setText(self.t("OPTION_3"))
        self.pushButton_5.setText(self.t("OPTION_4"))
        self.pushButton_3.setText(self.t("OPTION_5"))
        self.button_6.setText(self.t("OPTION_6"))
        self.theme_label.setText(self.t("THEME"))
        self.language_label.setText(self.t("LANGUAGE"))
        self.apply_button.setText(self.t("APPLY"))
        self.central_label.setText(self.t("CENTRAL_WINDOW_COLOUR"))
        self.editor_label.setText(self.t("EDITOR_WINDOW_COLOUR"))
        self.browser_label.setText(self.t("BROWSER_WINDOW_COLOUR"))
        self.topmenu_label.setText(self.t("TOP_MENU_COLOUR"))
        self.unified_label.setText(self.t("UNIFIED_APP_COLOUR"))
        self.unified_color_checkbox.setText(self.t("ENABLED"))
        self.font_size_label.setText(self.t("FONT_SIZE"))
        self.font_color_label.setText(self.t("FONT_COLOUR"))
        self.font_family_label.setText(self.t("FONT_STYLE"))

    def _show_theme_language_tab(self):
        """Show the theme and language settings tab."""
        self.colour_tab.hide()
        self.font_tab.hide()
        self.theme_language_tab.show()

    def _show_color_tab(self):
        """Show the color settings tab."""
        self.theme_language_tab.hide()
        self.font_tab.hide()
        self.colour_tab.show()

    def _show_font_tab(self):
        """Show the font settings tab."""
        self.theme_language_tab.hide()
        self.colour_tab.hide()
        self.font_tab.show()

    def _checkbox(self):
        """Handle unified color checkbox state changes.

        When 'unified color' option is selected, disable the other color options.
        When 'unified color' option is unselected, enable the other color options.
        """
        if self.unified_color_checkbox.isChecked():
            self.central_color_dropdown.setDisabled(True)
            self.editor_color_dropdown.setDisabled(True)
            self.browser_color_dropdown.setDisabled(True)
            self.topmenu_color_dropdown.setDisabled(True)
            self.unified_color_dropdown.setEnabled(True)
        else:
            self.central_color_dropdown.setEnabled(True)
            self.editor_color_dropdown.setEnabled(True)
            self.browser_color_dropdown.setEnabled(True)
            self.topmenu_color_dropdown.setEnabled(True)
            self.unified_color_dropdown.setDisabled(True)

    def _change_style(self):
        """Change the colour style of the window."""
        style = self.central_color_dropdown.currentText()
        if style == "Light":
            self.frame.setStyleSheet("background-color: #FCFCFC")
        elif style == "Dark":
            self.frame.setStyleSheet("background-color: #4A4A4A")
        elif style == "Blue":
            self.frame.setStyleSheet("background-color: #2786B0")
        elif style == "Red":
            self.frame.setStyleSheet("background-color: #B05A5A")
        elif style == "Green":
            self.frame.setStyleSheet("background-color: #31B04B")

    def _font_size(self):
        """Change the font size in the window."""
        font = self.font_size_label.font()
        size = self.font_size_spinbox.value()
        font.setPointSize(size)
        self.font_size_label.setFont(font)

    def _font_family(self):
        """Change the font family in the window."""
        font = self.font_family_label.font()
        family = self.font_family_dropdown.currentText()
        font.setFamily(family)
        self.font_family_label.setFont(font)

    def _setup_connections(self):
        """Setup connections between view and view model."""
        # Connect dropdown changes to handlers
        self.apply_button.clicked.connect(self._on_apply_settings)

        # Connect view model signals to update UI
        self.view_model.theme_list_changed.connect(self._update_theme_list)
        self.view_model.language_list_changed.connect(self._update_language_list)
        self.view_model.current_theme_changed.connect(self._on_current_theme_changed)
        self.view_model.current_language_changed.connect(self._on_current_language_changed)

    def _load_initial_data(self):
        """Load initial data from view model."""
        # Load available themes and languages
        themes = self.view_model.get_available_themes()
        languages = self.view_model.get_available_languages()

        self._update_theme_list(themes)
        self._update_language_list(languages)

        # Set current selections
        current_theme = self.view_model.get_current_theme()
        current_language = self.view_model.get_current_language()

        if current_theme:
            index = self.theme_dropdown.findText(current_theme)
            if index >= 0:
                self.theme_dropdown.setCurrentIndex(index)

        if current_language:
            index = self.language_dropdown.findText(current_language)
            if index >= 0:
                self.language_dropdown.setCurrentIndex(index)

    def _update_theme_list(self, themes: list[str]):
        """Update the theme dropdown with available themes.

        Args:
            themes (list[str]): List of available theme names.
        """
        current_text = self.theme_dropdown.currentText()
        self.theme_dropdown.clear()
        self.theme_dropdown.addItems(themes)

        # Restore selection if possible
        if current_text:
            index = self.theme_dropdown.findText(current_text)
            if index >= 0:
                self.theme_dropdown.setCurrentIndex(index)

    def _update_language_list(self, languages: list[str]):
        """Update the language dropdown with available languages.

        Args:
            languages (list[str]): List of available language codes.
        """
        current_text = self.language_dropdown.currentText()
        self.language_dropdown.clear()
        self.language_dropdown.addItems(languages)

        # Restore selection if possible
        if current_text:
            index = self.language_dropdown.findText(current_text)
            if index >= 0:
                self.language_dropdown.setCurrentIndex(index)

    def _on_apply_settings(self):
        """Apply the selected theme and language settings."""
        selected_theme = self.theme_dropdown.currentText()
        selected_language = self.language_dropdown.currentText()

        if selected_theme:
            self.view_model.set_theme(selected_theme)

        if selected_language:
            self.view_model.set_language(selected_language)
            # Update all UI text after language change
            self._retranslate_ui()

    def _on_current_theme_changed(self, theme_name: str):
        """Handle theme change from view model.

        Args:
            theme_name (str): The new theme name.
        """
        index = self.theme_dropdown.findText(theme_name)
        if index >= 0:
            self.theme_dropdown.setCurrentIndex(index)

    def _on_current_language_changed(self, language_code: str):
        """Handle language change from view model.

        Args:
            language_code (str): The new language code.
        """
        index = self.language_dropdown.findText(language_code)
        if index >= 0:
            self.language_dropdown.setCurrentIndex(index)
        # Update all UI text after language change
        self._retranslate_ui()
