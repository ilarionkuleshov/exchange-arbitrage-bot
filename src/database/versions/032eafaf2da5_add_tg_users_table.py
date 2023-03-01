"""add tg_users table

Revision ID: 032eafaf2da5
Revises: 5c7226307b6f
Create Date: 2023-03-01 13:27:51.672349

"""
from alembic import op

from sqlalchemy import Column, text
from sqlalchemy.dialects.mysql import BIGINT, BOOLEAN


# revision identifiers, used by Alembic.
revision = '032eafaf2da5'
down_revision = '5c7226307b6f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "tg_users",
        Column("id", BIGINT(unsigned=True), primary_key=True, autoincrement=True),
        Column("chat_id", BIGINT(unsigned=True), unique=True, nullable=False),
        Column(
            "is_admin", BOOLEAN(), index=True, nullable=False, server_default=text("0")
        )
    )


def downgrade() -> None:
    op.drop_table("tg_users")
