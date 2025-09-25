import configparser
import os
from typing import Optional

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "../../config.ini")


class AppConfig:
    """Application configuration loader and accessor."""

    config: Optional[configparser.ConfigParser] = None

    @classmethod
    def initialize(cls, path: str = CONFIG_PATH) -> None:
        """Initialize configuration from the given path.

        Args:
            path (str): The path to the configuration file.
        """
        cls.config = configparser.ConfigParser()
        cls.config.read(path)

    @classmethod
    def get_var(cls, section: str, key: str) -> str:
        """Get the variable from the config file.

        Args:
            section (str): The section in the config file.
            key (str): The key in the section.

        Returns:
            str: The value from the config file.

        Raises:
            RuntimeError: If AppConfig is not initialized.
        """
        if cls.config is None:
            raise RuntimeError("AppConfig not initialized")
        return cls.config.get(section, key)

    @classmethod
    def app_name(cls) -> str:
        """Get the application name.

        Returns:
            str: The application name.
        """
        return cls.get_var("app", "name")

    @classmethod
    def window_width(cls) -> int:
        """Get the window width.

        Returns:
            int: The window width.
        """
        return int(cls.get_var("window", "width"))

    @classmethod
    def window_height(cls) -> int:
        """Get the window height.

        Returns:
            int: The window height.
        """
        return int(cls.get_var("window", "height"))
