import math

# Configuration
HEAD_DOWN_PITCH_THRESHOLD = -10.0
HAND_NEAR_FACE_DISTANCE_THRESHOLD = 150
HAND_REFERENCE_POINT_INDEX = 9  # Index of the middle finger mcp
REQUIRED_FRAMES_FOR_DECISION = 10

PERSISTENCE_DICT = {}

def classify_distraction(person_id, pitch_angle, face_landmarks, hand_landmarks):
    """
    Classifies state as 'Focused', 'Sleeping', or 'Phone Use'.
    """
    global PERSISTENCE_DICT

    # 1. Determine Instantaneous State
    instant_status = _determine_instant_status(pitch_angle, face_landmarks, hand_landmarks)

    # 2. Temporal Filtering (Debounce)
    if person_id not in PERSISTENCE_DICT:
        PERSISTENCE_DICT[person_id] = {
            'confirmed_status': 'Focused',
            'consecutive_frames': 0,
            'last_instant_status': 'Focused'
        }

    person_state = PERSISTENCE_DICT[person_id]

    if instant_status == person_state['last_instant_status']:
        person_state['consecutive_frames'] += 1
    else:
        person_state['consecutive_frames'] = 1
        person_state['last_instant_status'] = instant_status

    # Confirm decision after threshold
    if person_state['consecutive_frames'] >= REQUIRED_FRAMES_FOR_DECISION:
        person_state['confirmed_status'] = instant_status

    return person_state['confirmed_status']

def _determine_instant_status(pitch_angle, face_landmarks, hand_landmarks):
    is_head_down = pitch_angle < HEAD_DOWN_PITCH_THRESHOLD

    if not is_head_down:
        return "Focused"

    try:
        face_x = face_landmarks[0]
        face_y = face_landmarks[1]
    except (IndexError, TypeError):
        return "Sleeping"

    # Check hand proximity
    is_hand_near_face = False
    for hand_points_list in hand_landmarks:
        try:
            # Get reference point (Middle Finger MCP)
            ref_hand_point = hand_points_list[HAND_REFERENCE_POINT_INDEX]
            hand_x = ref_hand_point[0]
            hand_y = ref_hand_point[1]

            distance = math.sqrt((hand_x - face_x) ** 2 + (hand_y - face_y) ** 2)

            if distance < HAND_NEAR_FACE_DISTANCE_THRESHOLD:
                is_hand_near_face = True
                break
        except (IndexError, TypeError, ValueError):
            continue

    if is_head_down and is_hand_near_face:
        return "Phone Use"
    else:
        return "Sleeping"