"""create couples table

Revision ID: b2e02948a817
Revises: 68c97e3857bb
Create Date: 2023-12-19 12:36:45.913495

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b2e02948a817'
down_revision: Union[str, None] = '68c97e3857bb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('couples',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('female_id', sa.BigInteger(), nullable=True),
    sa.Column('male_id', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['male_id'], ['athletes.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_unique_constraint(None, 'athletes', ['id'])
    op.create_unique_constraint(None, 'coaches', ['id'])
    op.create_unique_constraint(None, 'judges', ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'judges', type_='unique')
    op.drop_constraint(None, 'coaches', type_='unique')
    op.drop_constraint(None, 'athletes', type_='unique')
    op.drop_table('couples')
    # ### end Alembic commands ###
