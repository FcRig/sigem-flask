"""add usuario_sei column

Revision ID: 1b2e7c4e5b2d
Revises: dc56a59e0e34
Create Date: 2025-07-03 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '1b2e7c4e5b2d'
down_revision = 'dc56a59e0e34'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('usuario_sei', sa.String(length=120), nullable=True))


def downgrade():
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('usuario_sei')
