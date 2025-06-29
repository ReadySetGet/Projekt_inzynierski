import configparser

from app.utils.keys import CONFIG_PATH


class AppConfig:
    """
    Configuration File
    """
    _config = configparser.ConfigParser()
    _initialized = False

    @classmethod
    def initialize(cls, path=CONFIG_PATH) -> None:
        if not cls._initialized:
            cls._config.read(path)
            cls._initialized = True
        """
        Perform any necessary initializations here, e.g.:
        - Loading settings from a file
        """
    def get_var(self) -> None:
        """
        Get the Var.
        """
    @classmethod
    def app_name(cls):
        return cls._config.get("app", "name", fallback="Default App")

    @classmethod
    def window_width(cls):
        return cls._config.getint("window", "width", fallback=800)

    @classmethod
    def window_height(cls):
        return cls._config.getint("window", "height", fallback=600)