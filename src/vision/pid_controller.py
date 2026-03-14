from simple_pid import PID

class CameraTrackerPID:
    def __init__(self, pan_limits: tuple = (-45, 45), tilt_limits: tuple = (-45, 45)):
        """
        Initialize the PID controllers for Pan (X) and Tilt (Y).
        """
        # Tuned PID constants
        self.Kp_x = 0.12
        self.Ki_x = 0.0005
        self.Kd_x = 0.03
        
        self.Kp_y = 0.12
        self.Ki_y = 0.0005
        self.Kd_y = 0.03
        
        # Initialize Pan PID
        self.pid_pan = PID(self.Kp_x, self.Ki_x, self.Kd_x, setpoint=0)
        self.pid_pan.output_limits = pan_limits
        self.pid_pan.integral_limits = (-200, 200)  # Prevent integral windup
        
        # Initialize Tilt PID
        self.pid_tilt = PID(self.Kp_y, self.Ki_y, self.Kd_y, setpoint=0)
        self.pid_tilt.output_limits = tilt_limits
        self.pid_tilt.integral_limits = (-200, 200)  # Prevent integral windup
        
        # Track previous errors for reset detection
        self.prev_error_x = 0
        self.prev_error_y = 0

    def update(self, instructor_bbox: tuple, frame_width: int, frame_height: int) -> tuple:
        if not instructor_bbox or frame_width == 0 or frame_height == 0:
            return (0.0, 0.0)

        x1, y1, x2, y2 = instructor_bbox
        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2

        frame_center_x = frame_width / 2
        frame_center_y = frame_height / 2

        self.pid_pan.setpoint = frame_center_x
        self.pid_tilt.setpoint = frame_center_y

        error_x = frame_center_x - center_x
        error_y = frame_center_y - center_y

        # Anti-windup reset logic
        if abs(error_x - self.prev_error_x) > 50:
            self.pid_pan.reset()
        if abs(error_y - self.prev_error_y) > 50:
            self.pid_tilt.reset()

        self.prev_error_x = error_x
        self.prev_error_y = error_y

        pan_adjustment = self.pid_pan(center_x)
        tilt_adjustment = self.pid_tilt(center_y)

        return (pan_adjustment, tilt_adjustment)