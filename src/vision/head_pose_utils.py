import cv2
import numpy as np

def get_head_pose(landmarks, frame_width, frame_height):
    """
    Calculates Pitch, Yaw, and Roll using FaceMesh landmarks and solvePnP.
    
    Args:
        landmarks: MediaPipe FaceMesh landmarks object.
        frame_width: Width of the video frame.
        frame_height: Height of the video frame.
        
    Returns:
        tuple: (pitch, yaw, roll) in degrees.
    """
    # 3D Model points (Standard face model)
    model_points = np.array([
        (0.0, 0.0, 0.0),             # Nose tip
        (0.0, -330.0, -65.0),        # Chin
        (-225.0, 170.0, -135.0),     # Left eye left corner
        (225.0, 170.0, -135.0),      # Right eye right corner
        (-150.0, -150.0, -125.0),    # Left Mouth corner
        (150.0, -150.0, -125.0)      # Right mouth corner
    ])

    # 2D Image points corresponding to the model points
    # Indices: 1 (Nose), 152 (Chin), 33 (Left Eye), 263 (Right Eye), 61 (Mouth Left), 291 (Mouth Right)
    image_points = []
    
    try:
        # Nose
        image_points.append([landmarks.landmark[1].x * frame_width, landmarks.landmark[1].y * frame_height])
        # Chin
        image_points.append([landmarks.landmark[152].x * frame_width, landmarks.landmark[152].y * frame_height])
        # Left Eye
        image_points.append([landmarks.landmark[33].x * frame_width, landmarks.landmark[33].y * frame_height])
        # Right Eye
        image_points.append([landmarks.landmark[263].x * frame_width, landmarks.landmark[263].y * frame_height])
        # Left Mouth
        image_points.append([landmarks.landmark[61].x * frame_width, landmarks.landmark[61].y * frame_height])
        # Right Mouth
        image_points.append([landmarks.landmark[291].x * frame_width, landmarks.landmark[291].y * frame_height])
    except IndexError:
        return 0, 0, 0 # Fallback if landmarks missing

    image_points = np.array(image_points, dtype="double")

    # Camera internals (Approximation)
    focal_length = frame_width
    center = (frame_width / 2, frame_height / 2)
    camera_matrix = np.array([
        [focal_length, 0, center[0]],
        [0, focal_length, center[1]],
        [0, 0, 1]
    ], dtype="double")
    
    dist_coeffs = np.zeros((4, 1))  # Assuming no lens distortion

    # Solve PnP
    success, rotation_vector, translation_vector = cv2.solvePnP(
        model_points, image_points, camera_matrix, dist_coeffs, flags=cv2.SOLVEPNP_ITERATIVE
    )

    # Convert rotation vector to Euler angles
    rvec_matrix = cv2.Rodrigues(rotation_vector)[0]
    
    # Calculate projection to extract angles
    proj_matrix = np.hstack((rvec_matrix, translation_vector))
    _, _, _, _, _, _, euler_angles = cv2.decomposeProjectionMatrix(proj_matrix)
    
    pitch = euler_angles[0][0]
    yaw = euler_angles[1][0]
    roll = euler_angles[2][0]

    return pitch, yaw, roll