from abc import abstractmethod
from typing import Callable, Generator

from scrapy.http import Request, Response

from .base_client import BaseClient
from items import MarketItem


class BaseTickerClient(BaseClient):
    @property
    @abstractmethod
    def api_endpoint_url(self) -> str:
        pass

    def build_request(self, spider_callback: Callable) -> Request:
        return Request(
            url=self.api_endpoint_url,
            callback=spider_callback
        )

    @abstractmethod
    def parse(self, response: Response) -> Generator[MarketItem, None, None]:
        pass
