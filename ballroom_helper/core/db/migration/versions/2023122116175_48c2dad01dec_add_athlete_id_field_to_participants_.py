"""add athlete_id field to participants table

Revision ID: 48c2dad01dec
Revises: 5ef95a057f41
Create Date: 2023-12-21 16:17:05.034053

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '48c2dad01dec'
down_revision: Union[str, None] = '5ef95a057f41'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('participants', sa.Column('athlete_id', sa.BigInteger(), nullable=True))
    op.drop_constraint('participants_group_id_fkey', 'participants', type_='foreignkey')
    op.create_foreign_key(None, 'participants', 'athletes', ['athlete_id'], ['id'])
    op.drop_column('participants', 'group_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('participants', sa.Column('group_id', sa.BIGINT(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'participants', type_='foreignkey')
    op.create_foreign_key('participants_group_id_fkey', 'participants', 'groups', ['group_id'], ['id'])
    op.drop_column('participants', 'athlete_id')
    # ### end Alembic commands ###
