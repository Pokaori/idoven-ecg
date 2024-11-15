"""add date to ecg

Revision ID: 3f5276f51309
Revises: 7221aafb34e7
Create Date: 2024-11-10 02:37:53.099360

"""
from typing import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '3f5276f51309'
down_revision: str | None = '7221aafb34e7'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ecg', sa.Column('date', sa.Date(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('ecg', 'date')
    # ### end Alembic commands ###
