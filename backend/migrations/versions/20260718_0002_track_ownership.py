"""add track ownership

Revision ID: 20260718_0002
Revises: 20260718_0001
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260718_0002"
down_revision: str | None = "20260718_0001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "tracks",
        sa.Column(
            "owner_id",
            sa.String(length=255),
            nullable=False,
            server_default="anonymous",
        ),
    )
    op.create_index("ix_tracks_owner_id", "tracks", ["owner_id"])


def downgrade() -> None:
    op.drop_index("ix_tracks_owner_id", table_name="tracks")
    op.drop_column("tracks", "owner_id")
