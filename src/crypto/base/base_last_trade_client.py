from abc import abstractmethod
from typing import Callable, Generator, Union, Optional

from scrapy import Request

from .base_client import BaseClient
from items import MarketItem
from utils import format_exchange_name


class BaseLastTradeClient(BaseClient):
    @property
    @abstractmethod
    def api_endpoint_url(self) -> str:
        pass

    def build_request(
        self, spider_callback: Callable, url: str = None, meta: dict = {}
    ) -> Request:
        self.logger.info(
            f"Building request for "
            f"{format_exchange_name(self.exchange_name)} last trade client..."
        )
        request_url = url if url else self.api_endpoint_url
        return Request(
            url=request_url,
            callback=spider_callback,
            meta={
                "exchange_name": self.exchange_name,
                **meta
            }
        )

    @abstractmethod
    def parse(
        self,
        primary_response: Union[dict, list],
        additional_response: Optional[Union[dict, list]] = None
    ) -> Generator[MarketItem, None, None]:
        pass
