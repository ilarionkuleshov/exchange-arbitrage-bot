from sqlalchemy import Column, text
from sqlalchemy.dialects.mysql import VARCHAR, BOOLEAN

from .base import Base
from .mixins import PrimaryKeyMixin


class Exchange(Base, PrimaryKeyMixin):
    __tablename__ = "exchanges"

    name = Column("name", VARCHAR(15), unique=True, nullable=False)
    is_active = Column(
        "is_active", BOOLEAN(), index=True, nullable=False, server_default=text("1")
    )
