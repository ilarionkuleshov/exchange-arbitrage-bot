from typing import Dict, Any
from dataclasses import dataclass

from interfaces import MarketSymbol
from crypto.managers import UrlBuilderManager
from utils import format_exchange_name


@dataclass
class TGBundleMessage:
    exchange_from_name: str
    exchange_to_name: str
    symbol: MarketSymbol
    profit: float

    parse_mode: str = "MarkdownV2"
    spec_chars: str = "_~`>#+-=|{}.!"

    @classmethod
    def from_dict(cls, data_dict: Dict[str, Any]) -> "TGBundleMessage":
        return cls(**data_dict)

    def to_str(self, url_builder_manager: UrlBuilderManager) -> str:
        exchange_from = format_exchange_name(self.exchange_from_name)
        exchange_to = format_exchange_name(self.exchange_to_name)
        exchange_from_client = url_builder_manager.get_client(self.exchange_from_name)
        exchange_to_client = url_builder_manager.get_client(self.exchange_to_name)
        base_currency = self.symbol.base_currency.upper()
        symbol = self.symbol.to_str().upper()
        message_text = "\n".join(
            [
                f"Bundle: *{symbol}*",
                f"*{exchange_from} -> {exchange_to}*",
                f"Profit: *{self.profit*100:.2f}*%",
                "",
                f"*{exchange_from} exchange*",
                f"[Spot url \[{symbol}\]]({exchange_from_client.build_spot_url(self.symbol)})",
                f"[Withdrawal url \[{base_currency}\]]({exchange_from_client.build_withdrawal_url(base_currency)})",
                "",
                f"*{exchange_to} exchange*",
                f"[Spot url \[{symbol}\]]({exchange_to_client.build_spot_url(self.symbol)})",
                f"[Deposit url \[{base_currency}\]]({exchange_to_client.build_deposit_url(base_currency)})",
            ]
        )
        message_text = "".join(self._format_char(ch) for ch in message_text)
        return message_text

    def _format_char(self, char):
        return f"\{char}" if char in self.spec_chars else char
