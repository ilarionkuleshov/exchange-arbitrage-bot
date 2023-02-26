from sqlalchemy import Column
from sqlalchemy.dialects.mysql import BIGINT


class PrimaryKeyMixin:
    id = Column("id", BIGINT(unsigned=True), primary_key=True, autoincrement=True)
