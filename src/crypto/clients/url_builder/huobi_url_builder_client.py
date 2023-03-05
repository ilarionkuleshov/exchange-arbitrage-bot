from crypto.base import BaseUrlBuilderClient
from interfaces import MarketSymbol


class HuobiUrlBuilderClient(BaseUrlBuilderClient):
    def build_spot_url(self, symbol: MarketSymbol) -> str:
        return (
            f"https://www.huobi.com/en-us/exchange/{symbol.base_currency.lower()}_"
            f"{symbol.quote_currency.lower()}"
        )

    def build_deposit_url(self, currency: str) -> str:
        return f"https://www.huobi.com/en-us/finance/deposit/{currency.lower()}"

    def build_withdrawal_url(self, currency: str) -> str:
        return f"https://www.huobi.com/en-us/finance/withdraw/{currency.lower()}"
