"""add profiles

Revision ID: 00eb44133a8c
Revises: d8abb2547819
Create Date: 2023-05-28 00:13:37.394619

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '00eb44133a8c'
down_revision = 'd8abb2547819'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('profiles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=30), nullable=True),
    sa.Column('second_name', sa.String(length=30), nullable=True),
    sa.Column('username', sa.String(length=30), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_index(op.f('ix_profiles_first_name'), 'profiles', ['first_name'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_profiles_first_name'), table_name='profiles')
    op.drop_table('profiles')
    # ### end Alembic commands ###
