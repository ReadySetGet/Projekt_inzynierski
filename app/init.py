import sys
from PyQt6.QtWidgets import QApplication
from PyQt6 import QtWidgets

#from app.main_window import MainWindow
from app.utils.config import AppConfig
from app.ui_main_window import UiMainWindow


def run() -> int:
    """
    Initializes the application and runs it.

    Returns:
        int: The exit status code.
    """
    app: QApplication = QApplication(sys.argv)
    AppConfig.initialize()

    # window: MainWindow = MainWindow()
    # window.show()

    MainWindow = QtWidgets.QMainWindow()
    ui = UiMainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    return sys.exit(app.exec())