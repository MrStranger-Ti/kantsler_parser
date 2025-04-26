from typing import Any

from src.handling.base.formatter import Formatter


def get_types_values(data: list[dict[str, str]], types: list[str]) -> dict[str, str]:
    result = {}
    for item in data:
        if (package_type := item.get("type")) in types:
            result.update({package_type: item.get("value")})

    return result


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
    TYPES = ["infiltration", "contract"]
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

    DEPTH_LEVEL_FIELD = "depth_level"
    FILTER_VALUE = "1"

    def filter_categories(
        self,
        categories: dict[str, list[dict[str, Any]]],
    ) -> list[dict[str, Any]]:
        return [
            category
            for category in categories.get("data") or []
            if category.get(self.DEPTH_LEVEL_FIELD) == self.FILTER_VALUE
        ]

    def format(self, data: Any) -> dict[str, Any]:
        formatted_data = {}

        category_list = data.get(self.CATEGORY_FIELD)
        if category_list is None:
            return formatted_data

        categories = self.get_context("categories")
        filtered_categories = self.filter_categories(categories=categories)

        for category in filtered_categories:
            if category.get("id") in category_list:
                formatted_data.update(
                    {self.FORMATTED_CATEGORY_FIELD: category.get("name")}
                )
                break

        return formatted_data


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


class PackageFormatter(Formatter):
    PACKAGE_FIELD = "package_list"
    FORMATTED_PACKAGE_FIELDS = [
        "unit",
    ]

    def format(self, data: Any) -> dict[str, Any]:
        formatted_data = {}

        package_list = data.get(self.PACKAGE_FIELD)
        if package_list is None:
            return formatted_data

        fields = get_types_values(
            data=package_list, types=self.FORMATTED_PACKAGE_FIELDS
        )
        formatted_data.update(fields)

        return formatted_data


class SizesFormatter(Formatter):
    SIZES_FIELD = "package_size"
    FORMATTED_SIZES_FIELDS = [
        "height",
        "width",
        "depth",
    ]

    def format(self, data: Any) -> dict[str, Any]:
        formatted_data = {}

        sizes = data.get(self.SIZES_FIELD)
        if sizes is None:
            return formatted_data

        fields = get_types_values(data=sizes, types=self.FORMATTED_SIZES_FIELDS)
        formatted_data.update(fields)

        return formatted_data
