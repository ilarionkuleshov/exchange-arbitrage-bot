from dataclasses import dataclass
from typing import Dict, Any

from interfaces import MarketSymbol
from crypto.managers import UrlBuilderManager
from utils import format_exchange_name


@dataclass
class TGBundleMessage:
    exchange_from_name: str
    exchange_to_name: str
    symbol: MarketSymbol
    profit: float

    @classmethod
    def from_dict(cls, data_dict: Dict[str, Any]) -> "TGBundleMessage":
        return cls(**data_dict)

    def to_str(self, url_builder_manager: UrlBuilderManager) -> str:
        exchange_from = format_exchange_name(self.exchange_from_name)
        exchange_to = format_exchange_name(self.exchange_to_name)
        message_text = "\n".join(
            [
                f"Bundle: *{self.symbol.to_str().upper()}*",
                f"*{exchange_from} -> {exchange_to}*",
                f"Profit: *{self.profit*100:.2f}*%",
                "",
                f"*{exchange_from} exchange*",
                f"Spot url: {url_builder_manager.get_client(self.exchange_from_name).build_spot_url(self.symbol)}",
                f"Withdrawal url: {url_builder_manager.get_client(self.exchange_from_name).build_withdrawal_url(self.symbol.base_currency)}",
                "",
                f"*{exchange_to} exchange*",
                f"Spot url: {url_builder_manager.get_client(self.exchange_to_name).build_spot_url(self.symbol)}",
                f"Deposit url: {url_builder_manager.get_client(self.exchange_to_name).build_deposit_url(self.symbol.base_currency)}",
            ]
        )
        message_text = message_text.replace(".", "\.")
        message_text = message_text.replace("-", "\-")
        message_text = message_text.replace(">", "\>")
        message_text = message_text.replace("_", "\_")
        return message_text
