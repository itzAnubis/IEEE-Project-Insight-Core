from .mic_monitor import check_microphone
from .vision_monitor import check_vision
from .nlp_monitor import check_nlp
from .logger_config import setup_logger
import logging

def monitor_system(mic_status, vision_data, nlp_data):
    setup_logger()

    check_microphone(mic_status)
    check_vision(vision_data)
    check_nlp(nlp_data)

    logging.info("System monitoring completed")