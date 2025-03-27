import sys
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import os.path
import configparser

# Main

if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys.executable).parent
else:
    BASE_DIR = Path(__file__).parent.parent

_config = configparser.ConfigParser()
_config.read(BASE_DIR / "config.ini", encoding="utf-8")


# Logging

os.makedirs(BASE_DIR / "logs", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    handlers=[
        RotatingFileHandler(
            BASE_DIR / "logs/log",
            mode="a",
            backupCount=5,
            maxBytes=1000000,
        )
    ],
    datefmt="%d.%m.%Y-%H:%M:%S",
    format="[%(levelname)s | %(asctime)s | %(module)s:%(lineno)s] %(message)s",
)


# Parsing


def get_brands() -> list[str]:
    if os.path.exists(BRANDS_FILE_PATH):
        with open(BRANDS_FILE_PATH, "r", encoding="utf-8") as file:
            brands = file.read().strip()
            return brands.split("\n")

    raise FileNotFoundError(f"Brand file not found: {BRANDS_FILE_PATH}")


URL = _config.get("required", "URL")
if not URL:
    raise ValueError("URL option is required")

BRANDS_FILE_PATH = BASE_DIR / "brands.txt"

BRANDS = get_brands()

NONAME_BRAND_VALUE = _config.get("optional", "NONAME_BRAND_VALUE") or "Noname"


# Excel

RESULT_FILE_NAME = _config.get("optional", "RESULT_FILE_NAME") or "result.xlsx"

RESULT_FILE_DIR = _config.get("optional", "RESULT_FILE_DIR")
RESULT_FILE_DIR = (
    Path(RESULT_FILE_DIR) / RESULT_FILE_NAME
    if RESULT_FILE_DIR
    else BASE_DIR / RESULT_FILE_NAME
)

SHEET_NAME = _config.get("optional", "SHEET_NAME") or "Ассортимент"

COLS_NAMES = _config.get("optional", "COLS_NAMES")
COLS_NAMES = (
    COLS_NAMES.split(",")
    if COLS_NAMES
    else [
        "SKU",
        "Название товара",
        "Бренд",
        "Описание товара",
        "Ссылка на товар",
        "Цена",
        "НДС",
        "Категория",
        "Изображение товара",
        "Гарантия производителя",
        "Характеристики",
        "Единица измерения",
        "Доступность",
        "Вес с упаковкой",
    ]
)
