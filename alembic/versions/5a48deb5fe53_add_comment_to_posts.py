"""add comment to posts

Revision ID: 5a48deb5fe53
Revises: e079886f45d1
Create Date: 2026-09-23 19:50:44.196030

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5a48deb5fe53'
down_revision: Union[str, Sequence[str], None] = 'e079886f45d1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
