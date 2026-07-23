"""create spotify_connection table

Revision ID: 20260722_0001
Revises: 20260718_0002
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID

revision: str = "20260722_0001"
down_revision: str | None = "20260718_0002"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "spotify_connections",
        sa.Column(
            "id",
            UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column(
            "user_id", sa.String(length=255), unique=True, nullable=False, index=True
        ),
        sa.Column(
            "spotify_user_id", sa.String(length=255), unique=True, nullable=False
        ),
        sa.Column("spotify_display_name", sa.String(length=255), nullable=True),
        sa.Column("spotify_email", sa.String(length=255), nullable=True),
        sa.Column("access_token", sa.Text(), nullable=False),
        sa.Column("refresh_token", sa.Text(), nullable=False),
        sa.Column(
            "token_type", sa.String(length=50), nullable=False, server_default="Bearer"
        ),
        sa.Column("scope", sa.String(length=500), nullable=True),
        sa.Column("expires_at", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_table("spotify_connections")
