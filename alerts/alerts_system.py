import logging

logging.basicConfig(
    filename="alerts_logs.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    force=True
)

def simulate_microphone(status):
    if status == "unplugged":
        logging.error("Mic unplugged")
    elif status == "muted":
        logging.warning("Mic muted")
    elif status == "stopped":
        logging.error("Audio stream stopped")
    else:
        logging.info("Mic is working")

def simulate_data(vision_status, nlp_status):

    if vision_status == "stopped":
        logging.error("Missing Vision data")
    else:
        logging.info("Vision data is working")

    if nlp_status == "stopped":
        logging.error("Missing NLP data")
    else:
        logging.info("NLP data is working")


simulate_microphone("unplugged")
simulate_microphone("muted")
simulate_microphone("stopped")

simulate_data("stopped", "stopped")
simulate_data("active", "active")