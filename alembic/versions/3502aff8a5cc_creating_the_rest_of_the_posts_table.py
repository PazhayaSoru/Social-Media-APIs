"""creating the rest of the posts table

Revision ID: 3502aff8a5cc
Revises: 3ab8913cbe03
Create Date: 2025-02-04 07:14:49.733698

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3502aff8a5cc'
down_revision: Union[str, None] = '3ab8913cbe03'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts",sa.Column("content",sa.String,nullable=False))
    op.add_column("posts",sa.Column("published",sa.Boolean,server_default='True',nullable=False))
    op.add_column("posts",sa.Column("created_at",sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text('NOW()')))
    op.add_column("posts",sa.Column("user_id",sa.Integer,nullable=False))
    op.create_foreign_key("posts_users_fk",source_table="posts",referent_table="users",local_cols=['user_id'],remote_cols=['id'],ondelete='CASCADE')

def downgrade() -> None:
    op.drop_column("posts","content")
    op.drop_column("posts","published")
    op.drop_column("posts","created_at")
    op.drop_constraint('posts_users_fk','posts')
    op.drop_column("posts","user_id")

    
