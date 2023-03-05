from abc import ABC

from scrapy import Spider
from sqlalchemy import create_engine, select

from database.models import Exchange
from interfaces import SessionSettings
from utils.database import mysql_connection_url


class BaseSessionSpider(Spider, ABC):
    name = "base_session_spider"
    custom_settings = {}
    session_settings: SessionSettings

    def __init__(self, session_id: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.init_session_settings(session_id)

    def init_session_settings(self, raw_session_id: str) -> None:
        self.session_settings = SessionSettings.from_db(raw_session_id)
        with create_engine(mysql_connection_url()).connect() as connection:
            for exchange in connection.execute(
                select(Exchange.id, Exchange.name).where(
                    Exchange.is_active == True
                )
            ):
                self.session_settings.exchanges[exchange[1]] = exchange[0]
        self.logger.info("Spider session_settings successfully initialized")
