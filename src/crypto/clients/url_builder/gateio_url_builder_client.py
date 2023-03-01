from crypto.base import BaseUrlBuilderClient
from interfaces import MarketSymbol


class GateioUrlBuilderClient(BaseUrlBuilderClient):
    def build_spot_url(self, symbol: MarketSymbol) -> str:
        return (
            f"https://www.gate.io/trade/{symbol.base_currency.upper()}_"
            f"{symbol.quote_currency.upper()}"
        )

    def build_deposit_url(self, currency: str) -> str:
        return f"https://www.gate.io/ru/myaccount/deposit/{currency.upper()}"

    def build_withdrawal_url(self, currency: str) -> str:
        return f"https://www.gate.io/ru/myaccount/withdraw/{currency.upper()}"
