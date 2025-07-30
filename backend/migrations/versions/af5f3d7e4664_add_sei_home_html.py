"""add sei_home_html field"""

revision = 'af5f3d7e4664'
down_revision = '01bedea2b1bb'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('user', sa.Column('sei_home_html', sa.Text(), nullable=True))


def downgrade():
    op.drop_column('user', 'sei_home_html')
