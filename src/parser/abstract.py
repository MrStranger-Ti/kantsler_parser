import abc
import logging
from typing import Any

import requests
from requests import Response

log = logging.getLogger(__name__)


class XMLParser(abc.ABC):
    def __init__(
        self,
        url: str,
        params: dict[str, str] | None = None,
        headers: dict[str, str] | None = None,
    ):
        self.url: str = url
        self.params: dict[str, str] = params or {}
        self.headers: dict[str, str] = headers or {}

    def get_response(self) -> Response:
        try:
            response = requests.get(
                url=self.url,
                params=self.params,
                headers=self.headers,
                timeout=5,
            )
            if response.status_code != 200:
                raise requests.exceptions.HTTPError(
                    f"Status code is not 200 ({response.status_code})"
                )

        except (requests.exceptions.Timeout, requests.exceptions.HTTPError) as exc:
            log.error(str(exc))
            raise exc

        except requests.exceptions.ConnectionError as exc:
            log.error(f"{str(exc)}. Maybe you set invalid URL?")
            raise exc

        return response

    def get_data(self) -> Any:
        response = self.get_response()
        xml = response.content
        parsed_data = self._parse(xml)
        return parsed_data

    @abc.abstractmethod
    def _parse(self, xml: bytes) -> Any:
        pass
