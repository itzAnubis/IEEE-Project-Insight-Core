from .logger_config import setup_logger
from .mic_health import check_mic
from .data_health import check_data

def run_health_check(mic_status: str, report: dict) -> bool:
    """
    Runs full system health check.
    Returns True if system is healthy, False otherwise.
    """

    setup_logger()

    mic_ok = check_mic(mic_status)
    data_ok = check_data(report)

    if mic_ok and data_ok:
        return True

    return False