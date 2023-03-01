from crypto.base import BaseUrlBuilderClient
from interfaces import MarketSymbol


class OkxUrlBuilderClient(BaseUrlBuilderClient):
    def build_spot_url(self, symbol: MarketSymbol) -> str:
        return (
            f"https://www.okx.com/trade-spot/{symbol.base_currency.lower()}-"
            f"{symbol.quote_currency.lower()}"
        )

    def build_deposit_url(self, currency: str) -> str:
        return f"https://www.okx.com/ru/balance/recharge/{currency.lower()}"

    def build_withdrawal_url(self, currency: str) -> str:
        return f"https://www.okx.com/ru/balance/withdrawal/{currency.lower()}"
