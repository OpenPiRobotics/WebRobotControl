"""
	Raspberry Pi web robot controller

	Reused the motor functions from the Tiny 4WD code example from Approximate Engineering
	based on code from Brian Corteil as modified by Emma Norling
	subsequently modified by Tom Oinn to add dummy functions when no explorer hat is available.
"""
import RPi.GPIO as GPIO
from flask import Flask, render_template, jsonify, request
from time import sleep
import board
import busio

# Create the I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)

# define variables

robotStatus = {'motor1': 0, 'motor2': 0}
lastAction = "stop"

# motor control functions

# You will need to modify the from/import for your motor controller and the functions
# set_speeds
# stop_motors

try:
    """
    Attempt to import the Adafruit HAT library. If this fails, because we're running somewhere
    that doesn't have the library, we create dummy functions for set_speeds and stop_motors which
    just print out what they'd have done. This is a fairly common way to deal with hardware that
    may or may not exist! Obviously if you're actually running this on one of Brian's robots you
    should have the Explorer HAT libraries installed, this is really just so I can test on my big
    linux desktop machine when coding.
    """

    from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor

    # define an Adafruit Motor kit object

    from adafruit_motorkit import MotorKit

    mh = MotorKit()
    print('Adafruit Motor kit library available.')


    def set_speeds(power_left, power_right):
        """
        As we have an motor hat, we can use the motors

        :param power_left:
            Power to send to left motor
        :param power_right:
            Power to send to right motor, will be inverted to reflect chassis layout
        """
        print(power_left, power_right)

        mh.motor1.throttle = power_right
        mh.motor2.throttle = power_right
        mh.motor3.throttle = power_left
        mh.motor4.throttle = power_left


    def stop_motors():
        """
        As we have an motor hat, stop the motors using set_speeds
        """

        set_speeds(0, 0)


except ImportError:

    print('No Adafruit Motor HAT library available, using dummy functions.')


    def set_speeds(power_left, power_right):
        """
        No motor hat - print what we would have sent to it if we'd had one.
        """
        print('Left: {}, Right: {}'.format(power_left, power_right))
        sleep(0.1)


    def stop_motors():
        """
        No motor hat, so just print a message.
        """
        print('Motors stopping')

def mixer(yaw, throttle, max_power = 1):

    """
    Mix a pair of joystick axes, returning a pair of wheel speeds. This is where the mapping from
    joystick positions to wheel powers is defined, so any changes to how the robot drives should
    be made here, everything else is really just plumbing.

    :param yaw:
        Yaw axis value, ranges from -1.0 to 1.0
    :param throttle:
        Throttle axis value, ranges from -1.0 to 1.0
    :param max_power:
        Maximum speed that should be returned from the mixer, defaults to 100
    :return:
        A pair of power_left, power_right integer values to send to the motor driver
    """

    print(f"Yaw = {yaw} Throttle = {throttle}")

    left = throttle + yaw
    right = throttle - yaw
    scale = float(max_power) / max(1, abs(left), abs(right))
    return left * scale, right * scale


# define the Web app

app = Flask(__name__)

# setup the GPIOs pins used

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Display back light pin, this could be a LED instead
display = 26

# Define display pin as output
GPIO.setup(display, GPIO.OUT)

# and turn it off
GPIO.output(display, GPIO.LOW)


# Web routes ie. index.html and the setting motor speeds ie. /motors/forward

# site index page

@app.route("/")
def index():
    templateData = {
        'title': 'Remote Pi Noon',
    }
    return render_template('index2.html', **templateData)


# motor control is /motor then the action /forward or /left

@app.route("/<deviceName>/<action>/")
def action(deviceName, action):
    global robotStatus, lastAction

    if deviceName == 'motor' and lastAction != action:
        print(f"action: {action}")
        if action == "off":
            robotStatus["motor1"] = 0
            robotStatus["motor2"] = 0
            stop_motors()

        if action == "forward":
            robotStatus["motor1"] = 1
            robotStatus["motor2"] = 1

        if action == "backward":
            robotStatus["motor1"] = -1
            robotStatus["motor2"] = -1

        if action == "left":
            robotStatus["motor1"] = -1
            robotStatus["motor2"] = 1

        if action == "right":
            robotStatus["motor1"] = 1
            robotStatus["motor2"] = -1

        if action == "mixer":
            x = float(request.args.get('x'))
            y = float(request.args.get('y'))

            x, y = mixer(x, y)

            robotStatus["motor1"] = x;
            robotStatus["motor2"] = y;

            action = f"{action} x{x} y{y}"

        # set motor speeds
        set_speeds(robotStatus["motor1"], robotStatus["motor2"])

    lastAction = action
    print(f"last action: {lastAction}")

    return jsonify(robotStatus)


# WARNING if being run any where apart from your private home
# LAN debug should be switched off by setting debut to False
# the port setting is the value required for port forwarding

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5080, debug=False)  # debug switched off and port 5080
