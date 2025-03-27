from typing import Any

from src.parser.product_data.abstract import XMLProductDataStrategy


class XMLProductContext:
    def __init__(self, strategy: XMLProductDataStrategy | None = None) -> None:
        self._strategy: XMLProductDataStrategy | None = strategy

    @property
    def strategy(self) -> XMLProductDataStrategy:
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: XMLProductDataStrategy) -> None:
        self._strategy = strategy

    def get_data(self, *args, **kwargs) -> Any:
        if self._strategy is None:
            raise AttributeError("Impossible to get data without element instance")

        return self._strategy.get_product_data(*args, **kwargs)
