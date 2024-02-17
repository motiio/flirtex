import asyncio

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from sqlalchemy.schema import CreateSchema

from alembic import context
from src.config.settings import settings as app_settings
from src.modules import *

# from src.config.models import Base
from src.core.models import BaseModel

TECH_SCHEMA_NAME = "tech"  # Изменено с "core" на "tech"

def include_object(object, name, type_, reflected, compare_to):
    if type_ == "table":
        return object.schema in [None, TECH_SCHEMA_NAME]  # Использование TECH_SCHEMA_NAME
    else:
        return True

# Это объект конфигурации Alembic
config = context.config
config.set_main_option("sqlalchemy.url", app_settings.DATABASE_URI)

# Метаданные вашей модели для поддержки 'autogenerate'
target_metadata = BaseModel.metadata

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_schemas=True,
        version_table_schema=TECH_SCHEMA_NAME  # Указывает схему для таблицы версий Alembic
    )

    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection: Connection) -> None:
    def process_revision_directives(context, revision, directives):
        script = directives[0]
        if script.upgrade_ops.is_empty():
            directives[:] = []
            print("No changes found skipping revision creation.")
        else:
            # Попытка создать схему, если она еще не существует
            connection.execute(CreateSchema(TECH_SCHEMA_NAME))

    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        include_schemas=True,
        include_object=include_object,
        process_revision_directives=process_revision_directives,
        version_table_schema=TECH_SCHEMA_NAME  # Также укажите схему здесь
    )

    with context.begin_transaction():
        context.run_migrations()

async def run_async_migrations() -> None:
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
