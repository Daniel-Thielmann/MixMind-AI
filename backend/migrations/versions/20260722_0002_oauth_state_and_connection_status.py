"""create oauth_states table and add columns to spotify_connections

Revision ID: 20260722_0002
Revises: 20260722_0001
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260722_0002"
down_revision: str | None = "20260722_0001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "oauth_states",
        sa.Column("nonce", sa.String(length=64), primary_key=True),
        sa.Column("user_id", sa.String(length=255), nullable=False, index=True),
        sa.Column("provider", sa.String(length=50), nullable=False),
        sa.Column("expires_at", sa.Integer(), nullable=False),
        sa.Column(
            "consumed", sa.Boolean(), nullable=False, server_default=sa.text("false")
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )

    op.add_column(
        "spotify_connections",
        sa.Column(
            "status", sa.String(length=50), nullable=False, server_default="active"
        ),
    )
    op.add_column(
        "spotify_connections",
        sa.Column("authorized_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.add_column(
        "spotify_connections",
        sa.Column("last_refresh_at", sa.DateTime(timezone=True), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("spotify_connections", "last_refresh_at")
    op.drop_column("spotify_connections", "authorized_at")
    op.drop_column("spotify_connections", "status")
    op.drop_table("oauth_states")
