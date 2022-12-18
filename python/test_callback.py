from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory, PNOperationType
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

import time
import RPi.GPIO as GPIO
import time

# GPIO SETUP
channel = 16
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)


def callback(channel):
    input_value = GPIO.input(channel)
    print("Input value:", input_value)
    if input_value:
        print("Vibration Detected !")
    else:
        print("Vibration Detected !")


# Let us know when the pin goes high or low
GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=300)
GPIO.add_event_callback(channel, callback)

# Infinite Loop
while True:
    time.sleep(1)


    def test_callback():
        # Test the callback function to ensure that it prints the expected output
        callback(16)
        callback(17)


    def test_infinite_loop():
        # Test the infinite loop to ensure that it does not throw any errors
        while True:
            time.sleep(1)


    def main():
        # Set up the GPIO channel and event detection
        channel = 16
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(channel, GPIO.IN)
        GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=300)
        GPIO.add_event_callback(channel, callback)

        # Run the tests
        test_callback()
        test_infinite_loop()


    if name == "main":
        main()

pnconfig = PNConfiguration()

pnconfig.subscribe_key = 'sub-c-143f84aa-6dcf-405a-8805-96edb0b9554f'
pnconfig.publish_key = 'pub-c-c1b540b3-d0af-4fea-8316-245dc2589f12'
pnconfig.user_id = "user"
pubnub = PubNub(pnconfig)


def my_publish_callback(envelope, status):
    # Check whether request successfully completed or not
    if not status.is_error():
        pass  # Message successfully published to specified channel.
    else:
        pass  # Handle message publish error. Check 'category' property to find out possible issue
        # because of which request did fail.
        # Request can be resent using: [status retry];


class MySubscribeCallback(SubscribeCallback):
    def presence(self, pubnub, presence):
        pass  # handle incoming presence data

    def status(self, pubnub, status):
        if status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
            pass  # This event happens when radio / connectivity is lost

        elif status.category == PNStatusCategory.PNConnectedCategory:
            # Connect event. You can do stuff like publish, and know you'll get it.
            # Or just use the connected event to confirm you are subscribed for
            # UI / internal notifications, etc
            pass
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
        print(message.message)


pubnub.add_listener(MySubscribeCallback())
pubnub.subscribe().channels('score').execute()