
import cv2
import time
import logging
from camera_simulator import CameraSimulator

# Configure logging
logging.basicConfig(filename='camera_alerts.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def run_system(camera_id=0):
    camera = CameraSimulator(camera_id)
    print(f"Starting system for Camera {camera_id}. Press 'q' to quit.")
    logging.info(f"System started for Camera {camera_id}")

    while True:
        frame, status_msg = camera.get_frame()
        
        # Log the status
        if "ERROR" in status_msg:
            logging.error(status_msg)
            print(status_msg)
        elif "WARNING" in status_msg:
            logging.warning(status_msg)
            print(status_msg)
        else:
            # logging.info(status_msg) # Avoid flooding logs with INFO
            pass

        # Display the frame if available
        if frame is not None:
            # Add status text on the frame
            cv2.putText(frame, status_msg, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow('Camera Feed', frame)
        else:
            # If no frame (failure), show a black screen with the error message
            import numpy as np
            black_frame = np.zeros((480, 640, 3), dtype=np.uint8)
            cv2.putText(black_frame, status_msg, (50, 240), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.imshow('Camera Feed', black_frame)

        # Break loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    camera.release()
    logging.info(f"System stopped for Camera {camera_id}")
    print(f"System stopped for Camera {camera_id}.")

if __name__ == "__main__":
    run_system(0) # 0 is usually the default laptop camera
