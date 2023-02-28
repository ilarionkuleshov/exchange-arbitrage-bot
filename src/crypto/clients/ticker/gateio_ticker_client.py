from typing import Generator, Union

from crypto.base import BaseTickerClient
from interfaces import MarketSymbol
from items import MarketItem
from utils import safe_execute


class GateioTickerClient(BaseTickerClient):
    @property
    def api_endpoint_url(self) -> str:
        return "https://api.gateio.ws/api/v4/spot/tickers"

    def parse(self, json_response: Union[dict, list]) -> Generator[MarketItem, None, None]:                
        for data in (json_response or []):
            if self._validate_market_data(data):
                yield MarketItem(
                    exchange_id=self.exchange_internal_id,
                    symbol=MarketSymbol.from_str(data["currency_pair"], "_").to_str(),
                    price=float(data["last"]),
                    quote_volume_24h=float(data["quote_volume"])
                )

    def _validate_market_data(self, data: dict) -> bool:
        currencies = (data.get("currency_pair") or "").split("_")
        price = safe_execute(float, data.get("last"), default_value=0.0)
        quote_volume = safe_execute(float, data.get("quote_volume"), default_value=0.0)
        base_volume = safe_execute(float, data.get("base_volume"), default_value=0.0)
        return len(currencies) == 2 and price > 0 and quote_volume > 0 and base_volume > 0
