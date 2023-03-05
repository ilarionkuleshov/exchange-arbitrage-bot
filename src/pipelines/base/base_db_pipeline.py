import logging
from abc import ABC, abstractmethod

from scrapy import Spider, Item, signals
from scrapy.crawler import Crawler
from scrapy.exceptions import DontCloseSpider

from twisted.python.failure import Failure
from twisted.enterprise.adbapi import ConnectionPool

from utils.database import open_db_connection_pool


class BaseDBPipeline(ABC):
    db_connection_pool: ConnectionPool

    def __init__(self) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.pending_items = 0

    @classmethod
    def from_crawler(cls, crawler: Crawler) -> "BaseDBPipeline":
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

    @abstractmethod
    def process_item(self, item: Item, spider: Spider) -> Item:
        pass

    def item_stored(self, _) -> None:
        self.pending_items -= 1

    def errback(self, failure: Failure) -> None:
        self.logger.error(failure.getErrorMessage())
