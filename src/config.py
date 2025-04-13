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

log = logging.getLogger(__name__)


# Parsing


def get_brands() -> set[str]:
    if os.path.exists(BRANDS_FILE_PATH):
        with open(BRANDS_FILE_PATH, "r", encoding="utf-8") as file:
            brands = file.read().strip()
            return set(brands.split("\n"))

    raise FileNotFoundError(f"Brand file not found: {BRANDS_FILE_PATH}")


URL = _config.get("required", "URL")
if not URL:
    log.error("No URL. Set URL option in config.ini")
    raise ValueError("URL option is required")

BRANDS_FILE_PATH = BASE_DIR / "brands.txt"

BRANDS = get_brands()

NONAME_BRAND_VALUE = _config.get("optional", "NONAME_BRAND_VALUE") or "Noname"


# Excel

TEMPLATE_PATH = BASE_DIR / "templates/template.xlsx"

if not os.path.exists(TEMPLATE_PATH):
    msg = f"Path {TEMPLATE_PATH} does not exists."
    log.error(msg)
    raise FileNotFoundError(msg)

RESULT_FILE_NAME = _config.get("optional", "RESULT_FILE_NAME") or "result.xlsx"

RESULT_FILE_DIR = _config.get("optional", "RESULT_FILE_DIR")
RESULT_FILE_DIR = (
    Path(RESULT_FILE_DIR) / RESULT_FILE_NAME
    if RESULT_FILE_DIR
    else BASE_DIR / RESULT_FILE_NAME
)

SHEET_NAME = _config.get("optional", "SHEET_NAME") or "Ассортимент"

COLS = {
    "sku": 2,
    "name": 4,
    "brand": 6,
    "description": 8,
    "url": 10,
    "price": 11,
    "vat": 16,
    "category": 17,
    "img_url": 19,
    "guarantee": 21,
    "characteristics_text": 23,
    "unit_measurement": 24,
    "available": 25,
    "min_order": 27,
    "weight": 34,
}

START_ROW = 5
START_COL = 2
