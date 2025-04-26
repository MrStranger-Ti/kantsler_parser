import time

from fake_useragent import UserAgent
from tqdm import tqdm

from src import config
from src.api_service.client import HttpClient
from src.utils.tqdm import GETTING_PRODUCTS_CONFIG

ua = UserAgent()

headers = {
    "Accept": "application/json",
    "User-Agent": ua.random,
    "Accept-Encoding": "gzip",
}

client = HttpClient()


def get_categories() -> list[dict[str, str]]:
    categories = client.get_data(
        url="https://api.samsonopt.ru/v1/category",
        headers=headers,
        params={"api_key": config.API_KEY},
        timeout=config.TIMEOUT,
    )
    return categories


def get_products() -> dict[str, list[dict[str, str]]]:
    t = tqdm(**GETTING_PRODUCTS_CONFIG)

    products = {}
    for page in range(1, config.PAGINATION_PAGES + 1):
        data = client.get_data(
            url="https://api.samsonopt.ru/v1/sku",
            headers=headers,
            params={
                "api_key": config.API_KEY,
                "pagination_count": config.PAGINATION_COUNT,
                "pagination_page": page,
            },
            timeout=10,
        )

        page_products = data.get("data", [])
        products["data"] = products.get("data", []) + page_products

        t.postfix["value"] += len(page_products)
        t.update()

        time.sleep(1)

        if len(page_products) < config.PAGINATION_COUNT:
            break

    return products
