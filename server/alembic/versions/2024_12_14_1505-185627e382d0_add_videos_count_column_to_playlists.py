"""Add 'videos_count' column to 'playlists'

Revision ID: 185627e382d0
Revises: 5565c8b7123d
Create Date: 2024-12-14 15:05:35.095223

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "185627e382d0"
down_revision: Union[str, None] = "5565c8b7123d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("playlists", sa.Column("videos_count", sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("playlists", "videos_count")
    # ### end Alembic commands ###