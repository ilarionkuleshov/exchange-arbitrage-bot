from sqlalchemy import Column
from sqlalchemy.dialects.mysql import TEXT

from .base import Base
from .mixins import PrimaryKeyMixin, ExceptionMixin, StatusMixin, TimestampsMixin


class Session(Base, PrimaryKeyMixin, ExceptionMixin, StatusMixin, TimestampsMixin):
    __tablename__ = "sessions"

    settings = Column("settings", TEXT(), nullable=False)
