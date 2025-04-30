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


# Requests

API_KEY = _config.get("required", "API_KEY")
if not API_KEY:
    log.error("No API_KEY. Set API_KEY option in config.ini")
    raise ValueError("API_KEY option is required")

XML_URL = _config.get("required", "XML_URL")
if not XML_URL:
    log.error("No XML_URL. Set XML_URL option in config.ini")
    raise ValueError("XML_URL option is required")

PRODUCTS_URL = "https://api.samsonopt.ru/v1/sku"

CATEGORIES_URL = "https://api.samsonopt.ru/v1/category"

PAGINATION_PAGES = _config.get("optional", "PAGINATION_PAGES")
if PAGINATION_PAGES.isdigit():
    PAGINATION_PAGES = int(PAGINATION_PAGES)
else:
    PAGINATION_PAGES = 5

PAGINATION_COUNT = _config.get("optional", "PAGINATION_COUNT")
if PAGINATION_COUNT.isdigit():
    PAGINATION_COUNT = int(PAGINATION_COUNT)
else:
    PAGINATION_COUNT = 10000

TIMEOUT = _config.get("optional", "TIMEOUT")
if TIMEOUT.isdigit():
    TIMEOUT = int(TIMEOUT)
else:
    TIMEOUT = 10

PREV_DATA_PATH = BASE_DIR / "prev_data"
os.makedirs(PREV_DATA_PATH, exist_ok=True)


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
    "vendor_code": 7,
    "description": 8,
    "url": 10,
    "price": 11,
    "nds": 16,
    "category": 17,
    "images": 19,
    "guarantee": 21,
    "characteristics_text": 23,
    "unit": 24,
    "available": 25,
    "weight": 34,
    "depth": 35,
    "width": 36,
    "height": 37,
}

START_ROW = 5
START_COL = 2
