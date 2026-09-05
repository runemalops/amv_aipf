"""add interest icon column

Revision ID: 2dfd25a919c0
Revises: 06dfea022e0b
Create Date: 2026-08-30 22:46:15.410277

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2dfd25a919c0'
down_revision = '06dfea022e0b'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('interest', schema=None) as batch_op:
        batch_op.add_column(sa.Column('icon', sa.String(length=50), nullable=True))


def downgrade():
    with op.batch_alter_table('interest', schema=None) as batch_op:
        batch_op.drop_column('icon')
