"""Add Settings model for SMTP configuration

Revision ID: add_settings_model
Revises: da32293e9c61
Create Date: 2026-03-23

"""

from alembic import op
import sqlalchemy as sa


revision = "add_settings_model"
down_revision = "da32293e9c61"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "settings",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("key", sa.String(length=100), nullable=False),
        sa.Column("value", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("key"),
    )


def downgrade():
    op.drop_table("settings")
