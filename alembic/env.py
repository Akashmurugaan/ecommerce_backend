from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv
import os

# Load .env
load_dotenv()

# Alembic Config
config = context.config

# Set database URL from env
config.set_main_option(
    "sqlalchemy.url",
    os.getenv("DATABASE_URL")
)

# Logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Import Base and models
from app.db.base import Base
from app.db.models.user import User
from app.db.models.product import Product
from app.db.models.cart import Cart
from app.db.models.cart_item import CartItem
from app.db.models.order import Order
from app.db.models.wishlist import Wishlist
from app.db.models.category import Category
from app.db.models.measurement import Measurement
from app.db.models.product_measurement import ProductMeasurement        

target_metadata = Base.metadata


def run_migrations_offline():
    context.configure(
        url=os.getenv("DATABASE_URL"),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},

    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()








# from logging.config import fileConfig
# from sqlalchemy import engine_from_config

# from sqlalchemy import pool
# from alembic import context

# # Alembic Config object
# config = context.config

# # Setup logging
# if config.config_file_name is not None:
#     fileConfig(config.config_file_name)

# # Import your app settings & DB base
# from app.core.config import settings
# from app.core.database import Base

# # IMPORTANT: import all models so Alembic can detect them
# from app import models  # noqa

# # Set DB URL from .env via settings
# config.set_main_option(
#     "sqlalchemy.url",
#     settings.DATABASE_URL
# )

# target_metadata = Base.metadata


# def run_migrations_offline() -> None:
   
#     url = config.get_main_option("sqlalchemy.url")
#     context.configure(
#         url=url,
#         target_metadata=target_metadata,
#         literal_binds=True,
#         dialect_opts={"paramstyle": "named"},
#         compare_type=True,
#     )

#     with context.begin_transaction():
#         context.run_migrations()


# def run_migrations_online() -> None:
   
#     connectable = engine_from_config(
#         config.get_section(config.config_ini_section),
#         prefix="sqlalchemy.",
#         poolclass=pool.NullPool,
#     )

#     with connectable.connect() as connection:
#         context.configure(
#             connection=connection,
#             target_metadata=target_metadata,
#             compare_type=True,
#         )

#         with context.begin_transaction():
#             context.run_migrations()


# if context.is_offline_mode():
#     run_migrations_offline()
# else:
#     run_migrations_online()
