"""add product image fields

Revision ID: 9f1c4d8a2b7e
Revises: 0ad6139982e3
Create Date: 2026-02-11

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "9f1c4d8a2b7e"
down_revision: Union[str, Sequence[str], None] = "0ad6139982e3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("products", sa.Column("image_base64", sa.Text(), nullable=True))
    op.add_column("products", sa.Column("image_mime", sa.String(), nullable=True))
    op.add_column("products", sa.Column("image_filename", sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column("products", "image_filename")
    op.drop_column("products", "image_mime")
    op.drop_column("products", "image_base64")

