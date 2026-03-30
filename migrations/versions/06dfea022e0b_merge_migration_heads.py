"""Merge migration heads

Revision ID: 06dfea022e0b
Revises: add_settings_model, e14458c8dfcb
Create Date: 2026-03-29 17:59:27.049558

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '06dfea022e0b'
down_revision = ('add_settings_model', 'e14458c8dfcb')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
