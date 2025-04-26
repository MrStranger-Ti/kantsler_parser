import sys


def main() -> None:
    categories = get_categories()
    products = get_products()

    manager = DataManager(
        handlers=[
            ExcelHandler(context={"categories": categories}),
        ],
    )
    manager.manage(data=products)


if __name__ == "__main__":
    try:
        from src.api_service.requests import get_categories, get_products
        from src.handling.excel.handler import ExcelHandler
        from src.handling.manager import DataManager

        main()
    except Exception as exc:
        print(f"Error: {exc}")
        input("Press Enter to close console...")
        sys.exit(1)
