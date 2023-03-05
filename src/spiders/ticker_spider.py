import json
from typing import Generator, Union, Optional

from scrapy import Request, Item
from scrapy.http import Response

from .base import BaseSessionSpider
from pipelines import TickerDBPipeline, MarketFilterPipeline
from crypto.managers import TickerManager
from utils import get_import_full_name, safe_execute


class TickerSpider(BaseSessionSpider):
    name = "ticker_spider"
    custom_settings = {
        "ITEM_PIPELINES": {
            get_import_full_name(MarketFilterPipeline): 299,
            get_import_full_name(TickerDBPipeline): 300
        }
    }
    ticker_manager: TickerManager

    def __init__(self, session_id: str, *args, **kwargs) -> None:
        super().__init__(session_id, *args, **kwargs)
        self.ticker_manager = TickerManager(self.session_settings.exchanges)

    def start_requests(self) -> Generator[Request, None, None]:
        for client in self.ticker_manager.iterate():
            yield client.build_request(self.parse)

    def parse(self, response: Response) -> Generator[Union[Request, Item], None, None]:
        exchange_name = response.meta["exchange_name"]
        if primary_response := self._get_json_response(response, exchange_name):
            ticker_client = self.ticker_manager.get_client(exchange_name)
            if additional_request := ticker_client.build_additional_request(
                self.additional_parse, primary_response
            ):
                yield additional_request
                return
            yield from ticker_client.parse(primary_response)

    def additional_parse(self, response: Response) -> Generator[Union[Request, Item], None, None]:
        exchange_name = response.meta["exchange_name"]
        if additional_response := self._get_json_response(response, exchange_name):
            ticker_client = self.ticker_manager.get_client(exchange_name)
            yield from ticker_client.parse(
                response.meta["primary_response"], additional_response
            )

    def _get_json_response(
        self, response: Response, exchange_name: str
    ) -> Optional[Union[dict, list]]:
        json_response = safe_execute(json.loads, response.text)
        if type(json_response) not in [dict, list]:
            self.logger.error(
                f"Recieve empty response from "
                f"{exchange_name} ticker client"
            )
            return None
        return json_response
