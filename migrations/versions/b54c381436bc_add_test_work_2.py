"""add test work 2

Revision ID: b54c381436bc
Revises: 210e4f9712e6
Create Date: 2023-05-28 19:01:05.775034

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b54c381436bc'
down_revision = '210e4f9712e6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('workspaces',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=30), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('is_open', sa.Boolean(), nullable=False),
    sa.Column('url_open', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('aworkspaces')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('aworkspaces',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('title', sa.VARCHAR(length=30), autoincrement=False, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('is_open', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.Column('url_open', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='aworkspaces_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='aworkspaces_pkey')
    )
    op.drop_table('workspaces')
    # ### end Alembic commands ###
