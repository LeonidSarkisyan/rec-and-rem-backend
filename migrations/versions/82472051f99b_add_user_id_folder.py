"""Add user_id folder

Revision ID: 82472051f99b
Revises: 88b7639345f9
Create Date: 2023-06-02 13:43:48.120006

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '82472051f99b'
down_revision = '88b7639345f9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('folders', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'folders', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'folders', type_='foreignkey')
    op.drop_column('folders', 'user_id')
    # ### end Alembic commands ###
