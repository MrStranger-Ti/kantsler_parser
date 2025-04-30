from typing import Any

from src.handling.manager import Formatter


class ConstantFieldsFormatter(Formatter):
    def format(self, data: Any) -> dict[str, Any]:
        return {
            "available": "под заказ",
        }


class DefaultFieldsFormatter(Formatter):
    DEFAULT_FIELDS = [
        "id",
        "sku",
        "name",
        "brand",
        "vendor_code",
        "description",
        "manufacturer",
        "nds",
        "weight",
    ]

    def format(self, data: dict[str, Any]) -> dict[str, Any]:
        return {
            field: value
            for field, value in data.items()
            if field in self.DEFAULT_FIELDS
        }


class SKUFormatter(Formatter):
    SKU_FIELD = "sku"
    FORMATTED_SKU_FIELD = "sku"

    def format(self, data: Any) -> dict[str, Any]:
        formatted_data = {}
        if sku := data.get(self.SKU_FIELD):
            formatted_data.update({self.FORMATTED_SKU_FIELD: str(sku) + "S"})

        return formatted_data


class PriceFormatter(Formatter):
    PRICE_FIELD = "price_list"
    TYPES = ["infiltration"]
    FORMATTED_PRICE_FIELD = "price"

    def format(self, data: Any) -> dict[str, Any]:
        formatted_data = {}

        price_list = data.get(self.PRICE_FIELD)
        if price_list is None:
            return formatted_data

        for price_item in price_list:
            if price_item["type"] in self.TYPES:
                formatted_data.update({self.FORMATTED_PRICE_FIELD: price_item["value"]})
                break

        return formatted_data


class CategoryFormatter(Formatter):
    CATEGORY_FIELD = "category_list"
    FORMATTED_CATEGORY_FIELD = "category"

    def find_category_by_id(self, category_id: str) -> dict[str, Any]:
        categories = self.get_context("categories")
        while len(categories) > 1:
            left = categories[: len(categories) // 2]
            right = categories[len(categories) // 2 :]

            compare_id = left[-1].get("id")
            if compare_id is None:
                return {}

            if str(category_id) <= str(compare_id):
                categories = left
            else:
                categories = right

        return categories[0] if categories else {}

    def find_root_category(self, category_id: str) -> dict[str, Any]:
        category = self.find_category_by_id(category_id=category_id)
        while category.get("parent_id"):
            parent_category_id = str(category.get("parent_id"))
            if parent_category_id:
                category = self.find_category_by_id(category_id=parent_category_id)

        return category

    def format(self, data: Any) -> dict[str, Any]:
        category_list = data.get(self.CATEGORY_FIELD)
        if category_list is None:
            return {}

        root_category = self.find_root_category(str(category_list[0]))
        return {
            self.FORMATTED_CATEGORY_FIELD: root_category.get("name", ""),
        }


class ImagesFormatter(Formatter):
    IMAGES_FIELD = "photo_list"
    FORMATTED_IMAGES_FIELD = "images"

    def format(self, data: Any) -> dict[str, Any]:
        formatted_data = {}

        images_list = data.get(self.IMAGES_FIELD)
        if images_list is None:
            return formatted_data

        formatted_data.update({self.FORMATTED_IMAGES_FIELD: ",".join(images_list)})

        return formatted_data


class CharacteristicsFormatter(Formatter):
    CHARACTERISTICS_FIELD = "characteristic_list"
    FORMATTED_CHARACTERISTICS_FIELD = "characteristics_text"

    def format(self, data: Any) -> dict[str, Any]:
        formatted_data = {}

        if characteristics := data.get(self.CHARACTERISTICS_FIELD):
            formatted_characteristics = []
            for characteristic in characteristics:
                formatted_characteristic = characteristic.replace(": ", "|")
                formatted_characteristics.append(formatted_characteristic)

            formatted_data.update(
                {
                    self.FORMATTED_CHARACTERISTICS_FIELD: ";".join(
                        formatted_characteristics
                    )
                }
            )

        return formatted_data


class ListFieldFormatter(Formatter):
    LIST_FIELD = None
    FORMATTED_LIST_FIELDS = None

    def format(self, data: Any) -> dict[str, Any]:
        formatted_data = {}

        package_list = data.get(self.LIST_FIELD)
        if package_list is None:
            return formatted_data

        fields = {}
        for item in package_list:
            if (package_type := item.get("type")) in self.FORMATTED_LIST_FIELDS or []:
                fields.update({package_type: item.get("value")})

        formatted_data.update(fields)

        return formatted_data


class PackageFormatter(ListFieldFormatter):
    LIST_FIELD = "package_list"
    FORMATTED_LIST_FIELDS = [
        "unit",
    ]


class SizesFormatter(ListFieldFormatter):
    LIST_FIELD = "package_size"
    FORMATTED_LIST_FIELDS = [
        "height",
        "width",
        "depth",
    ]
