import json
import os
from typing import Dict


class TranslateManager:
    """Manager for loading and providing translations from JSON files."""

    translations: Dict[str, str]

    def __init__(self, locales_path: str, default_language: str = "en") -> None:
        """Initialize the TranslateManager.

        Args:
            locales_path (str): Path to the locales directory.
            default_language (str): The default language code.
        """
        self.locales_path = locales_path
        self.current_language = default_language
        self.translations = {}
        self.load_language(default_language)

    def available_languages(self) -> list[str]:
        """Get a list of available language codes.

        Returns:
            list: A list of available language codes.
        """
        langs: list[str] = []
        for lang_dir in os.listdir(self.locales_path):
            lang_path = os.path.join(self.locales_path, lang_dir)
            if os.path.isdir(lang_path):
                json_files = [f for f in os.listdir(lang_path) if f.endswith(".json")]
                if json_files:
                    langs.append(lang_dir)
        return langs

    def load_language(self, language_code: str) -> bool:
        """Load translations for the given language code.

        Args:
            language_code (str): The language code to load.

        Returns:
            bool: True if loaded successfully, False otherwise.
        """
        lang_dir = os.path.join(self.locales_path, language_code)
        json_files = [f for f in os.listdir(lang_dir) if f.endswith(".json")]
        if not json_files:
            return False
        json_file = os.path.join(lang_dir, json_files[0])
        with open(json_file, "r", encoding="utf-8") as f:
            self.translations = json.load(f)
        self.current_language = language_code
        return True

    def t(self, key: str) -> str:
        """Translate a key to the current language.

        Args:
            key (str): The translation key.

        Returns:
            str: The translated string, or the key if not found.
        """
        return self.translations.get(key, key)
