import sys


def main() -> None:
    categories = get_categories()
    products = get_products()
    products_xml = get_products_xml()

    manager = SamsonOptAPIManager(
        handlers_classes=[
            ExcelHandler,
        ],
        context={
            "categories": categories,
            "products_xml": products_xml,
        },
    )
    manager.manage(data=products)


if __name__ == "__main__":
    try:
        from src.api_service.requests import (
            get_categories,
            get_products,
            get_products_xml,
        )
        from src.handling.excel.handler import ExcelHandler
        from src.handling.manager import DataManager
        from src.handling.managers import SamsonOptAPIManager

        main()
    except Exception as exc:
        print(f"{exc.__class__.__name__}: {exc}")
        input("Press Enter to close console...")
        sys.exit(1)
