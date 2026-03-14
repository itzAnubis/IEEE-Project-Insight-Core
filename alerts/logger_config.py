import logging

def setup_logger():
    logging.basicConfig(
        filename="system_logs.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        force=True
    )