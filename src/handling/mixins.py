from typing import Any

from src import config
from src.utils.system import get_json, save_json


class ProductsHandlerMixin:
    products_ids_path = config.PREV_DATA_PATH / "products_ids.json"

    def save_products_ids(self, products: list[dict[str, Any]]) -> None:
        products_ids = [item.get("sku") for item in products if item.get("sku")]
        save_json(path=self.products_ids_path, data=products_ids)

    def get_saved_ids(self) -> set[int]:
        saving_products_ids = get_json(self.products_ids_path)
        return set(saving_products_ids) if saving_products_ids else {}

    def sort_products_by_oldest(
        self,
        products: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        saved_products_ids = self.get_saved_ids()

        old_products = []
        new_products = []
        for index, product in enumerate(products):
            product_id = product.get("sku")
            if product_id in saved_products_ids:
                old_products.append(product)
            else:
                new_products.append(product)

        return old_products + new_products
