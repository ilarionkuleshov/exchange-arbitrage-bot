from dataclasses import dataclass
from scrapy.utils.project import get_project_settings


SEPARATOR: str = get_project_settings()["MARKET_SYMBOL_SEPARATOR"]


@dataclass
class MarketSymbol:
    base_currency: str
    quote_currency: str
    separator: str = SEPARATOR

    def __init__(self, base_currency, quote_currency):
        self.base_currency = base_currency.lower()
        self.quote_currency = quote_currency.lower()

    @classmethod
    def from_str(cls, symbol_str: str, separator: str = SEPARATOR) -> "MarketSymbol":
        currencies = symbol_str.split(separator)
        if len(currencies) != 2:
            raise Exception(
                f"Invalid market symbol passed. Use `{separator}` separator"
            )
        return cls(*currencies)

    def to_str(self) -> str:
        return self.separator.join([self.base_currency, self.quote_currency])
