from typing import Any, Callable, Dict, Generic, Optional, TypeVar

T = TypeVar("T")


class classproperty(Generic[T]):
    def __init__(self, func: Callable[[Any], T]) -> None:
        self.func = func

    def __get__(self, instance: Any, owner: Any) -> T:
        return self.func(owner)


class Settings:
    _values: Dict[str, Optional[str]] = {}

    def __init__(self):
        raise TypeError("This class cannot be initialized.")

    @classmethod
    def create(cls, default_directory: Optional[str]):
        if cls._values:
            raise ValueError("Settings have already been initialized.")
        cls._values["default_directory"] = default_directory

    @classproperty
    def default_directory(cls) -> Optional[str]:
        return cls._values["default_directory"]
