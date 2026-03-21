import logging
from .logger_config import setup_logger

def check_microphone(mic_status):
    setup_logger()
    if mic_status == "unavailable":
        logging.warning("Microphone unplugged")