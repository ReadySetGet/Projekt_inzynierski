from PyQt6 import QtCore, QtGui, QtWidgets


class EditorTabWidget(QtWidgets.QTabWidget):
    add_mf_clicked = QtCore.pyqtSignal()
    remove_mf_clicked = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("editorTab")
        self._setup_ui()
        self._retranslate_ui()

    def _setup_ui(self):
        input_mf_list = ['Placeholder Input MF']
        output_mf_list = ['Placeholder Output MF']

        self.fis_properties_tab = QtWidgets.QWidget()
        self.fis_properties_tab.setObjectName("fis_properties_tab")

        self.addTab(self.fis_properties_tab, "fis_properties_tab")

        self.mf_properties_tab = QtWidgets.QWidget()
        self.mf_properties_tab.setObjectName("fis_properties_tab")

        self.addTab(self.mf_properties_tab, "mf_properties_tab")

        self.rule_editor_tab = QtWidgets.QWidget()
        self.rule_editor_tab.setObjectName("rule_editor_tab")

        self.addTab(self.rule_editor_tab, "rule_editor_tab")

        self._retranslate_ui()

    def _retranslate_ui(self):
        _translate = QtCore.QCoreApplication.translate

        self.setTabText(self.indexOf(self.fis_properties_tab), _translate("MainWindow", "fisPropertiesTab"))
        self.setTabText(self.indexOf(self.mf_properties_tab), _translate("MainWindow", "mfPropertiesTab"))
        self.setTabText(self.indexOf(self.rule_editor_tab), _translate("MainWindow", "rulePropertiesTab"))
