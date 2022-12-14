from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory, PNOperationType

import RPi.GPIO as GPIO
import time

channel_motion = 17
channel_vibration = 16

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel_motion, GPIO.IN)
GPIO.setup(channel_vibration, GPIO.IN)

pnconfig = PNConfiguration()

pnconfig.subscribe_key = 'sub-c-143f84aa-6dcf-405a-8805-96edb0b9554f'
pnconfig.publish_key = 'pub-c-c1b540b3-d0af-4fea-8316-245dc2589f12'
pnconfig.user_id = "pi"
pubnub = PubNub(pnconfig)

is_game_running = False

time_motion = 0
time_vibration = 0

count_motion = 0
count_vibration = 0
count_score = 0


def init():
    pubnub.add_listener(GameCallback())
    pubnub.subscribe().channels('game').execute()

    GPIO.add_event_detect(channel_motion, GPIO.BOTH, bouncetime=3000)
    GPIO.add_event_callback(channel_motion, action_callback)

    GPIO.add_event_detect(channel_vibration, GPIO.BOTH, bouncetime=300)
    GPIO.add_event_callback(channel_vibration, action_callback)


def start_game():
    global count_score
    global is_game_running

    count_score = 0
    is_game_running = True


def end_game():
    global is_game_running

    is_game_running = False


# def detect_motion():
#     global score
#     global is_game_running
#
#     try:
#         while True:
#             if is_game_running:
#                 if GPIO.input(channel_vibration) == 1:
#                     print("Motion detected")
#                     print("Scored " + score + " in total")
#                     score = score + 1
#                     pubnub.publish().channel('score').message(score).pn_async(score_callback)
#                 else:
#                     print("No motion detected")
#             time.sleep(1)
#     except KeyboardInterrupt:
#         GPIO.cleanup()


def action_callback(channel):
    global is_game_running
    global count_motion, count_vibration
    global time_motion, time_vibration

    if GPIO.input(channel) == GPIO.input(channel_motion):
        count_motion = count_motion + 1
        time_motion = time.time()
        # print("Motion detected")
    elif GPIO.input(channel) == GPIO.input(channel_vibration):
        count_vibration = count_vibration + 1
        time_vibration = time.time()
        # print("Vibration detected")

    check_score()


def check_score():
    global time_motion, time_vibration

    if time.time() - time_motion > 1:
        time_motion = 0

    if time.time() - time_vibration > 1:
        time_vibration = 0

    if time_motion != 0 and time_vibration != 0:
        print("Scored!")


# def score_callback(envelope, status):
#     # Check whether request successfully completed or not
#     if not status.is_error():
#         pass  # Message successfully published to specified channel.
#     else:
#         pass  # Handle message publish error. Check 'category' property to find out possible issue
#         # because of which request did fail.
#         # Request can be resent using: [status retry];


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


init()
