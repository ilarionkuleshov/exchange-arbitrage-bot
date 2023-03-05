from sqlalchemy import Column, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.mysql import BIGINT, VARCHAR, FLOAT

from .base import Base
from .mixins import PrimaryKeyMixin, StatusMixin


class Market(Base, PrimaryKeyMixin, StatusMixin):
    __tablename__ = "markets"

    exchange_id = Column(
        "exchange_id", BIGINT(unsigned=True), ForeignKey("exchanges.id"), nullable=False
    )
    symbol = Column("symbol", VARCHAR(25), nullable=False)
    price = Column("price", FLOAT(), nullable=False)
    quote_volume_24h = Column("quote_volume_24h", FLOAT(), nullable=True, default=None)

    __table_args__ = (
        UniqueConstraint(exchange_id, symbol),
        {"mysql_engine": "InnoDB", "mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_unicode_ci"}
    )
