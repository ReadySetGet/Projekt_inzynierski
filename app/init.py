import sys

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication

from app.app_context import AppContext
from app.main_window import MainWindow
from app.utils.config import AppConfig
from app.utils.paths import IMAGES_DIR
from app.view_models.base_view_model import BaseViewModel


def run() -> int:
    """Initializes the application and runs it.

    Returns:
        int: The exit status code.
    """
    app: QApplication = QApplication(sys.argv)

    icon_path = IMAGES_DIR / "app_icon.ico"
    if not icon_path.exists():
        icon_path = IMAGES_DIR / "app_icon.png"
    if icon_path.exists():
        app_icon = QIcon(str(icon_path))
    else:
        app_icon = MainWindow._create_default_icon()

    app.setWindowIcon(app_icon)

    AppConfig.initialize()
    context = AppContext()
    BaseViewModel.set_context_provider(lambda *a, **kw: context)
    context.theme_manager.set_theme("light", app)
    window: MainWindow = MainWindow(context)

    if sys.platform == "win32":
        import ctypes

        myappid = "fuzzy.logic.designer.1.0"
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    window.show()

    return sys.exit(app.exec())
