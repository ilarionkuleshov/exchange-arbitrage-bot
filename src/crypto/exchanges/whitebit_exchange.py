from typing import Type

from crypto.base import BaseExchange, BaseTickerClient
from crypto.clients.ticker import WhitebitTickerClient


class WhitebitExchange(BaseExchange):
    def ticker_client_type(self) -> Type[BaseTickerClient]:
        return WhitebitTickerClient
