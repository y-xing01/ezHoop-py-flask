#!/user/bin/python
import RPi.GPIO as GPIO
import time

#GPIO SETUP
channel = 16
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)

def callback(channel):
    if GPIO.input(channel):
        print("Vibration Detected !")
    else:
        print("Vibration Detected !")

#Let us know when the pin goes high or low
GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=300)
GPIO.add_event_callback(channel, callback)

#Infinite Loop
while True:
    time.sleep(1)