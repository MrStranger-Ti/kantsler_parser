import logging
import re
import string
from xml.etree.ElementTree import Element

import bs4

from src import config
from src.parser.product_data.abstract import XMLProductDataStrategy
from src.utils.formating import clear_html_entity

log = logging.getLogger(__name__)


class ChildElementTextStrategy(XMLProductDataStrategy):
    def get_product_data(self, child_name: str) -> str:
        text = ""
        try:
            text = self.element.find(child_name).text
        except AttributeError:
            log.warning(
                f"Element {self.element.get("id")} doesn't have tag {child_name}"
            )

        finally:
            cleared_text = clear_html_entity(text)
            return cleared_text


class AttributeElementStrategy(XMLProductDataStrategy):
    def get_product_data(self, attr_name: str) -> str:
        return self.element.get(attr_name, "")


class BrandStrategy(XMLProductDataStrategy):
    NONAME_VALUE = config.NONAME_BRAND_VALUE

    def get_product_data(self, name: str) -> str:
        trans_table = str.maketrans("", "", string.punctuation)
        cleared_text = name.translate(trans_table)

        for word in cleared_text.split():
            if word in config.BRANDS:
                return word

        return self.NONAME_VALUE


class CategoryStrategy(XMLProductDataStrategy):
    def __init__(self, element: Element, products_categories: dict[str, str]) -> None:
        super().__init__(element)
        self.products_categories = products_categories

    def get_product_data(self, category_id: str | int) -> str:
        return self.products_categories.get(str(category_id))


class ProductCharacteristics:
    WEIGHT_ASSOCIATIONS = ["Масса", "Вес"]
    GUARANTEE_ASSOCIATIONS = ["Гарантия"]

    def __init__(self, text: str, default_value: str = "") -> None:
        self.default_value: str = default_value
        self.dict: dict[str, str] = {}

        soup = bs4.BeautifulSoup(text, "lxml")
        for item in soup.select("ul > li, ol > li"):
            if ": " in item.text:
                name, value = item.text.split(": ", maxsplit=1)
                cleared_name = name.split()[0].lower()
                self.dict[cleared_name] = value.strip(" .")

    def __str__(self) -> str:
        return self.text

    def get(self, associations: list[str]) -> str:
        for name in associations:
            characteristic = self.dict.get(name.lower(), self.default_value)
            if characteristic:
                break

        return characteristic or self.default_value

    @property
    def text(self) -> str:
        rows = [f"{name}|{value};" for name, value in self.dict.items()]
        return "\n".join(rows)

    @property
    def weight(self) -> str:
        return self.get(self.WEIGHT_ASSOCIATIONS)

    @property
    def guarantee(self) -> str:
        return self.get(self.GUARANTEE_ASSOCIATIONS)


class CharacteristicStrategy(XMLProductDataStrategy):
    def get_product_data(self, description_text: str) -> ProductCharacteristics:
        return ProductCharacteristics(text=description_text)
