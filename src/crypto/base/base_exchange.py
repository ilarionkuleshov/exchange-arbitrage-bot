import logging

from typing import Type
from abc import ABC, abstractmethod

from .base_ticker_client import BaseTickerClient


class BaseExchange(ABC):
    ticker_client: BaseTickerClient

    def __init__(self) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.ticker_client = self.get_ticker_client()(self.name)

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def get_ticker_client(self) -> Type[BaseTickerClient]:
        pass
