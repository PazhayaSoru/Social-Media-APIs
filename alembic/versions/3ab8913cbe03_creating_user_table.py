"""creating user table

Revision ID: 3ab8913cbe03
Revises: d390ac1d9632
Create Date: 2025-02-04 00:00:04.321516

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3ab8913cbe03'
down_revision: Union[str, None] = 'd390ac1d9632'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("users", sa.Column("id",sa.Integer,nullable=False,primary_key=True),
                    sa.Column("username",sa.String,nullable=False,unique=True),
                    sa.Column("email",sa.String,nullable=False,unique=True),
                    sa.Column("password",sa.String,nullable=False),
                    sa.Column("created_at",sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text("NOW()")))


def downgrade() -> None:
    op.drop_table("users")
