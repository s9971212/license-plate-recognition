import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def setup_logging(log_file: Path):
    """
    設定 Application Logging
    """

    logger = logging.getLogger()

    # 避免重複設定
    if logger.handlers:
        return

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        fmt="%(asctime)s "
            "[%(levelname)s] "
            "%(name)s: "
            "%(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # =========================
    # Console
    # =========================

    console_handler = logging.StreamHandler()

    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    # =========================
    # File
    # =========================

    log_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    file_handler = RotatingFileHandler(
        filename=log_file,
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5,
        encoding="utf-8",
    )

    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
