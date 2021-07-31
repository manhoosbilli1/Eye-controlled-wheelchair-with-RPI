
#! /usr/bin/env python
from gpiozero import LED, Button
from time import sleep
import os
import cv2
from gaze_tracking import GazeTracking
state = "stop"
button = Button(22)
leftM1 = LED(5)
leftM2 = LED(6)
rightM1 = LED(26)
rightM2 = LED(13)
gaze = GazeTracking()
webcam = cv2.VideoCapture(0)
counter = 0
prevText = ""
prevCounter = 0
print("Program started")
flag = False
while True:
  if button.is_pressed:
    print("now detecting eyes")
    print("align the camera")
    flag = True
  
  while flag==True:
    # We get a new frame from the webcam
    _, frame = webcam.read()

    # We send this frame to GazeTracking to analyze it
    gaze.refresh(frame)

    frame = gaze.annotated_frame()
    text = ""

    if gaze.is_blinking():
      if gaze.is_center():
        counter = counter + 1
      text = "Blinking"
    elif gaze.is_right():
      text = "Looking right"
      state = "right"
      print("going right")
      leftM1.on()
      leftM2.off()
      rightM1.off()
      rightM2.on()

    elif gaze.is_left():
      text = "Looking left"
      state = "left"
      print("going left")
      leftM1.off()
      leftM2.on()
      rightM1.on()
      rightM2.off() 
      
    elif gaze.is_center():
      text = "Looking center"

    if state != "forward" and counter == 3:
      print("car going straight")
      state = "forward"
      leftM1.on()
      leftM2.off()
      rightM1.on()
      rightM2.off()
      counter = 0

    elif state != "stop" and counter == 2:
      print("Stopping now")
      state = "stop"
      leftM1.off()
      leftM2.off()
      rightM1.off()
      rightM2.off()
      counter = 0  
        
    if counter != prevCounter:
      print(counter)
      prevCounter = counter
      
    if text != prevText:
      print(text)
      prevText = text


    cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)

    left_pupil = gaze.pupil_left_coords()
    right_pupil = gaze.pupil_right_coords()
    cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
    cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)

    #cv2.imshow("Demo", frame)

    if cv2.waitKey(1) == 27:
      print("cleaning GPI'os");
      webcam.release()
      cv.destroyAllWindows()
      break
    
    if button.is_pressed:
      flag = False
      break
