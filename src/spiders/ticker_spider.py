import json
from typing import Generator, Union

from scrapy import Spider, Request, Item
from scrapy.http import Response

from sqlalchemy import create_engine, select

from pipelines import TickerDBPipeline, MarketFilterPipeline
from crypto.managers import TickerManager
from database.models import Session, Exchange
from interfaces import SessionSettings
from utils import get_import_full_name, safe_execute
from utils.database import mysql_connection_url


class TickerSpider(Spider):
    name = "ticker_spider"
    custom_settings = {
        "ITEM_PIPELINES": {
            get_import_full_name(MarketFilterPipeline): 299,
            get_import_full_name(TickerDBPipeline): 300
        }
    }
    session_settings: SessionSettings
    ticker_manager: TickerManager

    def __init__(self, session_id: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.init_session_settings(session_id)
        self.ticker_manager = TickerManager(self.session_settings)

    def init_session_settings(self, raw_session_id: str) -> None:
        session_id = safe_execute(int, raw_session_id)
        if session_id is None:
            raise Exception("Invalid session_id was passed")

        with create_engine(mysql_connection_url()).connect() as connection:
            raw_session_settings = connection.execute(
                select(Session.settings).where(Session.id == session_id)
            )
            raw_session_settings = list(raw_session_settings)
            if len(raw_session_settings) != 1 or len(raw_session_settings[0]) != 1:
                raise Exception(
                    f"Session with id = {session_id} does not exist in the database"
                )
            session_settings = safe_execute(json.loads, raw_session_settings[0][0])
            if session_settings is None:
                raise Exception(
                    f"Invalid settings specified for the session (id = {session_id})"
                )
            self.session_settings = SessionSettings(session_id, **session_settings)
            for exchange in connection.execute(
                select(Exchange.id, Exchange.name).where(
                    Exchange.is_active == True
                )
            ):
                self.session_settings.exchanges[exchange[1]] = exchange[0]
        self.logger.info("Spider session_settings successfully initialized")

    def start_requests(self) -> Generator[Request, None, None]:
        for client in self.ticker_manager.iterate():
            yield client.build_request(self.parse)

    def parse(self, response: Response) -> Generator[Union[Request, Item], None, None]:
        exchange_name = response.meta["exchange_name"]
        json_response = safe_execute(json.loads, response.text)
        if type(json_response) not in [dict, list]:
            self.logger.error(
                f"Recieve empty response from "
                f"{response.meta['exchange_name']} ticker client"
            )
            return
        yield from self.ticker_manager.get_client(exchange_name).parse(json_response)
