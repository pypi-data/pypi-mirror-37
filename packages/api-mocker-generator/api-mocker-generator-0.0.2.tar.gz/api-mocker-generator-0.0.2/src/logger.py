import logging


def set_verbose_logging() -> None:
    logging.basicConfig(level=logging.DEBUG)


def debug(message: str) -> None:
    logging.debug(message)


def info(message: str) -> None:
    logging.info(message)
