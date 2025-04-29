import abc
from typing import Any

from typing_extensions import TypeVar

from src.handling.manager.formatter import Formatter
from src.handling.manager.mixins import ContextMixin

T = TypeVar("T", bound=Formatter)


class Handler(ContextMixin, abc.ABC):
    def __init__(self, *args, name: str | None = None, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.name = name or self.__class__.__name__.replace("Handler", "").lower()

    def execute(self, data: Any) -> Any:
        return self.execute(data=data)

    @abc.abstractmethod
    def handle(self, data: Any) -> Any:
        pass


class FormatHandler(Handler):
    formatters_classes: list[T] | None = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.formatters_classes: list[T] = self.formatters_classes or []

    def process_formatters(self, data: Any) -> dict[str, Any]:
        formated_data = {}
        for formatter_class in self.formatters_classes:
            formatter = formatter_class(context=self.context)
            formatter_data = formatter.format(data=data)

            if formatter_data:
                formated_data.update(formatter_data)

        return formated_data or data

    def execute(self, data: Any) -> Any:
        formatted_data = self.format(data)
        return self.handle(data=formatted_data)

    @abc.abstractmethod
    def format(self, data: Any) -> Any:
        """
        Formating data.

        This method can format data by itself or call process_formatters method
        to delegate formatting to Formatter objects.
        """
        pass

    @abc.abstractmethod
    def handle(self, data: Any) -> Any:
        pass
