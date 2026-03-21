import logging

def check_mic(is_available: bool) -> bool:
    if not is_available:
        logging.warning("Microphone unplugged")
        return False   # مهم جدًا

    logging.info("Microphone is working")
    return True