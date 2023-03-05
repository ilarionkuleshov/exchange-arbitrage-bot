from abc import abstractmethod
from typing import Callable, Generator, Union

from scrapy import Request

from .base_client import BaseClient
from items import LastTradeItem
from interfaces import MarketSymbol
from utils import format_exchange_name


class BaseLastTradeClient(BaseClient):
    @abstractmethod
    def build_api_endpoint_url(self, symbol: MarketSymbol) -> str:
        pass

    def build_request(
        self, spider_callback: Callable, symbol: MarketSymbol
    ) -> Request:
        self.logger.info(
            f"Building request for "
            f"{format_exchange_name(self.exchange_name)} last trade client..."
        )
        request_url = self.build_api_endpoint_url(symbol)
        return Request(
            url=request_url,
            callback=spider_callback,
            meta={
                "exchange_name": self.exchange_name
            }
        )

    @abstractmethod
    def parse(
        self, response: Union[dict, list], market_id: int
    ) -> Generator[LastTradeItem, None, None]:
