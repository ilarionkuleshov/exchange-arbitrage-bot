import logging

from typing import Type
from abc import ABC, abstractmethod

from .base_ticker_client import BaseTickerClient


class BaseExchange(ABC):
    internal_id: int
    ticker_client: BaseTickerClient

    def __init__(self, internal_id) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.internal_id = internal_id
        self.ticker_client = self.get_ticker_client()(self.name, internal_id)

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def get_ticker_client(self) -> Type[BaseTickerClient]:
        pass
