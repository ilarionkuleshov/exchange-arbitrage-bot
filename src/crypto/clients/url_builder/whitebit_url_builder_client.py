from crypto.base import BaseUrlBuilderClient
from interfaces import MarketSymbol


class WhitebitUrlBuilderClient(BaseUrlBuilderClient):
    def build_spot_url(self, symbol: MarketSymbol) -> str:
        return (
            f"https://whitebit.com/trade/{symbol.base_currency.upper()}-"
            f"{symbol.quote_currency.upper()}?type=spot&tab=open-orders"
        )

    def build_deposit_url(self, currency: str) -> str:
        return f"https://whitebit.com/ua/balance/wallet?query={currency.lower()}"

    def build_withdrawal_url(self, currency: str) -> str:
        return self.build_deposit_url(currency)
