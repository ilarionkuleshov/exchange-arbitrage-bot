from crypto.base import BaseUrlBuilderClient
from interfaces import MarketSymbol


class KrakenUrlBuilderClient(BaseUrlBuilderClient):
    def build_spot_url(self, symbol: MarketSymbol) -> str:
        return (
            f"https://pro.kraken.com/app/trade/{symbol.base_currency.lower()}-"
            f"{symbol.quote_currency.lower()}"
        )

    def build_deposit_url(self, currency: str) -> str:
        return f"https://pro.kraken.com/app/portfolio/spot?dialog=funding/deposit/{currency.upper()}"

    def build_withdrawal_url(self, currency: str) -> str:
        return f"https://pro.kraken.com/app/portfolio/spot?dialog=funding/withdrawal/{currency.upper()}"
