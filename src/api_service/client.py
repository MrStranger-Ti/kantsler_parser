import logging
from typing import Any

import requests
from requests import Response

from src import config

log = logging.getLogger(__name__)


class HttpClient:
    def get_response(self, url: str, **kwargs) -> Response:
        try:
            response = requests.get(url, **kwargs)
            if response.status_code != 200:
                raise requests.exceptions.HTTPError(
                    f"Status code is not 200 ({response.status_code})"
                )

        except requests.exceptions.HTTPError as exc:
            msg = f"{str(exc)}. Maybe you set invalid API_KEY?"
            log.error(msg)
            raise exc.__class__(msg)

        except (requests.exceptions.Timeout, requests.exceptions.ReadTimeout) as exc:
            msg = f"{str(exc)}. No response from the server in {config.TIMEOUT} sec."
            log.error(msg)
            raise exc.__class__(msg)

        return response

    def get_data(self, url: str, **kwargs) -> Any:
        response = self.get_response(url, **kwargs)
        content_type = response.headers.get("Content-Type")

        if "application/json" in content_type:
            data = response.json()
        else:
            data = response.content

        return data
