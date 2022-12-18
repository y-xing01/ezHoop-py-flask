from unittest.mock import MagicMock

from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory, PNOperationType

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

is_game_running = False
score = 0


def init():
    pubnub.add_listener(GameCallback())
    pubnub.subscribe().channels('game').execute()


def start_game():
    global score
    global is_game_running

    score = 0
    is_game_running = True


def end_game():
    global is_game_running

    is_game_running = False


def detect_motion():
    global score
    global is_game_running

    try:
        while True:
            if is_game_running:
                if GPIO.input(PIR) == 1:
                    print("Motion detected")
                    print("Scored " + score + " in total")
                    score = score + 1
                    pubnub.publish().channel('score').message(score).pn_async(score_callback)
                else:
                    print("No motion detected")
            time.sleep(3)
    except KeyboardInterrupt:
        GPIO.cleanup()



def score_callback(envelope, status):
    # Check whether request successfully completed or not
    if not status.is_error():
        pass  # Message successfully published to specified channel.
    else:
        pass  # Handle message publish error. Check 'category' property to find out possible issue
        # because of which request did fail.
        # Request can be resent using: [status retry];


class GameCallback(SubscribeCallback):
    def presence(self, pubnub, presence):
        pass  # handle incoming presence data

    def status(self, pubnub, status):
        if status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
            pass  # This event happens when radio / connectivity is lost

        elif status.category == PNStatusCategory.PNConnectedCategory:
            pass
            # Connect event. You can do stuff like publish, and know you'll get it.
            # Or just use the connected event to confirm you are subscribed for
            # UI / internal notifications, etc
        elif status.category == PNStatusCategory.PNReconnectedCategory:
            pass
            # Happens as part of our regular operation. This event happens when
            # radio / connectivity is lost, then regained.
        elif status.category == PNStatusCategory.PNDecryptionErrorCategory:
            pass
            # Handle message decryption error. Probably client configured to
            # encrypt messages and on live data feed it received plain text.

    def message(self, pubnub, message):
        # Handle new message stored in message.message
        print(message.message + " " + message.channel)
        if message.channel == "game":
            if message.message == "start":
                start_game()
            else:
                end_game()

    def test_no_motion(self):
        # Set the value of the PIR pin to 0 (simulating no motion)
        GPIO.input = MagicMock(return_value=0)

        # Call the detect_motion() function
        detect_motion()

    def test_detect_motion(self):
        # Set the value of the PIR pin to 1 (simulating motion)
        GPIO.input = MagicMock(return_value=1)

        # Call the detect_motion() function
        detect_motion()

init()
detect_motion()
