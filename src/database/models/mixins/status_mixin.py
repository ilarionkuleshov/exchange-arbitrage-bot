from sqlalchemy import Column, text
from sqlalchemy.dialects.mysql import SMALLINT


class StatusMixin:
    status = Column(
        "status",
        SMALLINT(unsigned=True),
        index=True,
        nullable=False,
        server_default=text("0")
    )
