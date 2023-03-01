import logging

from scrapy import Spider, Item, signals
from scrapy.crawler import Crawler
from scrapy.exceptions import DontCloseSpider

from twisted.python.failure import Failure
from twisted.enterprise.adbapi import ConnectionPool

from MySQLdb.cursors import DictCursor
from sqlalchemy.dialects.mysql import insert

from items import MarketItem
from database.models import Market
from utils.database import open_db_connection_pool, compile_stmt


class TickerDBPipeline:
    db_connection_pool: ConnectionPool

    def __init__(self) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.pending_items = 0

    @classmethod
    def from_crawler(cls, crawler: Crawler) -> "TickerDBPipeline":
        o = cls()
        crawler.signals.connect(o.spider_idle, signal=signals.spider_idle)
        return o

    def open_spider(self, spider: Spider) -> None:
        self.db_connection_pool = open_db_connection_pool()

    def close_spider(self, spider: Spider) -> None:
        self.db_connection_pool.close()

    def spider_idle(self, spider: Spider) -> None:
        if self.pending_items > 0:
            raise DontCloseSpider

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

    def item_stored(self, _) -> None:
        self.pending_items -= 1

    def errback(self, failure: Failure) -> None:
        self.logger.error(failure.getErrorMessage())
