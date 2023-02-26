from .get_db_credentials import get_db_credentials


def mysql_connection_url() -> str:
    return "mysql+mysqldb://{}:{}@{}:{}/{}?charset=utf8mb4".format(
        *get_db_credentials()
    )
