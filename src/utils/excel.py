import logging

from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from tqdm import tqdm

from src.utils.tqdm import CREATING_EXCEL_CONFIG
from src import config

log = logging.getLogger(__name__)


def create_workbook() -> Workbook:
    workbook = Workbook()
    sheet: Worksheet = workbook.active
    sheet.title = config.SHEET_NAME
    sheet.append(config.COLS_NAMES)
    return workbook


def insert_rows(rows: list[list[str]]) -> None:
    log.info("Starting to prepare excel file")

    workbook = create_workbook()
    sheet = workbook.active

    for row_num, row in enumerate(tqdm(rows, **CREATING_EXCEL_CONFIG), start=2):
        for col_num, col_value in enumerate(row, start=1):
            sheet.cell(row=row_num, column=col_num, value=col_value)

    log.info("Saving file")
    try:
        workbook.save(config.RESULT_FILE_DIR)
    except PermissionError as exc:
        log.error(f"{str(exc)}. Close result excel file and try again.")
        raise exc

    log.info("Excel file created")
