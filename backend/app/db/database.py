from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import (
    DeclarativeBase,
    Session,
    sessionmaker,
)

from app.core.config import settings


def read_secret(value: object) -> str:
    if hasattr(value, "get_secret_value"):
        return str(value.get_secret_value())

    return str(value)


def get_database_url() -> str | URL:
    cloud_database_url = (
        settings.database_url or ""
    ).strip()

    if cloud_database_url:
        if cloud_database_url.startswith(
            "postgres://"
        ):
            cloud_database_url = (
                cloud_database_url.replace(
                    "postgres://",
                    "postgresql+psycopg://",
                    1,
                )
            )

        elif cloud_database_url.startswith(
            "postgresql://"
        ):
            cloud_database_url = (
                cloud_database_url.replace(
                    "postgresql://",
                    "postgresql+psycopg://",
                    1,
                )
            )

        return cloud_database_url

    return URL.create(
        drivername="postgresql+psycopg",
        username=settings.db_user,
        password=read_secret(
            settings.db_password
        ),
        host=settings.db_host,
        port=settings.db_port,
        database=settings.db_name,
    )


DATABASE_URL = get_database_url()


engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
)


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    pass


def get_db() -> Generator[
    Session,
    None,
    None,
]:
    database_session = SessionLocal()

    try:
        yield database_session
    finally:
        database_session.close()