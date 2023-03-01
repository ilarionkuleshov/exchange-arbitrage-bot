import logging
from abc import ABC


class BaseClient(ABC):
    def __init__(self, exchange_name: str, exchange_internal_id: int) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.exchange_name = exchange_name
        self.exchange_internal_id = exchange_internal_id
