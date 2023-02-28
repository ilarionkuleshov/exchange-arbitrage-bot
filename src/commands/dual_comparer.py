from argparse import Namespace
from itertools import combinations
from typing import Generator, Tuple, List, Dict, Any

from MySQLdb.cursors import DictCursor
from twisted.internet.defer import Deferred

from sqlalchemy import select
from sqlalchemy.dialects.mysql import insert

from .base import DBReactorCommand
from interfaces import SessionSettings
from database.models import Market, Bundle
from utils.database import compile_stmt, stringify_stmt


class DualComparer(DBReactorCommand):
    session_settings: SessionSettings

    def execute(self, args: list, opts: Namespace) -> Deferred:
        self.session_settings = SessionSettings.from_db(self._get_raw_session_id(args))
        d = self.db_connection_pool.runInteraction(self.select_markets)
        d.addCallback(self.get_bundles_and_build_insert_stmt)
        d.addCallback(self.db_connection_pool.runQuery)
        return d

    def select_markets(self, transaction: DictCursor) -> Tuple[Dict[str, Any]]:
        stmt = select(Market.id, Market.exchange_id, Market.symbol, Market.price)
        transaction.execute(*compile_stmt(stmt))
        return transaction.fetchall()

    def get_bundles_and_build_insert_stmt(self, markets: Tuple[Dict[str, Any]]) -> str:
        exchanges_markets = {m["exchange_id"]: [] for m in markets}
        for m in markets:
            exchanges_markets[m["exchange_id"]].append(m)

        bundles = []
        for exchanges_ids in combinations(exchanges_markets, 2):
            id_1, id_2 = exchanges_ids
            for bundle in self.compare_markets(exchanges_markets[id_1], exchanges_markets[id_2]):
                bundles.append(bundle)

        self.logger.info(f"Successfully found {len(bundles)} bundles")
        stmt = insert(Bundle).values(bundles).prefix_with("IGNORE")
        return stringify_stmt(stmt)

    def compare_markets(
        self, markets_1: List[Dict[str, Any]], markets_2: List[Dict[str, Any]]
    ) -> Generator[Dict[str, Any], None, None]:
        for m1 in markets_1:
            for m2 in markets_2:
                price_difference = self._calculate_abs_price_difference(m1["price"], m2["price"])
                if (
                    m1["symbol"] == m2["symbol"]
                    and price_difference >= self.session_settings.min_price_difference
                ):
                    market_from_id, market_to_id = m1["id"], m2["id"]
                    if m1["price"] > m2["price"]:
                        market_from_id, market_to_id = market_to_id, market_from_id
                    yield {
                        "market_from_id": market_from_id,
                        "market_to_id": market_to_id,
                        "profit": price_difference
                    }

    def _calculate_abs_price_difference(self, price_1: float, price_2: float) -> float:
        return abs(price_1 - price_2) / max(price_1, price_2)

    def _get_raw_session_id(self, args: list) -> str:
        for arg in args:
            if "session_id" in arg:
                arg_parts = arg.split("=")
                if len(arg_parts) == 2 and arg_parts[1].isdigit():
                    return arg_parts[1]
        return ""
