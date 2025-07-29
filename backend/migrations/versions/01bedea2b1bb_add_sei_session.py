"""add sei session field"""

revision = '01bedea2b1bb'
down_revision = '5e1d08683305'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('user', sa.Column('sei_session', sa.Text(), nullable=True))


def downgrade():
    op.drop_column('user', 'sei_session')
