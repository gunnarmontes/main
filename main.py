# main.py
import cv2
import mediapipe as mp
import time
from Squat_feedback import squat_feedback
from feedback_color import draw_feedback  # or keep this in main.py

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# Initialize state
state = 'up'

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the BGR image to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb_frame)

    if results.pose_landmarks:
        # Get feedback for squats (with timing and depth)
        time_feedback, depth_feedback, state = squat_feedback(results.pose_landmarks.landmark, state)

        # Draw feedback with color-coded skeleton
        draw_feedback(frame, results.pose_landmarks, time_feedback, depth_feedback)

    # Show the frame with feedback
    cv2.imshow('Pose Estimation', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
