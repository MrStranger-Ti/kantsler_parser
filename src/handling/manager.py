from typing import Any

from typing_extensions import TypeVar

from src.handling.base.handler import Handler

T = TypeVar("T", bound=Handler)


class DataManager:
    def __init__(self, handlers: list[T]) -> None:
        self._handlers: list[T] = handlers
        self.handlers_results: dict[str, Any] = {
            handler.name: None for handler in self._handlers
        }

    @property
    def handlers(self) -> list[T]:
        return self._handlers

    @handlers.setter
    def handlers(self, handlers: list[T]) -> None:
        self._handlers = handlers

    def _set_handler_data(self, name: str, value: Any) -> None:
        self.handlers_results[name] = value

    def manage(self, data: Any) -> None:
        for handler in self._handlers:
            result = handler.execute(data=data)
            if result:
                self._set_handler_data(name=handler.name, value=result)
