from abc import abstractmethod

from .base_client import BaseClient
from interfaces import MarketSymbol


class BaseUrlBuilderClient(BaseClient):
    @abstractmethod
    def build_spot_url(self, symbol: MarketSymbol) -> str:
        pass

    @abstractmethod
    def build_deposit_url(self, currency: str) -> str:
        pass

    @abstractmethod
    def build_withdrawal_url(self, currency: str) -> str:
        pass
