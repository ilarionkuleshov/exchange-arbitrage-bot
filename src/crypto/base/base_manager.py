import logging

from typing import Iterator, Type, Dict
from abc import ABC, abstractmethod

from .base_client import BaseClient
from interfaces import SessionSettings


class BaseManager(ABC):
    clients: Dict[str, BaseClient] = {}

    @property
    @abstractmethod
    def clients_types(self) -> Dict[str, Type[BaseClient]]:
        pass

    def __init__(self, session_settings: SessionSettings) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        for exchange_name, exchange_id in session_settings.exchanges.items():
            self.clients[exchange_name] = self.clients_types[exchange_name](
                exchange_name, exchange_id
            )

    def get_client(self, exchange_name: str) -> BaseClient:
        return self.clients[exchange_name]

    def iterate(self) -> Iterator[BaseClient]:
        return iter(self.clients.values())