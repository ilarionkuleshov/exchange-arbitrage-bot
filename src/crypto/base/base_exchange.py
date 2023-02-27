import logging

from typing import Type
from abc import ABC, abstractmethod

from .base_ticker_client import BaseTickerClient


class BaseExchange(ABC):
    ticker_client: BaseTickerClient

    def __init__(self, name: str, internal_id: int) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.name = name
        self.internal_id = internal_id
        self.ticker_client = self.ticker_client_type()(name, internal_id)

    @abstractmethod
    def ticker_client_type(self) -> Type[BaseTickerClient]:
        pass
