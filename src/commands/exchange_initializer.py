from argparse import Namespace

from MySQLdb.cursors import DictCursor
from twisted.internet.defer import Deferred

from sqlalchemy.dialects.mysql import insert

from .base import DBReactorCommand
from database.models import Exchange
from interfaces import SessionSettings
from crypto.managers import TickerManager
from utils.database import compile_stmt


class ExchangeInitializer(DBReactorCommand):
    def execute(self, args: list, opts: Namespace) -> Deferred:
        d = self.db_connection_pool.runInteraction(self.insert_exchanges)
        return d

    def insert_exchanges(self, transaction: DictCursor) -> None:
        exchanges = [
            {"name": exchange}
            for exchange in TickerManager(SessionSettings(0, 0.0, "", 0)).clients_types.keys()
        ]
        stmt = insert(Exchange).values(exchanges).prefix_with("IGNORE")
        transaction.execute(*compile_stmt(stmt))
        self.logger.info(f"Successfully inserted {len(exchanges)} exchanges")
