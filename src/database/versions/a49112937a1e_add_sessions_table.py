"""add sessions table

Revision ID: a49112937a1e
Revises: 4cc0533f4c31
Create Date: 2023-02-26 12:21:59.158862

"""
from alembic import op

from sqlalchemy import Column, text
from sqlalchemy.dialects.mysql import TEXT, BIGINT, SMALLINT, TIMESTAMP


# revision identifiers, used by Alembic.
revision = 'a49112937a1e'
down_revision = '4cc0533f4c31'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "sessions",
        Column("id", BIGINT(unsigned=True), primary_key=True, autoincrement=True),
        Column("settings", TEXT(), nullable=False),
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


def downgrade() -> None:
    op.drop_table("sessions")
