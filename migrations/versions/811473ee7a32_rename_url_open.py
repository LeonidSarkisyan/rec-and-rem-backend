"""Rename url_open

Revision ID: 811473ee7a32
Revises: a397eb8cb1c9
Create Date: 2023-06-04 01:33:26.067683

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '811473ee7a32'
down_revision = 'a397eb8cb1c9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('abstracts', sa.Column('url_open', sa.String(), nullable=True))
    op.drop_column('abstracts', 'open_url')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('abstracts', sa.Column('open_url', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('abstracts', 'url_open')
    # ### end Alembic commands ###