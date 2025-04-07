from typing import Optional


class Settings:
    _instance = None

    @classmethod
    def create(cls, default_directory: Optional[str]):
        if cls._instance is not None:
            raise ValueError("Settings were already initialized.")
        cls._instance = super(Settings, cls).__new__(cls)
        cls._instance.__init__(default_directory=default_directory)

    def __new__(cls):
        if cls._instance is None:
            raise ValueError("Settings should first be initialized with 'create'.")
        return cls._instance

    def __init__(self, **kwargs):
        if not hasattr(self, "_settings"):
            self._settings = dict(kwargs)

    @classmethod
    @property
    def default_directory(cls) -> Optional[str]:
        """Where to look for battle map files by default."""
        return cls._instance._settings["default_directory"]
