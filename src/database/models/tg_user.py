from sqlalchemy import Column, text
from sqlalchemy.dialects.mysql import BIGINT, BOOLEAN

from .base import Base
from .mixins import PrimaryKeyMixin


class TGUser(Base, PrimaryKeyMixin):
    __tablename__ = "tg_users"

    chat_id = Column("chat_id", BIGINT(unsigned=True), unique=True, nullable=False)
    is_admin = Column(
        "is_admin", BOOLEAN(), index=True, nullable=False, server_default=text("0")
    )
