from crypto.base import BaseUrlBuilderClient
from interfaces import MarketSymbol


class BinanceUrlBuilderClient(BaseUrlBuilderClient):
    def build_spot_url(self, symbol: MarketSymbol) -> str:
        return (
            f"https://www.binance.com/ru-UA/trade/{symbol.base_currency.upper()}_"
            f"{symbol.quote_currency.upper()}?type=spot"
        )

    def build_deposit_url(self, currency: str) -> str:
        return f"https://www.binance.com/ru-UA/my/wallet/account/main/deposit/crypto/{currency.upper()}"

    def build_withdrawal_url(self, currency: str) -> str:
        return f"https://www.binance.com/ru-UA/my/wallet/account/main/withdrawal/crypto/{currency.upper()}"
