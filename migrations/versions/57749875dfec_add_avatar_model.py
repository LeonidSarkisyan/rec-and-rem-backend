"""Add avatar model

Revision ID: 57749875dfec
Revises: 45835577bb1a
Create Date: 2023-05-30 19:48:29.580132

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '57749875dfec'
down_revision = '45835577bb1a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('avatars',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('url', sa.String(), nullable=False),
    sa.Column('profile_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['profile_id'], ['profiles.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('profile_id'),
    sa.UniqueConstraint('url')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('avatars')
    # ### end Alembic commands ###
