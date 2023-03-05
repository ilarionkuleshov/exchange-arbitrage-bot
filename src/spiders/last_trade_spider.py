from typing import Generator, Union, List, Dict, Any

from scrapy import Request, Item
from scrapy.http import Response
from sqlalchemy import Connection, select

from .base import BaseSessionSpider
from pipelines import LastTradeDBPipeline
from crypto.managers import LastTradeManager
from database.models import Market, Exchange
from interfaces import MarketSymbol
from utils import get_import_full_name
from utils.status_codes import MarketStatusCodes


class LastTradeSpider(BaseSessionSpider):
    name = "last_trade_spider"
    custom_settings = {
        "ITEM_PIPELINES": {
            get_import_full_name(LastTradeDBPipeline): 300
        }
    }
    last_trade_manager: LastTradeManager
    markets_to_process: List[Dict[str, Any]] = []

    def __init__(self, session_id: str, *args, **kwargs) -> None:
        super().__init__(session_id, *args, **kwargs)
        self.last_trade_manager = LastTradeManager(self.session_settings.exchanges)

    def additional_init_from_db(self, connection: Connection) -> None:
        for market in connection.execute(
            select(Market.id, Market.symbol, Exchange.name).where(
                Market.status == MarketStatusCodes.PRICE_NOT_DEFINED.value
            ).join(
                Exchange, Market.exchange_id == Exchange.id
            )
        ):
            self.markets_to_process.append(
                {
                    "id": market[0],
                    "symbol": MarketSymbol.from_str(market[1]),
                    "exchange_name": market[2]
                }
            )

    def start_requests(self) -> Generator[Request, None, None]:
        for market in self.markets_to_process:
            client = self.last_trade_manager.get_client(market["exchange_name"])
            yield client.build_request(self.parse, market["symbol"], market["id"])

    def parse(self, response: Response) -> Generator[Union[Request, Item], None, None]:
        exchange_name = response.meta["exchange_name"]
        market_id = response.meta["market_id"]
        if response := self._get_json_response(response, exchange_name):
            last_trade_client = self.last_trade_manager.get_client(exchange_name)
            yield from last_trade_client.parse(response, market_id)
