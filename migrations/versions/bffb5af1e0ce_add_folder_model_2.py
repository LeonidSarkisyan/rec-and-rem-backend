"""Add Folder Model 2

Revision ID: bffb5af1e0ce
Revises: a2fe468fa0b2
Create Date: 2023-06-01 23:40:32.299509

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bffb5af1e0ce'
down_revision = 'a2fe468fa0b2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('folders', sa.Column('is_open', sa.Boolean(), nullable=False))
    op.add_column('folders', sa.Column('url_open', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('folders', 'url_open')
    op.drop_column('folders', 'is_open')
    # ### end Alembic commands ###