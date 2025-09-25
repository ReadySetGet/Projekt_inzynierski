import json
import os
from typing import Any, Optional

from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QApplication

from app.utils.paths import THEMES_DIR


class ThemeManager(QObject):
    """Manager for loading and applying QSS themes with color palette support.

    Should be instantiated and managed by AppContext, not as a global singleton.
    """

    theme_changed = pyqtSignal()

    current_theme: Optional[str]
    current_palette: Optional[dict[str, Any]]

    def __init__(self, themes_path: Optional[str] = None) -> None:
        """Initialize the ThemeManager.

        Args:
            themes_path (Optional[str]): Path to the themes directory.
                Defaults to THEMES_DIR.
        """
        super().__init__()
        self.current_theme = None
        self.themes_path = themes_path if themes_path is not None else str(THEMES_DIR)
        self.palette_paths = self._discover_palettes()
        self.current_palette = None

    def _discover_palettes(self) -> dict[str, str]:
        """Discover available JSON palette files in the themes directory.

        Returns:
            dict[str, str]: Mapping of theme names to JSON palette file paths.
        """
        palette_files: dict[str, str] = {}
        if not os.path.isdir(self.themes_path):
            return palette_files
        for file in os.listdir(self.themes_path):
            if file.endswith(".json"):
                theme_name = file.replace(".json", "")
                palette_files[theme_name] = os.path.join(self.themes_path, file)
        return palette_files

    def _flatten_dict(
        self, d: dict[str, Any], parent_key: str = "", sep: str = "."
    ) -> dict[str, str]:
        """Flatten a nested dictionary for placeholder replacement.

        Args:
            d (dict): The dictionary to flatten.
            parent_key (str): The base key string.
            sep (str): Separator between keys.

        Returns:
            dict[str, str]: Flattened dictionary with dot-separated keys.
        """
        items = {}
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.update(self._flatten_dict(v, new_key, sep=sep))
            else:
                items[new_key] = str(v)
        return items

    def available_themes(self) -> list[str]:
        """Return a list of available theme names.

        Returns:
            list[str]: List of available theme names.
        """
        return list(self.palette_paths.keys())

    def set_theme(self, theme_name: str, app: Optional[QApplication] = None) -> bool:
        """Set and apply the theme by name.

        Replaces color placeholders from the palette.

        Args:
            theme_name (str): The name of the theme to apply.
            app (QApplication, optional): The QApplication instance.

        Returns:
            bool: True if the theme was applied, False otherwise.
        """
        palette_path = self.palette_paths.get(theme_name)
        if not palette_path or not os.path.exists(palette_path):
            print(f"[ThemeManager] Palette JSON file not found for theme: {theme_name}")
            return False
        with open(palette_path, "r", encoding="utf-8") as pf:
            palette = json.load(pf)
        self.current_theme = theme_name
        self.current_palette = palette
        print(f"[ThemeManager] Theme '{theme_name}' palette loaded successfully.")
        self.theme_changed.emit()
        return True

    def get_current_theme(self) -> Optional[str]:
        """Get the name of the currently applied theme.

        Returns:
            Optional[str]: The name of the current theme, or None if not set.
        """
        return self.current_theme

    def load_stylesheet_with_theme(self, qss_path: str) -> str:
        """Load a QSS file and apply the current palette.

        Supports both absolute and relative paths.

        Args:
            qss_path (str): Path to the QSS file.

        Returns:
            str: The QSS with color placeholders replaced, or an empty string if not
            found.
        """
        if not os.path.isabs(qss_path):
            rel_path = os.path.join(self.themes_path, qss_path)
            if os.path.exists(rel_path):
                qss_path = rel_path
        if not os.path.exists(qss_path):
            print(f"[ThemeManager] QSS file not found: {qss_path}")
            return ""
        with open(qss_path, "r", encoding="utf-8") as f:
            qss = f.read()
        palette = self.current_palette
        if palette:
            flat_palette = self._flatten_dict(palette)
            for key, value in flat_palette.items():
                qss = qss.replace(f"{{{key}}}", value)
        return qss
