import logging
from argparse import Namespace
from abc import ABC, abstractmethod

from twisted.internet import reactor
from twisted.internet.defer import Deferred
from twisted.python.failure import Failure
from twisted.enterprise.adbapi import ConnectionPool

from scrapy.commands import ScrapyCommand
from scrapy.utils.project import get_project_settings

from utils.database import open_db_connection_pool


class DBReactorCommand(ScrapyCommand, ABC):
    db_connection_pool: ConnectionPool

    def __init__(self) -> None:
        super().__init__()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.project_settings = get_project_settings()
        self.db_connection_pool = open_db_connection_pool()

    def execute(self, args: list, opts: Namespace) -> Deferred:
        raise NotImplementedError()

    def __execute(self, args: list, opts: Namespace) -> Deferred:
        d = self.execute(args, opts)
        d.addErrback(self.errback)
        d.addBoth(lambda _: reactor.stop())
        return d

    def errback(self, failure: Failure) -> None:
        self.logger.error(failure.getErrorMessage())

    def run(self, args: list, opts: Namespace) -> None:
        reactor.callFromThread(self.__execute, args, opts)
        reactor.run()

    def _get_raw_session_id(self, args: list) -> str:
        for arg in args:
            if "session_id" in arg:
                arg_parts = arg.split("=")
                if len(arg_parts) == 2 and arg_parts[1].isdigit():
                    return arg_parts[1]
        return ""
