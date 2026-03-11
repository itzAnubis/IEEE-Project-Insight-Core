import time
import random
import logging
from datetime import datetime

# --- Task 2: Implement Alert Logging ---
# Configure logging with specific levels as requested
def setup_alert_logging(log_file='system_alerts.log'):
    """
    Sets up the logging system for system alerts.
    """
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

def log_alert(issue_type):
    """
    Logs specific alerts based on the issue type.
    WARNING: Camera blocked
    ERROR: Camera disconnected
    """
    if issue_type == 'blocked':
        logging.warning("Camera blocked")
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ALERT: WARNING - Camera blocked")
    elif issue_type == 'disconnected':
        logging.error("Camera disconnected")
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ALERT: ERROR - Camera disconnected")

# --- Task 1: Implement Camera Health Monitoring ---
def check_camera_availability():
    """
    Simulates checking if the camera feed is available.
    Returns: 'available', 'blocked', or 'disconnected'
    """
    states = ['available', 'available', 'available', 'blocked', 'disconnected']
    return random.choice(states)

def start_monitoring(interval=5, duration=30):
    """
    Periodically checks camera availability and detects if feed stops.
    interval: seconds between checks
    duration: total simulation time in seconds
    """
    print(f"Starting Camera Health Monitoring (Interval: {interval}s)...")
    setup_alert_logging()
    
    start_time = time.time()
    while time.time() - start_time < duration:
        status = check_camera_availability()
        
        if status == 'available':
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Status: Camera feed is normal.")
        else:
            # Task 3: Connect Alerts with System (Triggering alerts during runtime)
            log_alert(status)
            
        time.sleep(interval)
    
    print("Monitoring session completed.")

if __name__ == "__main__":
    # Run the monitoring for 30 seconds with a 5-second interval
    start_monitoring(interval=5, duration=30)
