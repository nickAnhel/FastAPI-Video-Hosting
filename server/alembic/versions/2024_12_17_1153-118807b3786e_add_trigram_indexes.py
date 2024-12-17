"""Add trigram indexes

Revision ID: 118807b3786e
Revises: ee6fa46bdc06
Create Date: 2024-12-17 11:53:24.187380

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '118807b3786e'
down_revision: Union[str, None] = 'ee6fa46bdc06'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm;")
    op.execute("SET pg_trgm.similarity_threshold = 0.15;")

    op.create_index(
        "users_username_trgm_idx",
        "users",
        ["username"],
        postgresql_using="gin",
        postgresql_ops={"username": "gin_trgm_ops"},
    )
    op.create_index(
        "users_about_trgm_idx",
        "users",
        ["about"],
        postgresql_using="gin",
        postgresql_ops={"about": "gin_trgm_ops"},
    )

    op.create_index(
        "videos_title_trgm_idx",
        "videos",
        ["title"],
        postgresql_using="gin",
        postgresql_ops={"title": "gin_trgm_ops"},
    )
    op.create_index(
        "videos_description_trgm_idx",
        "videos",
        ["description"],
        postgresql_using="gin",
        postgresql_ops={"description": "gin_trgm_ops"},
    )

    op.create_index(
        "playlists_title_trgm_idx",
        "playlists",
        ["title"],
        postgresql_using="gin",
        postgresql_ops={"title": "gin_trgm_ops"},
    )
    op.create_index(
        "playlists_description_trgm_idx",
        "playlists",
        ["description"],
        postgresql_using="gin",
        postgresql_ops={"description": "gin_trgm_ops"},
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index("users_username_trgm_idx", table_name="users")
    op.drop_index("users_about_trgm_idx", table_name="users")

    op.drop_index("videos_title_trgm_idx", table_name="videos")
    op.drop_index("videos_description_trgm_idx", table_name="videos")

    op.drop_index("playlists_title_trgm_idx", table_name="playlists")
    op.drop_index("playlists_description_trgm_idx", table_name="playlists")
    # ### end Alembic commands ###
