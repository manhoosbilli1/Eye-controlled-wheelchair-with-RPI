#! /usr/bin/env python
from gpiozero import LED, Button
from time import sleep
import os
import cv2
from gaze_tracking import GazeTracking

button = Button(22)

leftM1 = LED(5)
leftM2 = LED(6)
rightM1 = LED(26)
rightM2 = LED(13)
gaze = GazeTracking()
webcam = cv2.VideoCapture(0)
counter = 0
prevText = ""
print("Program started")
flag = False
try:
  while True:
    # We get a new frame from the webcam
    _, frame = webcam.read()

    # We send this frame to GazeTracking to analyze it
    gaze.refresh(frame)

    frame = gaze.annotated_frame()
    text = ""

    if gaze.is_blinking():
    text = "Blinking"
    elif gaze.is_right():
    text = "Looking right"
    elif gaze.is_left():
    text = "Looking left"
    elif gaze.is_center():
    text = "Looking center"

    if gaze.is_center() and gaze.is_blinking():
    counter = counter + 1

    if gaze.is_left() and gaze.is_blinking():
    print("going left")
    leftM1.off()
    leftM2.on()
    rightM1.on()
    rightM2.off()          

    if gaze.is_right() and gaze.is_blinking():
    print("going right")
    leftM1.on()
    leftM2.off()
    rightM1.off()
    rightM2.on()       

    if counter == 3:
    print("car going straight")
    leftM1.on()
    leftM2.off()
    rightM1.on()
    rightM2.off()
    counter = 0

    if text != prevText:
    print(text)
    prevText = text


    cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)

    left_pupil = gaze.pupil_left_coords()
    right_pupil = gaze.pupil_right_coords()
    cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
    cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)

    cv2.imshow("Demo", frame)
    if button.is_pressed:
    flag = False

    if cv2.waitKey(1) == 27:
    print("cleaning GPI'os");
    webcam.release()
    cv.destroyAllWindows()
    break
except:
    print("Exiting program");
    
finally:
    print("cleaning GPI'os");
    webcam.release()
    cv.destroyAllWindows()

