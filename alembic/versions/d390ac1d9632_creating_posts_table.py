"""creating posts table

Revision ID: d390ac1d9632
Revises: 
Create Date: 2025-02-02 18:47:14.138889

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd390ac1d9632'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("posts",sa.Column("id",sa.Integer,nullable=False,primary_key=True),
                    sa.Column("title",sa.String,nullable=False))
    


def downgrade() -> None:
    op.drop_table("posts")
