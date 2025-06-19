"""add cpf and auth credentials

Revision ID: 4f67b9f9475c
Revises: 9c77cf571a1d
Create Date: 2025-07-01 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '4f67b9f9475c'
down_revision = '9c77cf571a1d'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('user', sa.Column('cpf', sa.String(length=14), nullable=True))
    op.add_column('user', sa.Column('senha_autoprf', sa.String(length=120), nullable=True))
    op.add_column('user', sa.Column('token_autoprf', sa.String(length=120), nullable=True))
    op.add_column('user', sa.Column('senha_siscom', sa.String(length=120), nullable=True))
    op.add_column('user', sa.Column('senha_sei', sa.String(length=120), nullable=True))
    op.add_column('user', sa.Column('token_sei', sa.String(length=120), nullable=True))


def downgrade():
    op.drop_column('user', 'token_sei')
    op.drop_column('user', 'senha_sei')
    op.drop_column('user', 'senha_siscom')
    op.drop_column('user', 'token_autoprf')
    op.drop_column('user', 'senha_autoprf')
    op.drop_column('user', 'cpf')
