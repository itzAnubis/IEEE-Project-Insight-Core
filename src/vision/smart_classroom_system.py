import cv2
import time
import json
import supervision as sv
from ultralytics import YOLO
import mediapipe as mp

# Importing Team Modules
from pid_controller import CameraTrackerPID
from distraction_logic import classify_distraction
from head_pose_utils import get_head_pose

class SmartClassroomSystem:
    def __init__(self):
        # 1. Initialize YOLO & Tracker (Ahmed ShamsEldin)
        print("Loading YOLO model...")
        self.model = YOLO('yolov8n.pt')
        self.tracker = sv.ByteTrack()
        
        # 2. Initialize PID (Ahmed AbdElSalam)
        self.pid_controller = CameraTrackerPID()
        
        # 3. Initialize MediaPipe (Kareem & Sari)
        # We use FaceMesh for Head Pose and Hands for Distraction
        self.mp_face_mesh = mp.solutions.face_mesh
        self.mp_hands = mp.solutions.hands
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5, min_tracking_confidence=0.5
        )
        self.hands = self.mp_hands.Hands(
            max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5
        )

        # 4. Crowd Counting & Logic (Ezzeldin & Demiana)
        self.last_crowd_count_time = time.time()
        self.crowd_history = []
        self.instructor_id = None # Assume we lock onto the first person detected as instructor

        # Visualization
        self.box_annotator = sv.BoxAnnotator()
        self.label_annotator = sv.LabelAnnotator()

    def process_instructor_details(self, frame, instructor_bbox):
        """
        Runs FaceMesh and Hands ONLY on the instructor's Region of Interest (ROI).
        This optimization ensures we meet the 15+ FPS requirement (Demiana).
        """
        x1, y1, x2, y2 = map(int, instructor_bbox)
        
        # Ensure ROI is within frame bounds
        h, w, _ = frame.shape
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(w, x2), min(h, y2)
        
        # Crop ROI
        roi = frame[y1:y2, x1:x2]
        if roi.size == 0:
            return 0, [], "No Data"

        # Convert ROI to RGB for MediaPipe
        roi_rgb = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
        
        # 1. Get Head Pose (Kareem)
        pitch, yaw, roll = 0, 0, 0
        face_landmark_list = []
        
        results_face = self.face_mesh.process(roi_rgb)
        if results_face.multi_face_landmarks:
            # We use the first face found in the ROI
            mesh_landmarks = results_face.multi_face_landmarks[0]
            
            # Calculate Angles (Note: we pass ROI dimensions, results are relative to head)
            pitch, yaw, roll = get_head_pose(mesh_landmarks, x2-x1, y2-y1)
            
            # Extract specific landmarks for Sari's logic (Chin point usually index 152)
            # Sari expects [x, y, z] global coords or relative. 
            # We return relative to ROI for distance calcs if needed, but let's return chin global coords.
            chin = mesh_landmarks.landmark[152]
            face_landmark_list = [chin.x * (x2-x1) + x1, chin.y * (y2-y1) + y1, chin.z]

        # 2. Get Hands (Sari)
        hand_landmarks_list = []
        results_hands = self.hands.process(roi_rgb)
        if results_hands.multi_hand_landmarks:
            for hand_lm in results_hands.multi_hand_landmarks:
                # Convert all 21 points to global coordinates
                hand_points = []
                for lm in hand_lm.landmark:
                    px = int(lm.x * (x2-x1)) + x1
                    py = int(lm.y * (y2-y1)) + y1
                    hand_points.append([px, py, lm.z])
                hand_landmarks_list.append(hand_points)

        # 3. Classify Distraction (Sari)
        # Note: If face_landmark_list is empty, classify_distraction handles IndexError
        status = classify_distraction(self.instructor_id, pitch, face_landmark_list, hand_landmarks_list)

        return pitch, hand_landmarks_list, status

    def run(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Could not open webcam.")
            return

        print("System Started. Press 'q' to quit.")

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            h, w, _ = frame.shape
            
            # --- STEP 1: Detection & Tracking (Ahmed ShamsEldin) ---
            results = self.model(frame, classes=[0], verbose=False)
            detections = sv.Detections.from_ultralytics(results[0])
            detections = self.tracker.update_with_detections(detections)
            
            total_people = len(detections)
            
            # --- STEP 2: Crowd Counting (Ezzeldin) ---
            current_time = time.time()
            if current_time - self.last_crowd_count_time > 60:
                print(f"[Crowd Count] Total people detected: {total_people}")
                # In a real app, send this to a database/log file
                self.crowd_history.append({"timestamp": current_time, "count": total_people})
                self.last_crowd_count_time = current_time

            # --- STEP 3: Instructor Identification & Processing ---
            instructor_bbox = None
            instructor_status = "Unknown"
            pitch_angle = 0
            
            # Determine Instructor ID (Logic: Persist ID once set, or take the first one)
            if self.instructor_id is None and len(detections) > 0:
                 self.instructor_id = detections.tracker_id[0]

            # Loop through detections to find our instructor
            for i in range(len(detections)):
                if detections.tracker_id is not None and detections.tracker_id[i] == self.instructor_id:
                    instructor_bbox = detections.xyxy[i]
                    
                    # Run Advanced Logic (Kareem + Sari) on ROI
                    pitch_angle, hands, status = self.process_instructor_details(frame, instructor_bbox)
                    instructor_status = status
                    break
            
            # --- STEP 4: PID Control (Ahmed AbdElSalam) ---
            pan_adj, tilt_adj = 0.0, 0.0
            if instructor_bbox is not None:
                pan_adj, tilt_adj = self.pid_controller.update(instructor_bbox, w, h)

            # --- STEP 5: Visualization (Demiana) ---
            # Draw all people
            annotated_frame = self.box_annotator.annotate(scene=frame.copy(), detections=detections)
            
            labels = []
            if detections.tracker_id is not None:
                for idx, tracker_id in enumerate(detections.tracker_id):
                    label = f"ID: {tracker_id}"
                    # Highlight Instructor
                    if tracker_id == self.instructor_id:
                        label += f" [INSTRUCTOR: {instructor_status}]"
                    labels.append(label)
            
            annotated_frame = self.label_annotator.annotate(scene=annotated_frame, detections=detections, labels=labels)
            
            # Overlay Info
            info = [
                f"FPS: {int(1/(time.time()-current_time+0.001))}", # Approx FPS
                f"Total People: {total_people} (Every 60s)",
                f"Instructor ID: {self.instructor_id}",
                f"Head Pitch: {pitch_angle:.1f}",
                f"Status: {instructor_status}",
                f"PID Out: Pan={pan_adj:.1f}, Tilt={tilt_adj:.1f}"
            ]
            
            for i, text in enumerate(info):
                cv2.putText(annotated_frame, text, (10, 30 + i*25), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            # --- STEP 6: JSON Stream Output (Demiana) ---
            # This is the data structure sent to other squads/backend
            json_output = {
                "timestamp": current_time,
                "instructor": {
                    "id": int(self.instructor_id) if self.instructor_id else None,
                    "status": instructor_status,
                    "head_pitch": float(pitch_angle),
                    "pid_adjustments": {"pan": float(pan_adj), "tilt": float(tilt_adj)}
                },
                "environment": {
                    "total_people_count": total_people,
                    "crowd_history_length": len(self.crowd_history)
                }
            }
            # print(json.dumps(json_output)) # Uncomment to see stream in console

            cv2.imshow("Smart Classroom System", annotated_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    system = SmartClassroomSystem()
    system.run()