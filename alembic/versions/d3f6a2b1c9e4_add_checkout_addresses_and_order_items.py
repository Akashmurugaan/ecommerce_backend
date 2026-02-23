"""add checkout addresses and order items

Revision ID: d3f6a2b1c9e4
Revises: e7d2957bf04f
Create Date: 2026-02-23
"""

from alembic import op
import sqlalchemy as sa


revision = "d3f6a2b1c9e4"
down_revision = "e7d2957bf04f"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "addresses",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("full_name", sa.String(), nullable=False),
        sa.Column("phone", sa.String(), nullable=False),
        sa.Column("line1", sa.String(), nullable=False),
        sa.Column("line2", sa.String(), nullable=True),
        sa.Column("city", sa.String(), nullable=False),
        sa.Column("state", sa.String(), nullable=True),
        sa.Column("postal_code", sa.String(), nullable=False),
        sa.Column("country", sa.String(), nullable=False, server_default="India"),
        sa.Column("is_default", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
    )

    op.create_table(
        "order_items",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("order_id", sa.Integer(), sa.ForeignKey("orders.id"), nullable=False),
        sa.Column("product_id", sa.Integer(), sa.ForeignKey("products.id"), nullable=False),
        sa.Column("seller_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("size_id", sa.Integer(), sa.ForeignKey("measurements.id"), nullable=False),
        sa.Column("product_name", sa.String(), nullable=False),
        sa.Column("size_name", sa.String(), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("unit_price", sa.Float(), nullable=False),
        sa.Column("subtotal", sa.Float(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_index("ix_addresses_user_id", "addresses", ["user_id"])
    op.create_index("ix_order_items_order_id", "order_items", ["order_id"])
    op.create_index("ix_order_items_seller_id", "order_items", ["seller_id"])

    op.add_column(
        "orders",
        sa.Column("total_amount", sa.Float(), nullable=False, server_default="0"),
    )
    op.add_column(
        "orders",
        sa.Column("payment_method", sa.String(), nullable=False, server_default="COD"),
    )
    op.add_column(
        "orders",
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    op.add_column("orders", sa.Column("shipping_full_name", sa.String(), nullable=True))
    op.add_column("orders", sa.Column("shipping_phone", sa.String(), nullable=True))
    op.add_column("orders", sa.Column("shipping_line1", sa.String(), nullable=True))
    op.add_column("orders", sa.Column("shipping_line2", sa.String(), nullable=True))
    op.add_column("orders", sa.Column("shipping_city", sa.String(), nullable=True))
    op.add_column("orders", sa.Column("shipping_state", sa.String(), nullable=True))
    op.add_column("orders", sa.Column("shipping_postal_code", sa.String(), nullable=True))
    op.add_column("orders", sa.Column("shipping_country", sa.String(), nullable=True, server_default="India"))


def downgrade():
    op.drop_column("orders", "shipping_country")
    op.drop_column("orders", "shipping_postal_code")
    op.drop_column("orders", "shipping_state")
    op.drop_column("orders", "shipping_city")
    op.drop_column("orders", "shipping_line2")
    op.drop_column("orders", "shipping_line1")
    op.drop_column("orders", "shipping_phone")
    op.drop_column("orders", "shipping_full_name")
    op.drop_column("orders", "created_at")
    op.drop_column("orders", "payment_method")
    op.drop_column("orders", "total_amount")

    op.drop_index("ix_order_items_seller_id", table_name="order_items")
    op.drop_index("ix_order_items_order_id", table_name="order_items")
    op.drop_index("ix_addresses_user_id", table_name="addresses")

    op.drop_table("order_items")
    op.drop_table("addresses")
