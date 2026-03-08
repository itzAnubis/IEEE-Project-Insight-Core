import logging
import os
from datetime import datetime

# Logging System Setup
def setup_logging(log_file='camera_events_en.log'):
    """
    Sets up the logging system to save events to a file with timestamps and severity.
    """
    # Ensure the directory exists if the path contains directories
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Configure the format (Timestamp, Severity Level, Message)
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

def log_camera_event(issue_type, severity='ERROR'):
    """
    Logs a camera event (blocked or disconnected).
    """
    message = f"Camera Issue Detected: {issue_type}"
    
    if severity == 'INFO':
        logging.info(message)
    elif severity == 'WARNING':
        logging.warning(message)
    elif severity == 'ERROR':
        logging.error(message)
    elif severity == 'CRITICAL':
        logging.critical(message)
    else:
        logging.error(message)

if __name__ == "__main__":
    # Simple test for the logging system
    setup_logging()
    log_camera_event("Camera blocked", "WARNING")
    log_camera_event("Camera disconnected", "CRITICAL")
    print("Logs have been saved to camera_events_en.log")
