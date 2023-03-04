from typing import Generator, Union, Optional, Dict

from crypto.base import BaseTickerClient
from interfaces import MarketSymbol
from items import MarketItem
from utils import safe_execute


class KrakenTickerClient(BaseTickerClient):
    @property
    def api_endpoint_url(self) -> str:
        return "https://api.kraken.com/0/public/Ticker"

    @property
    def additional_api_endpoint_url(self) -> Optional[str]:
        return "https://api.kraken.com/0/public/AssetPairs"

    def parse(
        self,
        primary_response: Union[dict, list],
        additional_response: Optional[Union[dict, list]] = None
    ) -> Generator[MarketItem, None, None]:
        validated_trading_pairs = self._get_validated_trading_pairs(additional_response)
        for symbol, data in ((primary_response or {}).get("result") or {}).items():
            if (
                self._validate_market_data(data)
                and symbol in validated_trading_pairs
            ):
                yield MarketItem(
                    exchange_id=self.exchange_internal_id,
                    symbol=validated_trading_pairs[symbol],
                    price=float(data["c"][0]),
                    quote_volume_24h=self._calculate_quote_volume(
                        float(data["v"][1]), float(data["c"][0])
                    )
                )

    def _validate_market_data(self, data: dict) -> bool:
        price = safe_execute(float, (data.get("c") or [0.0])[0], default_value=0.0)
        base_volume = safe_execute(float, (data.get("v") or [0.0, 0.0])[1], default_value=0.0)
        quote_volume = self._calculate_quote_volume(base_volume, price)
        return price > 0 and quote_volume > 0 and base_volume > 0

    def _calculate_quote_volume(self, base_volume: float, price: float) -> float:
        return base_volume * price

    def _get_validated_trading_pairs(
        self, additional_response: Union[dict, list]
    ) -> Dict[str, str]:
        validated_trading_pairs = {}
        if (
            not len(additional_response or {})
            or not len((additional_response or {}).get("result") or {})
        ):
            self.logger.error("Kraken AssetPairs IS EMPTY!")
        else:
            for symbol, data in ((additional_response or {}).get("result") or {}).items():
                if (data.get("status") or "").lower() == "online":
                    validated_trading_pairs[symbol] = MarketSymbol(
                        data["base"], data["quote"]
                    ).to_str()
        return validated_trading_pairs
