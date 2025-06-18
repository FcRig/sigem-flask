"""add administrador column to user

Revision ID: 9c77cf571a1d
Revises: 52135d4f11dc
Create Date: 2025-06-14 12:00:00.000000
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '9c77cf571a1d'
down_revision = '52135d4f11dc'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('user', sa.Column('administrador', sa.Boolean(), nullable=True, server_default=sa.false()))
    op.alter_column('user', 'administrador', server_default=None)


def downgrade():
    op.drop_column('user', 'administrador')
