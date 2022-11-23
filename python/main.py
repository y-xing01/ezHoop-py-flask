import RPi.GPIO as GPIO
import time

Buzzer = 26
PIR = 17

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR, GPIO.IN)
GPIO.setup(Buzzer, GPIO.OUT)

try:
    while True:
        if GPIO.input(PIR) == 1:
            GPIO.output(Buzzer, GPIO.HIGH)
            print("Motion detected")

        else:
            print("No motion detected")
            GPIO.output(Buzzer, GPIO.LOW)

        time.sleep(3)
except KeyboardInterrupt:
    GPIO.cleanup()
