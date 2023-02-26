from sqlalchemy import Column
from sqlalchemy.dialects.mysql import TEXT


class ExceptionMixin:
    exception = Column("exception", TEXT(), nullable=True, default=None)
