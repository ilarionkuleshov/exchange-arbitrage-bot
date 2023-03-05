from argparse import Namespace
from typing import Tuple, Dict

from MySQLdb.cursors import DictCursor
from twisted.internet.defer import Deferred

from sqlalchemy import delete, select

from .base import DBReactorCommand
from database.models import Bundle, Market
from utils.status_codes import BundleStatusCodes
from utils.database import compile_stmt, stringify_stmt


class DBCleaner(DBReactorCommand):
    def execute(self, args: list, opts: Namespace) -> Deferred:
        d = self.db_connection_pool.runInteraction(self.delete_bundles)
        d.addCallback(self.build_delete_markets_stmt)
        d.addCallback(self.db_connection_pool.runQuery)
        d.addCallback(self.on_success_clean)
        return d

    def delete_bundles(self, transaction: DictCursor) -> Tuple[Dict[str, int]]:
        delete_stmt = delete(Bundle).where(Bundle.status != BundleStatusCodes.BANNED.value)
        transaction.execute(*compile_stmt(delete_stmt))
        select_markets_ids_stmt = select(Bundle.market_from_id, Bundle.market_to_id)
        transaction.execute(*compile_stmt(select_markets_ids_stmt))
        return transaction.fetchall()

    def build_delete_markets_stmt(self, markets_ids: Tuple[Dict[str, int]]) -> str:
        not_delete_ids = [m_id for ids in markets_ids for m_id in ids.values()]
        stmt = delete(Market).where(Market.id.notin_(not_delete_ids))
        return stringify_stmt(stmt)

    def on_success_clean(self, _) -> None:
        self.logger.info("Successfully clean DB")
