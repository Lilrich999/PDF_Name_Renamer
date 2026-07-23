"""
logger.py
---------
Sets up a single shared logger that writes to both the console
and log.txt. Import `get_logger()` from any module instead of
configuring logging separately everywhere.
"""

import logging
import config


def get_logger(name: str = "pdf_renamer") -> logging.Logger:
    logger = logging.getLogger(name)

    if logger.handlers:
        # Already configured (e.g. imported from multiple modules) --
        # avoid adding duplicate handlers which would duplicate log lines.
        return logger

    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # File handler -- everything, so you always have a full record.
    file_handler = logging.FileHandler(config.LOG_FILE, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Console handler -- just the highlights while the program runs.
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
