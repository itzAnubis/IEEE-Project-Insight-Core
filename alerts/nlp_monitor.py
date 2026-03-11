import logging
from .logger_config import setup_logger

def check_nlp(nlp_data):
    setup_logger()
    if nlp_data is None:
        logging.error("Missing NLP data")