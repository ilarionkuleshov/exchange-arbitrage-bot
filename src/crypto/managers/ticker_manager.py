from typing import Type, Dict

from crypto.base import BaseManager, BaseClient
from crypto.clients.ticker import (
    WhitebitTickerClient,
    OkxTickerClient,
    GateioTickerClient,
    BinanceTickerClient,
    KrakenTickerClient,
    KucoinTickerClient,
    HuobiTickerClient,
)


class TickerManager(BaseManager):
    @property
    def clients_types(self) -> Dict[str, Type[BaseClient]]:
        return {
            "white_bit": WhitebitTickerClient,
            "okx": OkxTickerClient,
            "gate_i_o": GateioTickerClient,
            "binance": BinanceTickerClient,
            "kraken": KrakenTickerClient,
            "ku_coin": KucoinTickerClient,
            "huobi": HuobiTickerClient,
        }
