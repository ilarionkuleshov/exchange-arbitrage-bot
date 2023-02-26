"""add exchanges table

Revision ID: 4cc0533f4c31
Revises: 
Create Date: 2023-02-26 12:14:03.734378

"""
from alembic import op

from sqlalchemy import Column, text
from sqlalchemy.dialects.mysql import VARCHAR, BOOLEAN, BIGINT


# revision identifiers, used by Alembic.
revision = '4cc0533f4c31'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "exchanges",
        Column("id", BIGINT(unsigned=True), primary_key=True, autoincrement=True),
        Column("name", VARCHAR(15), unique=True, nullable=False),
        Column(
            "is_active", BOOLEAN(), index=True, nullable=False, server_default=text("1")
        )
    )


def downgrade() -> None:
    op.drop_table("exchanges")
