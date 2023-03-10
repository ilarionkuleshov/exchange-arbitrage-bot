"""add markets table

Revision ID: 816095287de2
Revises: a49112937a1e
Create Date: 2023-02-26 12:29:16.025226

"""
from alembic import op

from sqlalchemy import Column, ForeignKey, text
from sqlalchemy.dialects.mysql import BIGINT, VARCHAR, FLOAT, SMALLINT


# revision identifiers, used by Alembic.
revision = '816095287de2'
down_revision = 'a49112937a1e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "markets",
        Column("id", BIGINT(unsigned=True), primary_key=True, autoincrement=True),
        Column("exchange_id", BIGINT(unsigned=True), ForeignKey("exchanges.id"), nullable=False),
        Column("symbol", VARCHAR(25), nullable=False),
        Column("price", FLOAT(), nullable=True, default=None),
        Column("quote_volume_24h", FLOAT(), nullable=True, default=None),
        Column(
            "status",
            SMALLINT(unsigned=True),
            index=True,
            nullable=False,
            server_default=text("0")
        ),
    )
    op.create_index(
        op.f("uq_markets_exchange_id_symbol"),
        "markets",
        ["exchange_id", "symbol"],
        unique=True
    )


def downgrade() -> None:
    op.drop_index(
        op.f("uq_markets_exchange_id_symbol"),
        "markets"
    )
    op.drop_table("markets")
