"""merge heads: checkout and wishlist

Revision ID: 9b1b2d5db5a1
Revises: 45ad16686dad, d3f6a2b1c9e4
Create Date: 2026-02-23
"""

from typing import Sequence, Union

from alembic import op


revision: str = "9b1b2d5db5a1"
down_revision: Union[str, Sequence[str], None] = ("45ad16686dad", "d3f6a2b1c9e4")
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Merge revision (no schema changes)."""
    pass


def downgrade() -> None:
    """Downgrade merge revision (no schema changes)."""
    pass

