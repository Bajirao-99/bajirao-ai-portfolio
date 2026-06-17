from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool
from sqlalchemy.engine import URL

from app.db.database import Base, DATABASE_URL

from app.models import (  # noqa: F401
    Achievement,
    AdminUser,
    Certification,
    ChatInteraction,
    CodingProfile,
    ContactMessage,
    Education,
    Experience,
    GitHubProfile,
    GitHubRepository,
    InterviewRequest,
    JobMatchAnalysis,
    PageView,
    Profile,
    Project,
    ProjectImage,
    ResearchPublication,
    Resume,
    SiteVisitor,
    Skill,
)


config = context.config


if config.config_file_name is not None:
    fileConfig(config.config_file_name)


# DATABASE_URL can be either:
# 1. A SQLAlchemy URL object during local development
# 2. A string from Render's DATABASE_URL environment variable
if isinstance(DATABASE_URL, URL):
    database_url_string = DATABASE_URL.render_as_string(
        hide_password=False
    )
else:
    database_url_string = str(DATABASE_URL)


# Alembic ConfigParser treats % as interpolation syntax.
database_url_string = database_url_string.replace(
    "%",
    "%%",
)


config.set_main_option(
    "sqlalchemy.url",
    database_url_string,
)


target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option(
        "sqlalchemy.url"
    )

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={
            "paramstyle": "named",
        },
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    configuration = config.get_section(
        config.config_ini_section,
        {},
    )

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()