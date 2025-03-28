from src import config
from src.parser.parser import KantslerParser
from src.utils.excel import insert_rows


def main() -> None:
    parser = KantslerParser(url=config.URL)
    rows = parser.get_data()
    insert_rows(rows)


if __name__ == "__main__":
    main()
