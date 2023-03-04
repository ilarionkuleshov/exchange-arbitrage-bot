from crypto.base import BaseUrlBuilderClient
from interfaces import MarketSymbol


class KucoinUrlBuilderClient(BaseUrlBuilderClient):
    def build_spot_url(self, symbol: MarketSymbol) -> str:
        return (
            f"https://www.kucoin.com/trade/{symbol.base_currency.upper()}-"
            f"{symbol.quote_currency.upper()}"
        )

    def build_deposit_url(self, currency: str) -> str:
        return f"https://www.kucoin.com/assets/coin/{currency.upper()}"

    def build_withdrawal_url(self, currency: str) -> str:
        return f"https://www.kucoin.com/assets/withdraw/{currency.upper()}"
