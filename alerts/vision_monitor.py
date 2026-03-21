import logging
from .logger_config import setup_logger

def check_vision(vision_data):
    setup_logger()
    if vision_data is None:
        logging.error("Missing Vision data")