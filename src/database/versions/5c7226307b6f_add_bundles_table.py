"""add bundles table

Revision ID: 5c7226307b6f
Revises: 816095287de2
Create Date: 2023-02-26 12:37:04.797620

"""
from alembic import op

from sqlalchemy import Column, text
from sqlalchemy.dialects.mysql import BIGINT, FLOAT, TEXT, SMALLINT, TIMESTAMP


# revision identifiers, used by Alembic.
revision = '5c7226307b6f'
down_revision = '816095287de2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "bundles",
        Column("id", BIGINT(unsigned=True), primary_key=True, autoincrement=True),
        Column("market_from_id", BIGINT(unsigned=True), nullable=False),
        Column("market_to_id", BIGINT(unsigned=True), nullable=False),
        Column("profit", FLOAT(), nullable=False),
        Column("exception", TEXT(), nullable=True, default=None),
        Column(
            "status",
            SMALLINT(unsigned=True),
            index=True,
            nullable=False,
            server_default=text("0")
        ),
        Column(
            "created_at",
            TIMESTAMP(),
            nullable=False,
            index=True,
            server_default=text("CURRENT_TIMESTAMP")
        ),
        Column(
            "updated_at",
            TIMESTAMP(),
            nullable=False,
            index=True,
            server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
            server_onupdate=text("CURRENT_TIMESTAMP")
        )
    )
    op.create_index(
        op.f("uq_bundles_market_from_id_market_to_id"),
        "bundles",
        ["market_from_id", "market_to_id"],
        unique=True
    )


def downgrade() -> None:
    op.drop_index(
        op.f("uq_bundles_market_from_id_market_to_id"),
        "bundles"
    )
    op.drop_table("bundles")
