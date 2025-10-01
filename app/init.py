import sys

from PyQt6.QtWidgets import QApplication

from app.app_context import AppContext
from app.main_window import MainWindow
from app.utils.config import AppConfig
from app.view_models.base_view_model import BaseViewModel
from app.views.base_frame_view import BaseFrameView
from app.views.base_tab_view import BaseTabView
from app.views.base_view import BaseView


def run() -> int:
    """Initializes the application and runs it.

    Returns:
        int: The exit status code.
    """
    app: QApplication = QApplication(sys.argv)

    # Initialize configuration
    AppConfig.initialize()

    # Centralized app context
    context = AppContext()
    BaseViewModel.set_context_provider(lambda *a, **kw: context)
    BaseView.set_context_provider(lambda *a, **kw: context)
    BaseTabView.set_context_provider(lambda *a, **kw: context)
    BaseFrameView.set_context_provider(lambda *a, **kw: context)
    context.theme_manager.set_theme("dark", app)

    # Create main window with context
    window: MainWindow = MainWindow(context)
    window.show()

    return sys.exit(app.exec())
