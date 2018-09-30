import datetime
import logging
import colorlog


def get_date(s: str) -> datetime.date:
    """
    Helper function to convert string to datetime.date instance
    """
    return datetime.datetime.strptime(s, '%Y-%m-%d').date()


def configure_logging(log_level='INFO'):
    fmt = '%(log_color)s%(asctime)s [%(name)s]%(reset)s %(message)s'
    handler = colorlog.StreamHandler()
    handler.setFormatter(colorlog.ColoredFormatter(fmt))
    logging.basicConfig(level=log_level, format=fmt, handlers=[handler])
