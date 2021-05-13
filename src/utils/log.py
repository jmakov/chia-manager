import logging
from logging import handlers


def configure_logger(logger, log_path):
    logger.setLevel(logging.DEBUG)
    fh = handlers.RotatingFileHandler(log_path, backupCount=2, maxBytes=5000000)

    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s %(name)s.%(funcName)s:%(lineno)s:%(levelname)s:%(message)s")
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logging.info("Logger configured")