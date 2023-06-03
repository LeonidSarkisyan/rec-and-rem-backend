"""Add Abstract Desc nullable

Revision ID: 5edba1075e82
Revises: 80732c567099
Create Date: 2023-06-03 00:07:49.007164

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5edba1075e82'
down_revision = '80732c567099'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('abstracts', 'description',
               existing_type=sa.VARCHAR(length=150),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('abstracts', 'description',
               existing_type=sa.VARCHAR(length=150),
               nullable=False)
    # ### end Alembic commands ###
