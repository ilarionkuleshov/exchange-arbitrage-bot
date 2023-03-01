from argparse import Namespace
from typing import Tuple, Dict, List

from telebot import TeleBot

from MySQLdb.cursors import DictCursor
from twisted.internet.defer import Deferred

from sqlalchemy import select, update
from sqlalchemy.orm import aliased

from .base import DBReactorCommand
from database.models import Exchange, Market, Bundle, TGUser
from interfaces import MarketSymbol, TGBundleMessage
from crypto.managers import UrlBuilderManager
from utils import TaskStatusCodes
from utils.database import compile_stmt, stringify_stmt


class TGSender(DBReactorCommand):
    tg_bot: TeleBot
    raw_session_id: str

    def init_tg(self) -> None:
        tg_bot_token = self.project_settings.get("TG_BOT_TOKEN")
        if not tg_bot_token:
            raise Exception("Failed to get TG_BOT_TOKEN from settings")
        self.tg_bot = TeleBot(tg_bot_token)

    def execute(self, args: list, opts: Namespace) -> Deferred:
        self.init_tg()
        self.raw_session_id = self._get_raw_session_id(args)

        d = self.db_connection_pool.runInteraction(self.select_bundles_users_exchanges)
        d.addCallback(self.send_messages)
        d.addCallback(self.build_update_bundles_stmt)
        d.addCallback(self.db_connection_pool.runQuery)
        return d

    def select_bundles_users_exchanges(
        self, transaction: DictCursor
    ) -> Tuple[Dict[int, TGBundleMessage], List[int], Dict[str, int]]:
        market_from_alias = aliased(Market)
        market_to_alias = aliased(Market)
        exchange_from_alias = aliased(Exchange)
        exchange_to_alias = aliased(Exchange)

        bundles_stmt = select(
            Bundle.id,
            exchange_from_alias.name.label("exchange_from_name"),
            exchange_to_alias.name.label("exchange_to_name"),
            market_from_alias.symbol, Bundle.profit
        ).where(
            Bundle.status == TaskStatusCodes.NOT_PROCESSED.value
        ).join(
            market_from_alias, Bundle.market_from_id == market_from_alias.id
        ).join(
            market_to_alias, Bundle.market_to_id == market_to_alias.id
        ).join(
            exchange_from_alias, market_from_alias.exchange_id == exchange_from_alias.id
        ).join(
            exchange_to_alias, market_to_alias.exchange_id == exchange_to_alias.id
        )

        transaction.execute(*compile_stmt(bundles_stmt))
        bundles = {
            bundle["id"]:TGBundleMessage.from_dict(
                {
                    "exchange_from_name": bundle["exchange_from_name"],
                    "exchange_to_name": bundle["exchange_to_name"],
                    "symbol": MarketSymbol.from_str(bundle["symbol"]),
                    "profit": bundle["profit"]
                }
            )
            for bundle in transaction.fetchall()
        }

        users_stmt = select(TGUser.chat_id).where(TGUser.is_admin == True)
        transaction.execute(*compile_stmt(users_stmt))
        users = [user["chat_id"] for user in transaction.fetchall()]

        exchanges_stmt = select(Exchange.id, Exchange.name).where(
            Exchange.is_active == True
        )
        transaction.execute(*compile_stmt(exchanges_stmt))
        exchanges = {exc["name"]:exc["id"] for exc in transaction.fetchall()}

        return (bundles, users, exchanges)

    def send_messages(
        self, result: Tuple[Dict[int, TGBundleMessage], List[int], Dict[str, int]]
    ) -> List[int]:
        bundles, users, exchanges = result
        url_builder_manager = UrlBuilderManager(exchanges)
        for bundle_id, bundle in bundles.items():
            message_text = bundle.to_str(url_builder_manager)
            for chat_id in users:
                self.tg_bot.send_message(
                    chat_id=chat_id,
                    text=message_text,
                    parse_mode=bundle.parse_mode,
                    disable_web_page_preview=True
                )
                self.logger.info(
                    f"Successfully sent message to user with id={chat_id}, "
                    f"bundle with id={bundle_id}"
                )
        return list(bundles.keys())

    def build_update_bundles_stmt(self, bundles_ids) -> str:
        stmt = update(Bundle).values(status=TaskStatusCodes.MESSAGE_SENT_SUCCESS.value).where(
            Bundle.id.in_(bundles_ids)
        )
        return stringify_stmt(stmt)
