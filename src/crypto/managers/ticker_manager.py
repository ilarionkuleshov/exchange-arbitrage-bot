from typing import Type, Dict

from crypto.base import BaseManager, BaseClient
from crypto.clients.ticker import (
    WhitebitTickerClient,
    OkxTickerClient,
    GateioTickerClient,
    BinanceTickerClient,
)


class TickerManager(BaseManager):
    @property
    def clients_types(self) -> Dict[str, Type[BaseClient]]:
        return {
            "white_bit": WhitebitTickerClient,
            "okx": OkxTickerClient,
            "gate_i_o": GateioTickerClient,
            "binance": BinanceTickerClient,
        }
