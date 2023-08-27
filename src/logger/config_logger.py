import logging
from globals.constants import CONSTANTS
import sys

def configure_logger():
    formatters = CONSTANTS.Logger.Formatters
    basic_formatter = logging.Formatter(formatters.basic_log_formatter['format'], datefmt=formatters.basic_log_formatter['datefmt'])
    # Add log handlers:
    # Add stdout handler
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.DEBUG)
    stdout_handler.setFormatter(basic_formatter)

    # Add file handler
    file_handler = logging.FileHandler(filename="data-quality-tools.log", mode="a", encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(basic_formatter)


    logger = logging.getLogger()
    logger.setLevel(logging.INFO)  # set logger level
    logger.addHandler(stdout_handler)
    logger.addHandler(file_handler)