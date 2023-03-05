from typing import Generator, Union, Optional, Dict

from crypto.base import BaseTickerClient
from interfaces import MarketSymbol
from items import MarketItem
from utils import safe_execute
from utils.status_codes import MarketStatusCodes


class HuobiTickerClient(BaseTickerClient):
    @property
    def api_endpoint_url(self) -> str:
        return "https://api.huobi.pro/market/tickers"

    @property
    def additional_api_endpoint_url(self) -> Optional[str]:
        return "https://api.huobi.pro/v2/settings/common/symbols"

    def parse(
        self,
        primary_response: Union[dict, list],
        additional_response: Optional[Union[dict, list]] = None
    ) -> Generator[MarketItem, None, None]:
        validated_trading_pairs = self._get_validated_trading_pairs(additional_response)
        for data in ((primary_response or {}).get("data") or []):
            if (
                self._validate_market_data(data)
                and data["symbol"] in validated_trading_pairs
            ):
                yield MarketItem(
                    exchange_id=self.exchange_internal_id,
                    symbol=validated_trading_pairs[data["symbol"]],
                    price=None,
                    quote_volume_24h=data["vol"],
                    status=MarketStatusCodes.PRICE_NOT_DEFINED.value
                )

    def _validate_market_data(self, data: dict) -> bool:
        quote_volume = safe_execute(float, data.get("vol"), default_value=0.0)
        base_volume = safe_execute(float, data.get("amount"), default_value=0.0)
        return quote_volume > 0 and base_volume > 0

    def _get_validated_trading_pairs(
        self, additional_response: Union[dict, list]
    ) -> Dict[str, str]:
        validated_trading_pairs = {}
        if (
            not len(additional_response or {})
            or not len((additional_response or {}).get("data") or [])
        ):
            self.logger.error("Huobi common/symbols IS EMPTY!")
        else:
            for symbol_data in ((additional_response or {}).get("data") or []):
                if (symbol_data.get("state") or "").lower() == "online":
                    validated_trading_pairs[symbol_data["sc"]] = MarketSymbol(
                        symbol_data["bcdn"], symbol_data["qcdn"]
                    ).to_str()
        return validated_trading_pairs
