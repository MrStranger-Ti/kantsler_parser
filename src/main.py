from src import config
from src.parser.parser import KantslerParser
from src.excel.manager import ExcelManager


def main() -> None:
    parser = KantslerParser(url=config.URL)
    rows = parser.get_data()

    with ExcelManager(rows=rows) as manager:
        manager.insert_rows()


if __name__ == "__main__":
    main()
