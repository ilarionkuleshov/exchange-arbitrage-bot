from sqlalchemy import Column, text
from sqlalchemy.dialects.mysql import TIMESTAMP


class TimestampsMixin:
    created_at = Column(
        "created_at",
        TIMESTAMP(),
        nullable=False,
        index=True,
        server_default=text("CURRENT_TIMESTAMP")
    )
    updated_at = Column(
        "updated_at",
        TIMESTAMP(),
        nullable=False,
        index=True,
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
        server_onupdate=text("CURRENT_TIMESTAMP")
    )
