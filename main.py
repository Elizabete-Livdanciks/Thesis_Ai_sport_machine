import mediapipe as mp
import cv2
import tkinter as tk
from tkinter import filedialog, messagebox

# Function to open file dialog and get video file path
def get_file_path():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    return file_path

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:

    # Get video file path from user
    video_file_path = get_file_path()

    # Load video
    cap = cv2.VideoCapture(video_file_path)

    while cap.isOpened():
        # Read frame from video
        success, image = cap.read()
        if not success:
            break
    
        # Get frame dimensions
        image_height, image_width, _ = image.shape
        
        # Convert frame from BGR to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Analyze pose in frame
        results = pose.process(image_rgb)

        # If pose is detected, provide recommendations
        if results.pose_landmarks:

            # Key points
            landmarks = results.pose_landmarks.landmark

            # Head detection
            nose_x = landmarks[mp_pose.PoseLandmark.NOSE.value].x * image_width
            nose_y = landmarks[mp_pose.PoseLandmark.NOSE.value].y * image_height

            # Elbow detection
            left_elbow_x = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x * image_width
            left_elbow_y = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y * image_height
            right_elbow_x = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x * image_width
            right_elbow_y = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y * image_height

            # Knee detection
            left_knee_x = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x * image_width
            left_knee_y = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y * image_height


            # Shoulder detection
            left_shoulder_x = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x * image_width
            left_shoulder_y = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y * image_height
            right_shoulder_x = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x * image_width
            right_shoulder_y = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y * image_height

            # Hip detection
            hip_x = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x * image_width
            hip_y = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y * image_height

            # Foot detection
            left_foot_x = landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX].x * image_width
            left_foot_y = landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX].y * image_height
            right_foot_x = landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX].x * image_width
            right_foot_y = landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX].y * image_height

            # Mistake: Hips too low -> Raise your hips
            if hip_y < (left_shoulder_y + right_shoulder_y) / 2:
                cv2.putText(image, 'Lower your hips', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)

            # Mistake: Hips too high -> Lower your hips
            if hip_y > (left_shoulder_y + right_shoulder_y) / 2:
                cv2.putText(image, 'Upper your hips', (50, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)


            if left_elbow_x < left_shoulder_x or left_elbow_x > right_shoulder_x or right_elbow_x > right_shoulder_x or right_elbow_x < left_shoulder_x:
                cv2.putText(image, 'Move elbows straight under the shoulders', (50, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)

                # Mistake: Head is up -> Put your head down
            if landmarks[mp_pose.PoseLandmark.NOSE.value].y < landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y and landmarks[mp_pose.PoseLandmark.NOSE.value].y < landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y:
                cv2.putText(image, 'look at the floor, your neck and head should be in one line', (50, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)

    
        # Display the frame
            cv2.imshow('Pose Estimation', image)

        # Wait for 'q' key to be pressed to exit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

# Release resources
    cap.release()
    