import abc
from typing import Any

from src.handling.manager.mixins import ContextMixin


class Formatter(ContextMixin, abc.ABC):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    @abc.abstractmethod
    def format(self, data: Any) -> dict[str, Any]:
        pass
