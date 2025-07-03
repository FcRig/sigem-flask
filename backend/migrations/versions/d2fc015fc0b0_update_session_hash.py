"""drop password columns add hashed session"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'd2fc015fc0b0'
down_revision = '1b2e7c4e5b2d'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('autoprf_session_hash', sa.String(length=255), nullable=True))
        batch_op.drop_column('autoprf_session')
        batch_op.drop_column('senha_autoprf')
        batch_op.drop_column('senha_siscom')
        batch_op.drop_column('senha_sei')


def downgrade():
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('senha_sei', sa.String(length=120), nullable=True))
        batch_op.add_column(sa.Column('senha_siscom', sa.String(length=120), nullable=True))
        batch_op.add_column(sa.Column('senha_autoprf', sa.String(length=120), nullable=True))
        batch_op.add_column(sa.Column('autoprf_session', sa.Text(), nullable=True))
        batch_op.drop_column('autoprf_session_hash')
