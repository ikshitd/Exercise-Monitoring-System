from tkinter import *
import tkinter.font as tkFont
from PIL import ImageTk, Image
import cv2
import mediapipe as mp
import numpy as np

activity = 0

def calculate_angle(a,b,c):
    a = np.array(a) 
    b = np.array(b) 
    c = np.array(c) 
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle >180.0:
        angle = 360-angle
        
    return angle 

def react(): 
    global activity
    activity = (clicked.get())
    root.destroy()

root = Tk()
root.geometry("1000x900")
root.title("AI Exercise Monitoring System")
root.configure(background="#e9ecef")

text_label = Label(root, text = "WELCOME TO AI EXERCISE MONITORING SYSTEM", fg = "black", bg = "#e9ecef", font="Helvetica 19  bold")
text_label.pack(pady = (15, 15))

img = Image.open("image.png")
img = ImageTk.PhotoImage(img)
img_label = Label(root, image=img)
img_label.pack(pady = (10, 10))

label = Label(root, text = "Select the activity", fg = "black", bg = "#e9ecef" ,font="Helvetica 10")
label.pack(pady =(15, 15))

options = [
    "Curl-Biceps",
    "Push-Ups",
    "Squats", 
    "Sit-Ups"
]

clicked = StringVar()
clicked.set("Curl-Biceps")
helv10 = tkFont.Font(family='Helvetica', size=10)
dropdown = OptionMenu(root, clicked, *options)
dropdown.config(font = helv10)
dropdown.pack(pady = (7,15))
    
button = Button(root, text = "GO", command = react)
button.pack()

root.mainloop()

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

videoinput = activity + ".mp4"

cap = cv2.VideoCapture(0)

# Curl counter variables
counter = 0 
stage = None

## Setup mediapipe instance
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        
        # Recolor image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
      
        # Make detection
        results = pose.process(image)
    
        # Recolor back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        image = cv2.resize(image, (1000, 900)); 
        
        # Extract landmarks
        if(activity == "Curl-Biceps"): 
            try:
                landmarks = results.pose_landmarks.landmark

                # Get coordinates
                shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x ,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

                # Calculate angle
                angle = calculate_angle(shoulder, elbow, wrist)
                # Visualize angle
                cv2.putText(image, str(angle), 
                               tuple(np.multiply(elbow, [640, 480]).astype(int)), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                    )
                # Curl counter logic
                if angle > 130:
                    stage = "down"
                if angle < 80 and stage =='down':
                    stage="up"
                    counter +=1
            except:
                pass
            
        if(activity == "Push-Ups"):
            try:
                landmarks = results.pose_landmarks.landmark

                # Get coordinates
                left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

                # Calculate angle
                right_angle= calculate_angle(right_shoulder, right_elbow, right_wrist)
                left_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)

                angle = (right_angle + left_angle) / 2; 

                # Visualize angle
                cv2.putText(image, str(angle), 
                               tuple(np.multiply(elbow, [640, 480]).astype(int)), 
                               font, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                    )

                # Curl counter logic
                if angle > 130:
                    stage = "up"
                if angle <= 120 and stage =='up':
                    stage="down"
                    counter +=1
                       
            except:
                pass
            
        if(activity == "Squats"): 
            try:
                landmarks = results.pose_landmarks.landmark

                # Get coordinates
                left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
                right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                right_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                right_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

                # Calculate angle
                right_angle= calculate_angle(right_hip, right_knee, right_ankle)
                left_angle = calculate_angle(left_hip, left_knee, left_ankle)

                angle = (right_angle + left_angle) / 2; 

                # Visualize angle
                cv2.putText(image, str(angle), 
                               tuple(np.multiply(elbow, [640, 480]).astype(int)), 
                               font, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                    )

                # Curl counter logic
                if angle > 130:
                    stage = "up"
                if angle <= 90 and stage =='up':
                    stage="down"
                    counter +=1

            except:
                pass
        
        if(activity == "Sit-Ups"): 
            try:
                landmarks = results.pose_landmarks.landmark

                # Get coordinates
                left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                right_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]

                # Calculate angle
                right_angle= calculate_angle(right_shoulder, right_hip, right_knee)
                left_angle = calculate_angle(left_shoulder, left_hip, left_knee)

                angle = (right_angle + left_angle) / 2; 

                # Visualize angle
                cv2.putText(image, str(angle), 
                               tuple(np.multiply(elbow, [640, 480]).astype(int)), 
                               font, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                    )

                # Curl counter logic
                if angle > 120:
                    stage = "down"
                if angle <= 60 and stage =='down':
                    stage="up"
                    counter +=1

            except:
                pass
        
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.rectangle(image, (0,0), (230,73), (245,117,16), -1)
        
        # Counter data
        cv2.putText(image, activity, (15,12), font, 0.5, (0,0,0), 1, cv2.LINE_AA)
        cv2.putText(image, str(counter), (40,60), font, 1, (255,255,255), 2, cv2.LINE_AA)
        
        # Stage data
        cv2.putText(image, 'Stage', (120,12), font, 0.5, (0,0,0), 1, cv2.LINE_AA)
        cv2.putText(image, stage, (120,60), font, 1, (255,255,255), 2, cv2.LINE_AA)
        
        # Render detections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2))               
        
        cv2.imshow('Mediapipe Feed', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
