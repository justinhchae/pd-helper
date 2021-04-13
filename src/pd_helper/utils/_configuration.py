import logging
import sys


def _configuration(echo=False):
    """Runs configuration for logging.
    """
    if echo:
        level = logging.INFO
    else:
        level = None

    logger = logging.getLogger("pipeline").getChild("configuration")
    format = "%(asctime)s:%(name)s:%(levelname)s:%(message)s"

    log_formatter = logging.Formatter(format)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(log_formatter)

    logging.basicConfig(format=format, level=level)
    logging.getLogger().addHandler(stream_handler)

    if echo:
        logger.info("Logging configured.")



