from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
APP_DIR = ROOT_DIR / "app"
UTILS_DIR = APP_DIR / "utils"
RESOURCES_DIR = APP_DIR / "resources"
VIEWS_DIR = APP_DIR / "views"
VIEW_MODELS_DIR = APP_DIR / "view_models"
MODELS_DIR = APP_DIR / "models"
CONFIG_PATH = ROOT_DIR / "config.ini"
