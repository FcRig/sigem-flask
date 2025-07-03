"""remove autoprf and sei tokens

Revision ID: 07430eaa3e8b
Revises: 1b2e7c4e5b2d
Create Date: 2025-07-04 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '07430eaa3e8b'
down_revision = '1b2e7c4e5b2d'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('token_autoprf')
        batch_op.drop_column('token_sei')


def downgrade():
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('token_sei', sa.String(length=120), nullable=True))
        batch_op.add_column(sa.Column('token_autoprf', sa.String(length=120), nullable=True))
