__all__ = [
    "DataManager",
    "Handler",
    "Formatter",
    "FormatHandler",
]

from typing import Any

from typing_extensions import TypeVar

from src.handling.manager.format import Formatter
from src.handling.manager.handling import Handler, FormatHandler
from src.handling.manager.mixins import ContextMixin

T = TypeVar("T", bound=Handler)


class DataManager(ContextMixin):
    def __init__(
        self,
        handlers_classes: list[type[T]],
        context: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(context=context)
        self.handlers_classes: list[type[T]] = handlers_classes
        self.handlers_results: dict[str, Any] = {}
        self.context = context

    def _set_handler_data(self, name: str, value: Any) -> None:
        self.handlers_results[name] = value

    def _run_handlers(self, data: Any) -> None:
        for handler_class in self.handlers_classes:
            handler = handler_class(context=self.context)
            result = handler.execute(data=data)
            if result:
                self._set_handler_data(name=handler.name, value=result)

    def manage(self, data: Any) -> None:
        prepared_data = self.manage_before(data=data)
        self._run_handlers(prepared_data)
        self.manage_after(data=prepared_data)

    def manage_before(self, data: Any) -> Any:
        """
        Preparing data before handling.
        """
        return data

    def manage_after(self, data: Any) -> None:
        """
        Finish managing data after manage.
        """
        return None
