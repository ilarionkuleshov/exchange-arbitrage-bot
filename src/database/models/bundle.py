from sqlalchemy import Column, UniqueConstraint
from sqlalchemy.dialects.mysql import BIGINT, FLOAT

from .base import Base
from .mixins import PrimaryKeyMixin, ExceptionMixin, StatusMixin, TimestampsMixin


class Bundle(Base, PrimaryKeyMixin, ExceptionMixin, StatusMixin, TimestampsMixin):
    __tablename__ = "bundles"

    market_from_id = Column("market_from_id", BIGINT(unsigned=True), nullable=False)
    market_to_id = Column("market_to_id", BIGINT(unsigned=True), nullable=False)
    profit = Column("profit", FLOAT(), nullable=False)

    __table_args__ = (
        UniqueConstraint(market_from_id, market_to_id),
        {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_unicode_ci"}
    )
