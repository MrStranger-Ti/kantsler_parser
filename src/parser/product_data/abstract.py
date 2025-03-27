import abc
from xml.etree.ElementTree import Element


class XMLProductDataStrategy(abc.ABC):
    def __init__(self, element: Element) -> None:
        self.element = element

    @abc.abstractmethod
    def get_product_data(self):
        pass
