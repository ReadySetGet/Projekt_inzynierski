from PyQt6 import QtWidgets, QtCore, QtGui


class SettingsView(QtWidgets.QWidget):
    styles = ['Light', 'Dark', 'Blue', 'Red', 'Green']

    def __init__(self):
        super().__init__()
        self.setObjectName("settings")
        self._setup_ui()
        self._retranslate_ui()

    def _setup_ui(self):
        self.resize(800, 600)
        self.setWindowTitle("Settings")

        self.verticalLayoutWidget = QtWidgets.QWidget(parent=self)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 30, 102, 561))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")

        self.settings_buttons = QtWidgets.QFormLayout(self.verticalLayoutWidget)
        self.settings_buttons.setContentsMargins(0, 0, 0, 0)
        self.settings_buttons.setObjectName("settings_buttons")

        self.colour_button = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        self.colour_button.setObjectName("colour_button")
        self.colour_button.clicked.connect(self._show_color_tab)
        self.settings_buttons.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.colour_button)

        self.text_button = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        self.text_button.setObjectName("text_button")
        self.text_button.clicked.connect(self._show_font_tab)
        self.settings_buttons.setWidget(1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.text_button)

        self.pushButton_6 = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        self.pushButton_6.setObjectName("pushButton_6")
        self.settings_buttons.setWidget(2, QtWidgets.QFormLayout.ItemRole.LabelRole, self.pushButton_6)

        self.pushButton_5 = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        self.pushButton_5.setObjectName("pushButton_5")
        self.settings_buttons.setWidget(3, QtWidgets.QFormLayout.ItemRole.LabelRole, self.pushButton_5)

        self.pushButton_3 = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.settings_buttons.setWidget(4, QtWidgets.QFormLayout.ItemRole.LabelRole, self.pushButton_3)

        self.button_6 = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        self.button_6.setObjectName("button_6")
        self.settings_buttons.setWidget(5, QtWidgets.QFormLayout.ItemRole.LabelRole, self.button_6)

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

        self.colour_tab = QtWidgets.QWidget(parent=self.frame)
        self.colour_tab.setObjectName("colour_tab")

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
        _translate = QtCore.QCoreApplication.translate
        self.colour_button.setText(_translate("MainWindow", "Colour"))
        self.text_button.setText(_translate("MainWindow", "Text"))
        self.pushButton_6.setText(_translate("MainWindow", "Option 3"))
        self.pushButton_5.setText(_translate("MainWindow", "Option 4"))
        self.pushButton_3.setText(_translate("MainWindow", "Option 5"))
        self.button_6.setText(_translate("MainWindow", "Option 6"))
        self.central_label.setText(_translate("MainWindow", "Central Window Colour"))
        self.editor_label.setText(_translate("MainWindow", "Editor Window Colour"))
        self.browser_label.setText(_translate("MainWindow", "Browser Window Colour"))
        self.topmenu_label.setText(_translate("MainWindow", "Top Menu Colour"))
        self.unified_label.setText(_translate("MainWindow", "Unified App Colour"))
        self.unified_color_checkbox.setText(_translate("MainWindow", "Enabled"))
        self.font_size_label.setText(_translate("MainWindow", "Font Size"))
        self.font_color_label.setText(_translate("MainWindow", "Font Colour"))
        self.font_family_label.setText(_translate("MainWindow", "Font Style"))

    def _show_color_tab(self):
        self.font_tab.hide()
        self.colour_tab.show()

    def _show_font_tab(self):
        self.colour_tab.hide()
        self.font_tab.show()

    def _checkbox(self):
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
        style = self.central_color_dropdown.currentText()
        if style == 'Light':
            self.frame.setStyleSheet("background-color: #FCFCFC")
        elif style == 'Dark':
            self.frame.setStyleSheet("background-color: #4A4A4A")
        elif style == 'Blue':
            self.frame.setStyleSheet("background-color: #2786B0")
        elif style == 'Red':
            self.frame.setStyleSheet("background-color: #B05A5A")
        elif style == 'Green':
            self.frame.setStyleSheet("background-color: #31B04B")

    def _font_size(self):
        font = self.font_size_label.font()
        size = self.font_size_spinbox.value()
        font.setPointSize(size)
        self.font_size_label.setFont(font)

    def _font_family(self):
        font = self.font_family_label.font()
        family = self.font_family_dropdown.currentText()
        font.setFamily(family)
        self.font_family_label.setFont(font)

