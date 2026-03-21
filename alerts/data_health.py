import logging

def check_data(vision_data: bool, nlp_data: bool) -> bool:
    """
    Checks if Vision and NLP modules are sending data.
    Returns True if both are working, False otherwise.
    """

    system_ok = True

    if not vision_data:
        logging.error("Missing Vision data")
        system_ok = False

    if not nlp_data:
        logging.error("Missing NLP data")
        system_ok = False

    if system_ok:
        logging.info("All data streams are working")

    return system_ok