"""Optional LagaPy logging configuration with independent output levels.

LagaPy does not configure the application-wide root logger. Libraries should
use ``logging.getLogger(__name__)`` and leave this setup to their caller.
"""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOGGER_NAME = "lagapy"


def configure_logging(
    *,
    console_level: int | None = logging.INFO,
    file_level: int = logging.DEBUG,
    output: str | Path | None = None,
    max_bytes: int = 5_000_000,
    backup_count: int = 3,
) -> logging.Logger:
    """Configure LagaPy logging to the console, a rotating file, or both.

    Console and file handlers filter messages independently. The level of the
    shared ``lagapy`` logger is automatically set to the *lowest* active
    handler level, so a quiet console cannot suppress detailed file logs.

    Calling this function again replaces the LagaPy handlers (without
    changing the root logger) and does not duplicate messages. File output is
    appended and rotates when ``max_bytes`` is reached.

    Args:
        console_level: Minimum console severity; ``None`` disables console
            logging. Console messages are sent to standard error.
        file_level: Minimum file severity, if ``output`` is provided.
        output: Optional path to a rotating log file, whose parent directory
            will be created if it does not exist.
        max_bytes: Maximum size of each file before rotation, in bytes.
        backup_count: Number of old log files to keep when rotating.

    Returns:
        The configured ``lagapy`` logger.

    Examples:
        >>> configure_logging(console_level=logging.WARNING)
        <Logger lagapy (WARNING)>
        >>> # configure_logging(console_level=logging.INFO,
        >>> #                   output="logs/run.log", file_level=logging.DEBUG)
    """
    if max_bytes <= 0:
        raise ValueError("max_bytes must be greater than zero")
    if backup_count < 0:
        raise ValueError("backup_count cannot be negative")
    for name, value in (("console_level", console_level), ("file_level", file_level)):
        if name == "console_level" and value is None:
            continue
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            raise ValueError(f"{name} must be a nonnegative logging level")

    formatter = logging.Formatter(
        "%(asctime)s %(levelname)-8s %(name)s: %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
    )

    # Construct new handlers first: an invalid output path should not destroy
    # a previously working logging configuration.
    handlers: list[logging.Handler] = []
    try:
        if console_level is not None:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(console_level)
            console_handler.setFormatter(formatter)
            handlers.append(console_handler)

        if output is not None:
            path = Path(output).expanduser()
            path.parent.mkdir(parents=True, exist_ok=True)
            file_handler = RotatingFileHandler(
                path,
                mode="a",
                maxBytes=max_bytes,
                backupCount=backup_count,
                encoding="utf-8",
            )
            file_handler.setLevel(file_level)
            file_handler.setFormatter(formatter)
            handlers.append(file_handler)
    except Exception:
        for handler in handlers:
            handler.close()
        raise

    logger = logging.getLogger(LOGGER_NAME)
    # NOTSET (0) on a logger inherits the root logger's level. Use 1 instead
    # when an active handler requests NOTSET, so all standard messages pass.
    logger.setLevel(max(1, min((handler.level for handler in handlers), default=logging.CRITICAL + 1)))
    logger.propagate = False
    for old_handler in logger.handlers[:]:
        logger.removeHandler(old_handler)
        old_handler.close()
    for handler in handlers:
        logger.addHandler(handler)
    return logger
