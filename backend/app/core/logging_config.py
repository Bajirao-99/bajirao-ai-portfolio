import logging
import sys

from app.core.config import settings


def configure_logging() -> None:
    log_level = getattr(
        logging,
        settings.log_level.upper(),
        logging.INFO,
    )

    logging.basicConfig(
        level=log_level,
        stream=sys.stdout,
        format=(
            "%(asctime)s | "
            "%(levelname)s | "
            "%(name)s | "
            "%(message)s"
        ),
        force=True,
    )

    logging.getLogger(
        "sqlalchemy.engine"
    ).setLevel(logging.WARNING)

    logging.getLogger(
        "httpx"
    ).setLevel(logging.WARNING)