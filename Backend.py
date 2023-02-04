# Modification of TechVidvan hand Gesture Recognizer

# import necessary packages

import cv2
import numpy as np
import mediapipe as mp
import tensorflow as tf
from tensorflow.keras.models import load_model


class HandGesturesDetector:
    def __init__(self) -> None:
        # initialize mediapipe
        self.mpHands = mp.solutions.hands
        self.hands = None
        self.mpDraw = None
        
        # Load the gesture recognizer model
        self.model = load_model('mp_hand_gesture')
        
        # Load class names
        self.f = open('gesturenames/gesture.names', 'r')
        self.classNames = self.f.read().split('\n')
        self.f.close()
        
        self.cap = None
        self.stopFlag = None
        self.init_detector()
        
    def init_detector(self):
        # initialize hands
        self.hands = self.mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7)
        self.mpDraw = mp.solutions.drawing_utils
        
        print(self.classNames)
        
        self.stopFlag = False
        
        # Initialize the webcam
        self.cap = cv2.VideoCapture(0)        
        
    def startDetector(self):
        self.init_detector()
        self.detectGestures()
            
    def stopDetector(self, flag):
        self.stopFlag = flag
        self.cap.release()
        cv2.destroyAllWindows()
            
    def detectGestures(self):
        while True:
            # Read each frame from the webcam
            _, frame = self.cap.read()
            x, y, c = frame.shape
            
            # Flip the frame vertically
            frame = cv2.flip(frame, 1)
            framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Get hand landmark prediction
            result = self.hands.process(framergb)
            # print(result)
    
            className = ''
            
            # Post processings
            if result.multi_hand_landmarks:
                landmarks = []
                for handslms in result.multi_hand_landmarks:
                    for lm in handslms.landmark:
                        # print(id, lm)
                        lmx = int(lm.x * x)
                        lmy = int(lm.y * y)
                        landmarks.append([lmx, lmy])
                        
                    # Drawing landmarks on frames
                    self.mpDraw.draw_landmarks(frame, handslms, self.mpHands.HAND_CONNECTIONS)
                    
                    # Predict gesture
                    prediction = self.model.predict([landmarks])
                    # print(prediction)
                    classID = np.argmax(prediction)
                    className = self.classNames[classID]
                    
            # show the prediction on the frame
            cv2.putText(frame, className, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)
            
            # Show the final output
            cv2.imshow("Output", frame)
            
            if cv2.waitKey(1) == ord('q') or self.stopFlag == True:
                cv2.destroyAllWindows()
                break

