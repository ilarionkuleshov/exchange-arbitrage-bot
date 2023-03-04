from typing import Generator, Union, Optional

from crypto.base import BaseTickerClient
from interfaces import MarketSymbol
from items import MarketItem
from utils import safe_execute


class KucoinTickerClient(BaseTickerClient):
    @property
    def api_endpoint_url(self) -> str:
        return "https://api.kucoin.com/api/v1/market/allTickers"

    def parse(
        self,
        primary_response: Union[dict, list],
        additional_response: Optional[Union[dict, list]] = None
    ) -> Generator[MarketItem, None, None]:
        for data in (((primary_response or {}).get("data") or {}).get("ticker") or []):
            if self._validate_market_data(data):
                yield MarketItem(
                    exchange_id=self.exchange_internal_id,
                    symbol=MarketSymbol.from_str(data["symbol"], "-").to_str(),
                    price=float(data["last"]),
                    quote_volume_24h=float(data["volValue"])
                )

    def _validate_market_data(self, data: dict) -> bool:
        currencies = (data.get("symbol") or "").split("-")
        price = safe_execute(float, data.get("last"), default_value=0.0)
        quote_volume = safe_execute(float, data.get("volValue"), default_value=0.0)
        base_volume = safe_execute(float, data.get("vol"), default_value=0.0)
        return len(currencies) == 2 and price > 0 and quote_volume > 0 and base_volume > 0
