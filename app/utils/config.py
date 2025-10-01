import configparser

from app.utils.keys import CONFIG_PATH


class AppConfig:
    """Application configuration loader and accessor."""

    _config = configparser.ConfigParser()
    _initialized = False

    @classmethod
    def initialize(cls, path: str = CONFIG_PATH) -> None:
        """Initialize configuration from the given path.

        Args:
            path (str): The path to the configuration file.
        """
        if not cls._initialized:
            cls._config.read(path)
            cls._initialized = True

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
        if not cls._initialized:
            raise RuntimeError("AppConfig not initialized")
        return cls._config.get(section, key)

    @classmethod
    def app_name(cls) -> str:
        """Get the application name.

        Returns:
            str: The application name.
        """
        return cls._config.get("app", "name", fallback="Default App")

    @classmethod
    def window_width(cls) -> int:
        """Get the window width.

        Returns:
            int: The window width.
        """
        return cls._config.getint("window", "width", fallback=800)

    @classmethod
    def window_height(cls) -> int:
        """Get the window height.

        Returns:
            int: The window height.
        """
        return cls._config.getint("window", "height", fallback=600)
