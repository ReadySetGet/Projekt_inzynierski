import sys
from pathlib import Path


def get_resource_path(*parts: str) -> Path:
    """Return the absolute path to a resource, compatible with PyInstaller bundles.

    Args:
        *parts (str): Path components relative to the resource root.

    Returns:
        Path: The absolute path to the resource.
    """
    if hasattr(sys, "_MEIPASS"):
        base_path = Path(sys._MEIPASS)
    else:
        base_path = PROJECT_ROOT
    return base_path.joinpath(*parts)


def get_writable_path(*parts: str) -> Path:
    """Return the absolute path to a writable directory, compatible with PyInstaller bundles.

    When running as an .exe, this returns a path relative to the executable's directory.
    When running as a script, this returns a path relative to the project root.

    Args:
        *parts (str): Path components relative to the writable root.

    Returns:
        Path: The absolute path to the writable directory.
    """
    if getattr(sys, "frozen", False):
        if hasattr(sys, "_MEIPASS"):
            exe_path = Path(sys.executable).parent
        else:
            exe_path = Path(sys.executable).parent
        base_path = exe_path
    else:
        base_path = PROJECT_ROOT
    return base_path.joinpath(*parts)


PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
APP_DIR = PROJECT_ROOT / "app"
ASSETS_DIR = get_resource_path("assets")
THEMES_DIR = get_resource_path("assets", "themes")
LOCALES_DIR = get_resource_path("assets", "locales")
FONTS_DIR = get_resource_path("assets", "fonts")
IMAGES_DIR = get_resource_path("assets", "images")
UTILS_DIR = APP_DIR / "utils"
VIEWS_DIR = APP_DIR / "views"
VIEW_MODELS_DIR = APP_DIR / "view_models"
MODELS_DIR = APP_DIR / "models"
CONFIG_PATH = PROJECT_ROOT / "config.ini"
PYPROJECT_TOML = PROJECT_ROOT / "pyproject.toml"
REQUIREMENTS_TXT = PROJECT_ROOT / "requirements.txt"
PROJECTS_DIR = get_writable_path("projects")


def local_path(module_file: str, *parts: str) -> Path:
    """Return a path relative to the directory of the given module file.

    Args:
        module_file (str): The __file__ of the calling module.
        *parts (str): Path components relative to the module's directory.

    Returns:
        Path: The absolute path resolved from the module's directory and parts.
    """
    return Path(module_file).parent.joinpath(*parts)
