from abc import abstractmethod
from typing import Callable, Generator, Union

from scrapy import Request

from .base_client import BaseClient
from items import MarketItem
from utils import format_exchange_name


class BaseTickerClient(BaseClient):
    @property
    @abstractmethod
    def api_endpoint_url(self) -> str:
        pass

    def build_request(self, spider_callback: Callable) -> Request:
        self.logger.info(
            f"Building request for "
            f"{format_exchange_name(self.exchange_name)} ticker client..."
        )
        return Request(
            url=self.api_endpoint_url,
            callback=spider_callback,
            meta={
                "exchange_name": self.exchange_name
            }
        )

    @abstractmethod
    def parse(self, json_response: Union[dict, list]) -> Generator[MarketItem, None, None]:
        pass
