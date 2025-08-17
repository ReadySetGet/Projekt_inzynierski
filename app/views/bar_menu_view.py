from PyQt6 import QtCore, QtGui, QtWidgets


class BarMenuWidget(QtWidgets.QMenuBar):
    def __init__(self, main_window=None, parent=None):
        super().__init__(parent)
        self.setObjectName("barMenu")
        self._setup_ui(main_window)
        self._setup_actions()
        self._retranslate_ui()

    def _setup_ui(self, main_window):
        self.menuBar = QtWidgets.QMenuBar(parent=main_window)
        self.menuBar.setObjectName("menuBar")

        self.menu_files = QtWidgets.QMenu(parent=self.menuBar)
        self.menu_files.setObjectName("menu_files")

        self.submenu_new = QtWidgets.QMenu(parent=self.menu_files)
        self.submenu_new.setObjectName("submenu_new")

        self.menu_view = QtWidgets.QMenu(parent=self.menuBar)
        self.menu_view.setObjectName("menu_view")

        self.submenu_convert = QtWidgets.QMenu(parent=self.menu_view)
        self.submenu_convert.setObjectName("submenu_convert")

        self.menu_settings = QtWidgets.QMenu(parent=self.menuBar)
        self.menu_settings.setObjectName("menu_settings")

        self.menu_help = QtWidgets.QMenu(parent=self.menuBar)
        self.menu_help.setObjectName("menu_help")

        self.action_save = QtGui.QAction(parent=main_window)
        self.action_save.setObjectName("action_save")

        self.action_import = QtGui.QAction(parent=main_window)
        self.action_import.setObjectName("action_import")

        self.action_export = QtGui.QAction(parent=main_window)
        self.action_export.setObjectName("action_export")

        self.action_mamdani = QtGui.QAction(parent=main_window)
        self.action_mamdani.setObjectName("action_mamdani")

        self.action_sugeno = QtGui.QAction(parent=main_window)
        self.action_sugeno.setObjectName("action_sugeno")

        self.action_clear_inputs = QtGui.QAction(parent=main_window)
        self.action_clear_inputs.setObjectName("action_clear_inputs")

        self.action_clear_outputs = QtGui.QAction(parent=main_window)
        self.action_clear_outputs.setObjectName("action_clear_outputs")

        self.action_mamdani_to_sugeno = QtGui.QAction(parent=main_window)
        self.action_mamdani_to_sugeno.setObjectName("action_mamdani_to_sugeno")

        self.action_sugeno_to_mamdani = QtGui.QAction(parent=main_window)
        self.action_sugeno_to_mamdani.setObjectName("action_sugeno_to_mamdani")

        self.actionPlaceholder = QtGui.QAction(parent=main_window)
        self.actionPlaceholder.setObjectName("actionPlaceholder")

        self.actionPlaceholder_2 = QtGui.QAction(parent=main_window)
        self.actionPlaceholder_2.setObjectName("actionPlaceholder_2")
        main_window.setMenuBar(self.menuBar)

    def _setup_actions(self):
        self.submenu_new.addAction(self.action_mamdani)
        self.submenu_new.addAction(self.action_sugeno)

        self.menu_files.addAction(self.action_save)
        self.menu_files.addAction(self.action_import)
        self.menu_files.addAction(self.action_export)
        self.menu_files.addAction(self.submenu_new.menuAction())
        self.menu_files.addSeparator()

        self.submenu_convert.addAction(self.action_mamdani_to_sugeno)
        self.submenu_convert.addAction(self.action_sugeno_to_mamdani)

        self.menu_view.addAction(self.action_clear_inputs)
        self.menu_view.addAction(self.action_clear_outputs)
        self.menu_view.addSeparator()
        self.menu_view.addAction(self.submenu_convert.menuAction())

        self.menu_settings.addAction(self.actionPlaceholder)

        self.menu_help.addAction(self.actionPlaceholder_2)

        self.menuBar.addAction(self.menu_files.menuAction())
        self.menuBar.addAction(self.menu_view.menuAction())
        self.menuBar.addAction(self.menu_settings.menuAction())
        self.menuBar.addAction(self.menu_help.menuAction())

    def _retranslate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        self.menu_files.setTitle(_translate("MainWindow", "Files"))
        self.submenu_new.setTitle(_translate("MainWindow", "New"))
        self.menu_view.setTitle(_translate("MainWindow", "View"))
        self.submenu_convert.setTitle(_translate("MainWindow", "Convert"))
        self.menu_settings.setTitle(_translate("MainWindow", "Settings"))
        self.menu_help.setTitle(_translate("MainWindow", "Help"))
        self.action_save.setText(_translate("MainWindow", "Save"))
        self.action_import.setText(_translate("MainWindow", "Import"))
        self.action_export.setText(_translate("MainWindow", "Export"))
        self.action_mamdani.setText(_translate("MainWindow", "Mamdani"))
        self.action_sugeno.setText(_translate("MainWindow", "Sugeno"))
        self.action_clear_inputs.setText(_translate("MainWindow", "Clear Inputs"))
        self.action_clear_outputs.setText(_translate("MainWindow", "Clear Outputs"))
        self.action_mamdani_to_sugeno.setText(_translate("MainWindow", "Mamdani to Sugeno"))
        self.action_sugeno_to_mamdani.setText(_translate("MainWindow", "Sugeno to Mamdani"))
        self.actionPlaceholder.setText(_translate("MainWindow", "Placeholder"))
        self.actionPlaceholder_2.setText(_translate("MainWindow", "Placeholder"))