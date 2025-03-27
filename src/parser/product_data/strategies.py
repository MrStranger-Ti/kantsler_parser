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

        for brand in config.BRANDS:
            if brand and re.search(rf"\s+{brand}\s+", cleared_text):
                return brand

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
        soup = bs4.BeautifulSoup(text, "lxml")

        self.text: str = str(soup.select_one("ul, ol"))
        self.default_value: str = default_value
        self.dict: dict[str, str] = {}

        for item in soup.select("ul > li, ol > li"):
            if ": " in item.text:
                name, value = item.text.split(": ", maxsplit=1)
                cleared_name = name.split()[0].lower()
                self.dict[cleared_name] = value.strip()

    def get(self, names: list[str]) -> str:
        for name in names:
            characteristic = self.dict.get(name.lower(), self.default_value)
            if characteristic:
                break

        return characteristic or self.default_value

    @property
    def weight(self) -> str:
        return self.get(self.WEIGHT_ASSOCIATIONS)

    @property
    def guarantee(self) -> str:
        return self.get(self.GUARANTEE_ASSOCIATIONS)

    # @property
    # def dimensions(self) -> tuple[str, str, str]:
    #     """
    #     Получение длины, ширины и высоты.
    #     """
    #
    #     dimensions_text = self.get("Размер в упаковке")
    #     match = re.fullmatch(r"(\d+\.\d+)x(\d+\.\d+)x(\d+\.\d+).*", dimensions_text)
    #     dimensions = (
    #         (match.group(1), match.group(2), match.group(3)) if match else ("", "", "")
    #     )
    #     return dimensions


class CharacteristicStrategy(XMLProductDataStrategy):
    def get_product_data(self, description_text: str) -> ProductCharacteristics:
        return ProductCharacteristics(text=description_text)
