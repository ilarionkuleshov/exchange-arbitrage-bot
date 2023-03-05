from scrapy import Spider, Item

from MySQLdb.cursors import DictCursor
from sqlalchemy.dialects.mysql import insert

from .base import BaseDBPipeline
from items import MarketItem
from database.models import Market
from utils.database import compile_stmt


class TickerDBPipeline(BaseDBPipeline):
    def process_item(self, item: Item, spider: Spider) -> Item:
        if isinstance(item, MarketItem):
            stmt = insert(Market).values(item).on_duplicate_key_update(
                price=item["price"],
                quote_volume_24h=item["quote_volume_24h"]
            )
            d = self.db_connection_pool.runInteraction(self.insert_market, stmt)
            d.addCallback(self.item_stored)
            d.addErrback(self.errback)
            self.pending_items += 1
        else:
            self.logger.warning(f"Undefined item instance ({type(item)})")
        return item

    def insert_market(self, transaction: DictCursor, stmt) -> None:
        transaction.execute(*compile_stmt(stmt))
