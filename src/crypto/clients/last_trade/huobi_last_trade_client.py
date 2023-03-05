from typing import Union, Generator

from crypto.base import BaseLastTradeClient
from items import LastTradeItem
from interfaces import MarketSymbol
from utils.status_codes import MarketStatusCodes


class HuobiLastTradeClient(BaseLastTradeClient):
    def build_api_endpoint_url(self, symbol: MarketSymbol) -> str:
        formatted_symbol = f"{symbol.base_currency}{symbol.quote_currency}".lower()
        return f"https://api.huobi.pro/market/trade?symbol={formatted_symbol}"

    def parse(
        self, response: Union[dict, list], market_id: int
    ) -> Generator[LastTradeItem, None, None]:
        data = (((response or {}).get("tick") or {}).get("data") or [{}])[0]
        if data.get("price"):
            yield LastTradeItem(
                market_id=market_id,
                price=data["price"],
                status=MarketStatusCodes.SUCCESS.value
            )
        else:
            yield LastTradeItem(
                market_id=market_id,
                price=0.0,
                status=MarketStatusCodes.ERROR.value
            )
