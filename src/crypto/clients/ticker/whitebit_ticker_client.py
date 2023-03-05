from typing import Generator, Union, Optional

from crypto.base import BaseTickerClient
from interfaces import MarketSymbol
from items import MarketItem
from utils import safe_execute
from utils.status_codes import MarketStatusCodes


class WhitebitTickerClient(BaseTickerClient):
    @property
    def api_endpoint_url(self) -> str:
        return "https://whitebit.com/api/v4/public/ticker"

    def parse(
        self,
        primary_response: Union[dict, list],
        additional_response: Optional[Union[dict, list]] = None
    ) -> Generator[MarketItem, None, None]:
        for symbol, data in (primary_response or {}).items():
            if self._validate_market_data(data) and "_" in symbol:
                yield MarketItem(
                    exchange_id=self.exchange_internal_id,
                    symbol=MarketSymbol.from_str(symbol, "_").to_str(),
                    price=float(data["last_price"]),
                    quote_volume_24h=float(data["quote_volume"]),
                    status=MarketStatusCodes.SUCCESS.value
                )

    def _validate_market_data(self, data: dict) -> bool:
        price = safe_execute(float, data.get("last_price"), default_value=0.0)
        quote_volume = safe_execute(float, data.get("quote_volume"), default_value=0.0)
        base_volume = safe_execute(float, data.get("base_volume"), default_value=0.0)
        is_frozen = data.get("isFrozen", True)
        return price > 0 and quote_volume > 0 and base_volume > 0 and not is_frozen
