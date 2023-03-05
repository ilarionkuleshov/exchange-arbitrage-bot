from scrapy import Spider, Item

from sqlalchemy import update
from MySQLdb.cursors import DictCursor

from .base import BaseDBPipeline
from items import LastTradeItem
from database.models import Market
from utils.database import compile_stmt


class LastTradeDBPipeline(BaseDBPipeline):
    def process_item(self, item: Item, spider: Spider) -> Item:
        if isinstance(item, LastTradeItem):
            stmt = update(Market).values(
                price=item["price"],
                status=item["status"]
            ).where(
                Market.id == item["market_id"]
            )
            d = self.db_connection_pool.runInteraction(self.update_market, stmt)
            d.addCallback(self.item_stored)
            d.addErrback(self.errback)
            self.pending_items += 1
        else:
            self.logger.warning(f"Undefined item instance ({type(item)})")
        return item

    def update_market(self, transaction: DictCursor, stmt) -> None:
        transaction.execute(*compile_stmt(stmt))
