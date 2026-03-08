import random
from camera_logging_en import setup_logging, log_camera_event

# Setup logging at the start of execution
setup_logging()

def simulate_camera_feed():
    """
    Dummy function to simulate camera feed availability.
    Returns one of three states: 'available', 'blocked', 'disconnected'.
    """
    states = ['available', 'blocked', 'disconnected']
    # Choose a random state for simulation
    return random.choice(states)

def test_health_check():
    """
    Function to test the health check and trigger correct logging if the camera is blocked or disconnected.
    """
    print("Starting Camera Health Check Simulation...")
    
    # Simulate health check 5 times
    for i in range(5):
        status = simulate_camera_feed()
        print(f"Test {i+1}: Camera status is '{status}'")
        
        if status == 'blocked':
            log_camera_event("Camera blocked", "WARNING")
            print("   -> Logged: Camera blocked (WARNING)")
        elif status == 'disconnected':
            log_camera_event("Camera disconnected", "CRITICAL")
            print("   -> Logged: Camera disconnected (CRITICAL)")
        else:
            print("   -> Camera is working correctly.")

if __name__ == "__main__":
    test_health_check()
    print("\nHealth check simulation completed. Check 'camera_events_en.log' for details.")
