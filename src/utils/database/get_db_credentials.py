from typing import List

from scrapy.utils.project import get_project_settings


class InvalidDBCredentials(Exception):
    def __init__(
        self, message: str = "Invalid database credentials in settings.py"
    ) -> None:
        self.message = message
        super().__init__(self.message)


def get_db_credentials() -> List[str]:
    settings = get_project_settings()
    credentials = [
        settings.get("DB_USERNAME"),
        settings.get("DB_PASSWORD"),
        settings.get("DB_HOST"),
        settings.get("DB_PORT"),
        settings.get("DB_DATABASE"),
    ]
    if not all(map(bool, credentials)):
        raise InvalidDBCredentials()
    return credentials
