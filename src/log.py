import logging
from src.utils import get_current_date_and_time

FORMATTER = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

def _setup_console_logger(logger, formatter: logging.Formatter = FORMATTER):
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

def _setup_file_logger(logger, formatter: logging.Formatter = FORMATTER):
    file_handler = logging.FileHandler(f'logs/{get_current_date_and_time()}.log')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

def get_logger(console_loger=True, file_logger=True) -> logging.Logger:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    if console_loger:
        _setup_console_logger(logger)
    if file_logger:
        _setup_file_logger(logger)

    return logger

