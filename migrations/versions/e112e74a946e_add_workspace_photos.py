"""Add workspace photos

Revision ID: e112e74a946e
Revises: fe141384f5b5
Create Date: 2023-09-20 13:01:49.852210

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e112e74a946e'
down_revision = 'fe141384f5b5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('workspaces_avatars',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('high_photo_url', sa.String(), nullable=True),
    sa.Column('low_photo_url', sa.String(), nullable=True),
    sa.Column('workspace_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['workspace_id'], ['workspaces.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('high_photo_url'),
    sa.UniqueConstraint('low_photo_url'),
    sa.UniqueConstraint('workspace_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('workspaces_avatars')
    # ### end Alembic commands ###
