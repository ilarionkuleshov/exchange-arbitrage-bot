from twisted.enterprise.adbapi import ConnectionPool
from MySQLdb.cursors import DictCursor

from .get_db_credentials import get_db_credentials


def open_db_connection_pool() -> ConnectionPool:
    user, passwd, host, port, db = get_db_credentials()
    return ConnectionPool(
        "MySQLdb",
        user=user,
        passwd=passwd,
        host=host,
        port=int(port),
        db=db,
        charset="utf8mb4",
        use_unicode=True,
        cursorclass=DictCursor,
        cp_reconnect=True,
        cp_max=1
    )
