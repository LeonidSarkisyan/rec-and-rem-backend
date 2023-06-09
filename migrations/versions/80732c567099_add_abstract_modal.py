"""Add Abstract Modal

Revision ID: 80732c567099
Revises: 82472051f99b
Create Date: 2023-06-02 23:50:59.022368

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '80732c567099'
down_revision = '82472051f99b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('abstracts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=30), nullable=False),
    sa.Column('description', sa.String(length=150), nullable=False),
    sa.Column('content', sa.String(), nullable=True),
    sa.Column('datetime_created', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('datetime_updated', sa.DateTime(), nullable=False),
    sa.Column('is_open', sa.Boolean(), nullable=False),
    sa.Column('open_url', sa.String(), nullable=True),
    sa.Column('folder_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['folder_id'], ['folders.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('abstracts')
    # ### end Alembic commands ###
