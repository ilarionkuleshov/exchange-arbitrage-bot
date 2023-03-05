from typing import Type, Dict

from crypto.base import BaseManager, BaseClient
from crypto.clients.last_trade import (
    HuobiLastTradeClient,
)


class LastTradeManager(BaseManager):
    @property
    def clients_types(self) -> Dict[str, Type[BaseClient]]:
        return {
            "huobi": HuobiLastTradeClient,
        }
