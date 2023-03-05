from typing import Generator, Union, Optional, Dict

from crypto.base import BaseTickerClient
from interfaces import MarketSymbol
from items import MarketItem
from utils import safe_execute
from utils.status_codes import MarketStatusCodes


class BinanceTickerClient(BaseTickerClient):
    @property
    def api_endpoint_url(self) -> str:
        return "https://data.binance.com/api/v3/ticker/24hr"

    @property
    def additional_api_endpoint_url(self) -> Optional[str]:
        return "https://data.binance.com/api/v3/exchangeInfo"

    def parse(
        self,
        primary_response: Union[dict, list],
        additional_response: Optional[Union[dict, list]] = None
    ) -> Generator[MarketItem, None, None]:
        validated_trading_pairs = self._get_validated_trading_pairs(additional_response)
        for data in (primary_response or []):
            if (
                self._validate_market_data(data)
                and data["symbol"] in validated_trading_pairs
            ):
                yield MarketItem(
                    exchange_id=self.exchange_internal_id,
                    symbol=validated_trading_pairs[data["symbol"]],
                    price=float(data["lastPrice"]),
                    quote_volume_24h=float(data["quoteVolume"]),
                    status=MarketStatusCodes.SUCCESS.value
                )

    def _validate_market_data(self, data: dict) -> bool:
        symbol = data.get("symbol")
        price = safe_execute(float, data.get("lastPrice"), default_value=0.0)
        quote_volume = safe_execute(float, data.get("quoteVolume"), default_value=0.0)
        base_volume = safe_execute(float, data.get("volume"), default_value=0.0)
        return symbol and price > 0 and quote_volume > 0 and base_volume > 0

    def _get_validated_trading_pairs(
        self, additional_response: Union[dict, list]
    ) -> Dict[str, str]:
        validated_trading_pairs = {}
        if (
            not len(additional_response or {})
            or not len((additional_response or {}).get("symbols") or [])
        ):
            self.logger.error("Binance exchangeInfo IS EMPTY!")
        else:
            for symbol_data in ((additional_response or {}).get("symbols") or []):
                if (
                    (symbol_data.get("status") or "").lower() == "trading"
                    and symbol_data.get("isSpotTradingAllowed") == True
                ):
                    validated_trading_pairs[symbol_data["symbol"]] = MarketSymbol(
                        symbol_data["baseAsset"], symbol_data["quoteAsset"]
                    ).to_str()
        return validated_trading_pairs
