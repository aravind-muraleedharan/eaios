"""Logging setup: JSON lines to the console and to a rotating file."""

import json
import logging
from datetime import UTC, datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_DIR = Path("logs")
LOG_FILE = LOG_DIR/"eaios.log"
MAX_BYTES = 5_000_000 # Rotate after 5 MB
BACKUP_COUNT = 5 # Keep the most recent rotates files.


class jsonFormatter(logging.Formatter):
    """Format each log record as a single line of JSON."""

    def format(self, record: logging.LogRecord) -> str:
        entry = {
            "timestamp": datetime.fromtimestamp(record.created, tz=UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        # Extra structured fields passed as extra={"fields": {...}}.
        fields = getattr(record, "fields", None)
        if fields:
            entry.update(fields)

        if record.exc_info:
            entry["exception"] = self.formatException(record.exc_info)

        return json.dumps(entry)


def setup_logging(level: str) -> None:
    """Send JSON logs to the console and to a rotating file."""
    LOG_DIR.mkdir(exist_ok=True)
    formatter = jsonFormatter()

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=MAX_BYTES,
        backupCount=BACKUP_COUNT,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)

    logger = logging.getLogger("eaios")
    logger.setLevel(level)
    logger.handlers = [console_handler, file_handler]
    logger.propagate = False




