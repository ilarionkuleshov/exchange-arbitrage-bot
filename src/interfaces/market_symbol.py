from dataclasses import dataclass


@dataclass
class MarketSymbol:
    base_currency: str
    quote_currency: str

    separator: str = "/"

    def __post_init__(self):
        self.base_currency = self.base_currency.lower()
        self.quote_currency = self.quote_currency.lower()

    @classmethod
    def from_str(cls, symbol_str: str) -> "MarketSymbol":
        currencies = symbol_str.split(cls.separator)
        if len(currencies) != 2:
            raise Exception(
                f"Invalid market symbol passed. Use `{cls.separator}` separator"
            )
        return cls(*currencies)

    def to_str(self) -> str:
        return self.separator.join([self.base_currency, self.quote_currency])
