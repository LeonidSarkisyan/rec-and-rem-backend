"""12312

Revision ID: c0dcf7c1dd68
Revises: 811473ee7a32
Create Date: 2023-06-04 16:01:19.392549

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c0dcf7c1dd68'
down_revision = '811473ee7a32'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('workspaces', 'url_open',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('workspaces', 'url_open',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###
