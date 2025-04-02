"""Add content and image_url to Challenge model

Revision ID: your_revision_id_here  <-- This will be a unique ID
Revises: ddfb44df83d8             <-- This should be the previous revision
Create Date: 2025-03-30 ...

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6f08f452b14f'  
down_revision: Union[str, None] = 'ddfb44df83d8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('challenges', sa.Column('content', sa.Text(), nullable=True))
    op.add_column('challenges', sa.Column('image_url', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column('challenges', 'image_url')
    op.drop_column('challenges', 'content')