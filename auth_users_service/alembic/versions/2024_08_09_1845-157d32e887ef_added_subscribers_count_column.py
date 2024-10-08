"""Added subscribers_count column

Revision ID: 157d32e887ef
Revises: 3187f544645d
Create Date: 2024-08-09 18:45:31.984075

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "157d32e887ef"
down_revision: Union[str, None] = "3187f544645d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("users", sa.Column("subscribers_count", sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("users", "about")
    # ### end Alembic commands ###
