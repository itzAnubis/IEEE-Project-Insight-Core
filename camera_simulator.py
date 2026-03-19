
import cv2
import random

class CameraSimulator:
    def __init__(self, camera_id=0):
        self.camera_id = camera_id
        self.status = "active"
        self.cap = None
        self.open_camera()

    def open_camera(self):
        """Try to open the real camera."""
        self.cap = cv2.VideoCapture(self.camera_id)
        if not self.cap.isOpened():
            self.status = "disconnected"
            return False
        self.status = "active"
        return True

    def get_frame(self):
        """Get a frame from the camera, simulating failures."""
        # Simulate different camera problems randomly
        rand_val = random.randint(1, 100)
        
        if rand_val <= 2:  # 2% chance of disconnection
            self.status = "disconnected"
            if self.cap:
                self.cap.release()
            return None, "ERROR: Camera disconnected"
        
        elif rand_val <= 5:  # 3% chance of being blocked (black screen)
            self.status = "blocked"
            return None, "WARNING: Camera blocked"
        
        elif rand_val <= 8:  # 3% chance of stopping (frozen frame)
            self.status = "stopped"
            return None, "WARNING: Camera stopped during runtime"
        
        # Normal operation
        if self.status == "disconnected":
            # Try to reconnect if it was disconnected
            if self.open_camera():
                self.status = "active"
            else:
                return None, "ERROR: Camera disconnected"

        if self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                self.status = "stopped"
                return None, "WARNING: Camera stopped during runtime"
            
            self.status = "active"
            return frame, "INFO: Camera is active"
        
        return None, "ERROR: Camera disconnected"

    def release(self):
        if self.cap:
            self.cap.release()
            cv2.destroyAllWindows()
