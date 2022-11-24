from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

import RPi.GPIO as GPIO
import time

PIR = 17

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR, GPIO.IN)

pnconfig = PNConfiguration()

pnconfig.subscribe_key = 'sub-c-143f84aa-6dcf-405a-8805-96edb0b9554f'
pnconfig.publish_key = 'pub-c-c1b540b3-d0af-4fea-8316-245dc2589f12'
pnconfig.user_id = "pi"
pubnub = PubNub(pnconfig)

score = 0


def detect_motion():
    global score

    try:
        while True:
            if GPIO.input(PIR) == 1:
                print("Motion detected")
                score = score + 1
                pubnub.publish().channel('score').message(score).pn_async(score_callback)
            else:
                print("No motion detected")
            time.sleep(3)
    except KeyboardInterrupt:
        GPIO.cleanup()
        score = 0


def score_callback(envelope, status):
    # Check whether request successfully completed or not
    if not status.is_error():
        pass  # Message successfully published to specified channel.
    else:
        pass  # Handle message publish error. Check 'category' property to find out possible issue
        # because of which request did fail.
        # Request can be resent using: [status retry];


detect_motion()