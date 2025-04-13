import io
import logging
from lxml import etree

from tqdm import tqdm

from src.excel.column import Column
from src.parser.abstract import XMLParser
from src.parser.product_data.context import XMLProductContext
from src.parser.product_data.strategies import (
    ChildElementTextStrategy,
    AttributeElementStrategy,
    BrandStrategy,
    CharacteristicStrategy,
    CategoryStrategy,
    MinOrderStrategy,
)
from src.utils.tqdm import PRODUCTS_PARSING_CONFIG

log = logging.getLogger(__name__)


class KantslerParser(XMLParser):
    def _parse(self, xml: bytes) -> list[dict[str, str]]:
        categories = {}
        offers_rows = []

        t = tqdm(**PRODUCTS_PARSING_CONFIG)
        for _, element in etree.iterparse(io.BytesIO(xml), events=("end",)):
            if element.tag == "category":
                context = XMLProductContext()

                context.strategy = AttributeElementStrategy(element=element)
                category_name = element.text
                category_id = context.get_data("id")
                categories[category_id] = category_name

                log.info(f"Category {category_name!r} was parsed")

            elif element.tag == "offer":
                context = XMLProductContext()

                context.strategy = ChildElementTextStrategy(element=element)
                description = context.get_data(child_name="description")
                name = context.get_data(child_name="name")
                url = context.get_data(child_name="url")
                price = context.get_data(child_name="price")
                img_url = context.get_data(child_name="picture")

                _category_id = context.get_data(child_name="categoryId")

                context.strategy = AttributeElementStrategy(element=element)
                sku = context.get_data("id") + "S"

                context.strategy = BrandStrategy(element=element)
                brand = context.get_data(name=name)

                context.strategy = CategoryStrategy(
                    element=element,
                    products_categories=categories,
                )
                category = context.get_data(category_id=_category_id)

                context.strategy = CharacteristicStrategy(element=element)
                characteristics = context.get_data(description_text=description)
                weight = characteristics.weight
                guarantee = characteristics.guarantee
                characteristics_text = characteristics.text

                context.strategy = MinOrderStrategy(element=element)
                min_order = context.get_data(child_name="sales_notes")

                unit_measurement = "Шт"
                available = "под заказ"
                vat = "20"

                offers_rows.append(
                    {
                        "sku": sku,
                        "name": name,
                        "brand": brand,
                        "description": description,
                        "url": url,
                        "price": price,
                        "vat": vat,
                        "category": category,
                        "img_url": img_url,
                        "guarantee": guarantee,
                        "characteristics_text": characteristics_text,
                        "unit_measurement": unit_measurement,
                        "available": available,
                        "min_order": min_order,
                        "weight": weight,
                    },
                )

                element.clear()

                t.postfix["value"] += 1
                t.update()
                log.info(f"Offer {name!r} was parsed")

        return offers_rows
