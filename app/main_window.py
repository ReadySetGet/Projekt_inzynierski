from PyQt6.QtWidgets import QMainWindow

from app.utils.config import AppConfig


class MainWindow(QMainWindow):
    """
    MainWindow

    Args:
        QMainWindow (QMainWindow): Inheritance
    """

    def __init__(self) -> None:
        """
        Initialize the Main-Window.
        """
        super().__init__()
        # Window-Settings
        self.setWindowTitle(AppConfig.app_name())
        self.resize(AppConfig.window_width(), AppConfig.window_height())

        # To be implemented, according to https://github.com/Julkul1/pyqt-mvvm-example as agreed
        #
        # model = CounterModel()
        # view_model = MainViewModel(model)
        # view = MainView(view_model)
        # self.setCentralWidget(view)
        # view.show()