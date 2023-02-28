from abc import abstractmethod
from typing import Callable, Generator, Union, Optional

from scrapy import Request

from .base_client import BaseClient
from items import MarketItem
from utils import format_exchange_name


class BaseTickerClient(BaseClient):
    @property
    @abstractmethod
    def api_endpoint_url(self) -> str:
        pass

    @property
    def additional_api_endpoint_url(self) -> Optional[str]:
        return None

    def build_request(
        self, spider_callback: Callable, url: str = None, meta: dict = {}
    ) -> Request:
        self.logger.info(
            f"Building request for "
            f"{format_exchange_name(self.exchange_name)} ticker client..."
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

    def build_additional_request(
        self, spider_callback: Callable, primary_response: Union[dict, list]
    ) -> Optional[Request]:
        if not self.additional_api_endpoint_url:
            return None
        return self.build_request(
            spider_callback,
            self.additional_api_endpoint_url,
            {"primary_response": primary_response}
        )

    @abstractmethod
    def parse(
        self,
        primary_response: Union[dict, list],
        additional_response: Optional[Union[dict, list]] = None
    ) -> Generator[MarketItem, None, None]:
        pass
