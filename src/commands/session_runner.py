import json
from argparse import Namespace

from scrapy.crawler import CrawlerRunner

from MySQLdb.cursors import DictCursor
from twisted.internet.defer import Deferred

from sqlalchemy import update
from sqlalchemy.dialects.mysql import insert

from .base import DBReactorCommand
from interfaces import SessionSettings
from database.models import Session
from utils.status_codes import SessionStatusCodes
from utils.database import compile_stmt, stringify_stmt

from spiders import TickerSpider
from commands import DBCleaner, DualComparer, TGSender


class SessionRunner(DBReactorCommand):
    session_settings: SessionSettings

    def execute(self, args: list, opts: Namespace) -> Deferred:
        d = self.db_connection_pool.runInteraction(self.insert_session)
        d.addCallback(self.db_cleaner_deferred)
        d.addCallback(self.ticker_spider_deferred)
        d.addCallback(self.dual_comparer_deferred)
        d.addCallback(self.tg_sender_deferred)
        d.addCallback(self.build_update_session_stmt)
        d.addCallback(self.db_connection_pool.runQuery)
        return d

    def insert_session(self, transaction: DictCursor) -> None:
        self.session_settings = SessionSettings(
            session_id=0,
            min_price_difference=self.project_settings["MIN_PRICE_DIFFERENCE"],
            quote_currency=self.project_settings["QUOTE_CURRENCY"],
            min_quote_volume_24h=self.project_settings["MIN_QUOTE_VOLUME_24H"]
        )
        stmt = insert(Session).values(
            settings=json.dumps(self.session_settings.to_dict(["session_id", "exchanges"])),
            status=SessionStatusCodes.IN_PROCESSING.value
        )
        transaction.execute(*compile_stmt(stmt))
        if type(transaction.lastrowid) != int:
            raise Exception("Error inserting new session")
        self.session_settings.session_id = transaction.lastrowid

    def db_cleaner_deferred(self, _) -> Deferred:
        return DBCleaner().execute([], Namespace())

    def ticker_spider_deferred(self, _) -> Deferred:
        runner = CrawlerRunner(self.project_settings)
        runner.crawl(TickerSpider, session_id=self.session_settings.session_id)
        return runner.join()

    def dual_comparer_deferred(self, _) -> Deferred:
        return DualComparer().execute(
            [f"session_id={self.session_settings.session_id}"], Namespace()
        )

    def tg_sender_deferred(self, _) -> Deferred:
        return TGSender().execute(
            [f"session_id={self.session_settings.session_id}"], Namespace()
        )

    def build_update_session_stmt(self, _) -> str:
        stmt = update(Session).values(status=SessionStatusCodes.SUCCESS.value).where(
            Session.id == self.session_settings.session_id
        )
        return stringify_stmt(stmt)
