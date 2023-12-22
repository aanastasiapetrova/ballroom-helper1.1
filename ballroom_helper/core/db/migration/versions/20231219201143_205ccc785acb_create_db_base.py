"""create db base

Revision ID: 205ccc785acb
Revises: caf0279e3f73
Create Date: 2023-12-19 20:11:43.117169

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '205ccc785acb'
down_revision: Union[str, None] = 'caf0279e3f73'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('groups',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('age_group', sa.String(length=255), nullable=False),
    sa.Column('program', sa.String(length=255), nullable=False),
    sa.Column('dances', sa.String(length=10), nullable=True),
    sa.Column('participants_amount', sa.Integer(), nullable=True),
    sa.Column('participants_limit', sa.Integer(), nullable=True),
    sa.Column('competition_part_number', sa.Integer(), nullable=True),
    sa.Column('min_age', sa.Integer(), nullable=True),
    sa.Column('max_age', sa.Integer(), nullable=True),
    sa.Column('min_class', sa.Integer(), nullable=True),
    sa.Column('max_class', sa.Integer(), nullable=True),
    sa.Column('competition_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['competition_id'], ['competitions.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('participants',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('start_number', sa.BigInteger(), nullable=True),
    sa.Column('competition_id', sa.BigInteger(), nullable=False),
    sa.Column('group_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['competition_id'], ['competitions.id'], ),
    sa.ForeignKeyConstraint(['group_id'], ['groups.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('shedules',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('group_start', sa.DateTime(), nullable=True),
    sa.Column('group_finish', sa.DateTime(), nullable=True),
    sa.Column('floor', sa.String(length=1), nullable=True),
    sa.Column('round', sa.String(length=10), nullable=True),
    sa.Column('full_amount', sa.Integer(), nullable=True),
    sa.Column('to_choose_amount', sa.Integer(), nullable=True),
    sa.Column('heats_amount', sa.Integer(), nullable=True),
    sa.Column('group_duration', sa.Integer(), nullable=True),
    sa.Column('competition_id', sa.BigInteger(), nullable=False),
    sa.Column('group_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['competition_id'], ['competitions.id'], ),
    sa.ForeignKeyConstraint(['group_id'], ['groups.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('competition_judge',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('competition_id', sa.BigInteger(), nullable=False),
    sa.Column('judge_id', sa.BigInteger(), nullable=False),
    sa.Column('role', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['competition_id'], ['competitions.id'], ),
    sa.ForeignKeyConstraint(['judge_id'], ['judges.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('group_participants',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('group_id', sa.BigInteger(), nullable=False),
    sa.Column('partcipant_id', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['group_id'], ['groups.id'], ),
    sa.ForeignKeyConstraint(['partcipant_id'], ['participants.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('marks',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('dance', sa.String(length=10), nullable=True),
    sa.Column('heat_number', sa.Integer(), nullable=True),
    sa.Column('participant_start_number', sa.Integer(), nullable=True),
    sa.Column('mark', sa.Integer(), nullable=True),
    sa.Column('group_id', sa.BigInteger(), nullable=False),
    sa.Column('partcipant_id', sa.BigInteger(), nullable=False),
    sa.Column('shedule_id', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['group_id'], ['groups.id'], ),
    sa.ForeignKeyConstraint(['partcipant_id'], ['participants.id'], ),
    sa.ForeignKeyConstraint(['shedule_id'], ['shedules.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('shedule_judges',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('judge_abbreviation', sa.String(length=4), nullable=True),
    sa.Column('competition_id', sa.BigInteger(), nullable=False),
    sa.Column('group_id', sa.BigInteger(), nullable=False),
    sa.Column('judge_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['competition_id'], ['competitions.id'], ),
    sa.ForeignKeyConstraint(['group_id'], ['groups.id'], ),
    sa.ForeignKeyConstraint(['judge_id'], ['judges.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_unique_constraint(None, 'athlet_coach', ['id'])
    op.create_unique_constraint(None, 'competitions', ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'competitions', type_='unique')
    op.drop_constraint(None, 'athlet_coach', type_='unique')
    op.drop_table('shedule_judges')
    op.drop_table('marks')
    op.drop_table('group_participants')
    op.drop_table('competition_judge')
    op.drop_table('shedules')
    op.drop_table('participants')
    op.drop_table('groups')
    # ### end Alembic commands ###
