import logging

def check_mic(mic_status: str) -> bool:
    """
    Checks microphone status.
    Returns True if mic is healthy, False otherwise.
    """

    if mic_status == "unavailable":
        logging.error("Mic Issue: Microphone Unavailable")
        return False

    elif mic_status == "muted":
        logging.warning("Mic Issue: Microphone Muted")
        return True

    logging.info("Mic Status: Working Properly")
    return True