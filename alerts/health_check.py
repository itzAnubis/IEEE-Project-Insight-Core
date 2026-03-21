from .logger_config import setup_logger
from .mic_health import check_mic
from .data_health import check_data

def run_health_check(mic_ok: bool, vision_ok: bool, nlp_ok: bool) -> bool:
    """
    Runs full system health check.
    Returns True if system is healthy, False otherwise.
    """

    setup_logger()

    mic_status = check_mic(mic_ok)
    data_status = check_data(vision_ok, nlp_ok)

    return mic_status and data_status