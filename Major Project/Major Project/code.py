import requests
import time
import cv2
import os
import speake3
import pytesseract
import pyttsx3
import json

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
but = 2
GPIO.setup(but,GPIO.IN)

#set GPIO Pins
GPIO_TRIGGER = 3
GPIO_ECHO = 4
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
 
def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance


#set GPIO Pins
GPIO_TRIGGER1 = 27
GPIO_ECHO1 = 17
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER1, GPIO.OUT)
GPIO.setup(GPIO_ECHO1, GPIO.IN)
 
def distance1():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER1, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER1, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO1) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO1) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance






engine = speake3.Speake() # Initialize the speake engine
engine.set('voice', 'en')
engine.set('speed', '150')
engine.set('pitch', '50')
engine.say("WELCOME") #String to be spoken
engine.talkback()


api_key = 'acc_7055d8b2de8746e'
api_secret = 'c8704997ca8e97b2d8dcc02cc67ad3c9'


(W, H) = (None, None)
vs = cv2.VideoCapture(0)
time.sleep(2)

while(1):

    (grabbed, frame) = vs.read()
    cv2.imshow('input',frame)
    cv2.waitKey(1)

    
    
    if(GPIO.input(but)==0):
        tm=0
        while(GPIO.input(but)==0):
            tm=tm+1
            time.sleep(0.3)
            print(tm)
        if(1):
            cv2.imwrite('test.jpg',frame)
            cv2.waitKey(1)
            image_path = 'test.jpg'

            response = requests.post('https://api.imagga.com/v2/tags',
                                     auth=(api_key, api_secret),
                                     files={'image': open(image_path, 'rb')})
            for x in range(3):
              
                obj= ('IDENTIFIED OBJECT IS ' + str(response.json()['result']['tags'][x]['tag']['en']) + '  WITH CONFIDENCE OF '+ str(int(response.json()['result']['tags'][x]['confidence']))+'%' )
                print(obj)
                engine.say(obj)
                engine.talkback()
                time.sleep(3)

          
        else:
            print('OCR:  captured image')
            engine.say("image is captured") #String to be spoken
            engine.talkback()

            print(pytesseract.image_to_string(frame))
            engine.say(pytesseract.image_to_string(frame))
            engine.talkback()
                            
            #cv2.imshow('output',frame)
            #cv2.waitKey(2000)




