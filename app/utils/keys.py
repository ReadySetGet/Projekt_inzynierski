from pathlib import Path

# Root of the project
ROOT_DIR = Path(__file__).resolve().parent.parent.parent

# App root
APP_DIR = ROOT_DIR / "app"

# Common paths
UTILS_DIR = APP_DIR / "utils"
RESOURCES_DIR = APP_DIR / "resources"
VIEWS_DIR = APP_DIR / "views"
VIEW_MODELS_DIR = APP_DIR / "view_models"
MODELS_DIR = APP_DIR / "models"

# Specific files
CONFIG_PATH = ROOT_DIR / "config.ini"

# Other Constants
PROGRESS_CALLBACK = "progress_callback"
