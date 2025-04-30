import io
from typing import Any
from xml.etree.ElementTree import iterparse

from src.handling.manager import DataManager
from src.handling.mixins import ProductsManagerMixin


class SamsonOptAPIManager(DataManager, ProductsManagerMixin):
    def get_products_ids_from_xml(self) -> set[int]:
        xml: bytes = self.get_context("products_xml")
        return {
            int(element.get("id"))
            for _, element in iterparse(io.BytesIO(xml), events=("end",))
            if element.tag == "offer" and element.get("id").isdigit()
        }

    def prepare_categories(self) -> None:
        """
        Sorting categories by id.
        """
        categories = self.get_context("categories")
        self.context["categories"] = sorted(
            (category for category in categories.get("data") or []),
            key=lambda category: category.get("id"),
        )

    def manage_before(self, data: dict[str, dict | list]) -> list[dict[str, Any]]:
        self.prepare_categories()

        products = data.get("data", {})
        products = self.sort_products_by_oldest(products=products)
        products = self.filter_products_by_xml_ids(
            products=products,
            ids=self.get_products_ids_from_xml(),
        )
        return products

    def manage_after(self, data: list[dict[str, Any]]) -> None:
        self.save_products_ids(products=data)
