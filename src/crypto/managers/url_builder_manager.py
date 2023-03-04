from typing import Type, Dict

from crypto.base import BaseManager, BaseClient
from crypto.clients.url_builder import (
    WhitebitUrlBuilderClient,
    OkxUrlBuilderClient,
    GateioUrlBuilderClient,
    BinanceUrlBuilderClient,
    KrakenUrlBuilderClient,
)


class UrlBuilderManager(BaseManager):
    @property
    def clients_types(self) -> Dict[str, Type[BaseClient]]:
        return {
            "white_bit": WhitebitUrlBuilderClient,
            "okx": OkxUrlBuilderClient,
            "gate_i_o": GateioUrlBuilderClient,
            "binance": BinanceUrlBuilderClient,
            "kraken": KrakenUrlBuilderClient,
        }
