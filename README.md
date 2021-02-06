# WebRobotControl

A simple web interface for controlling your Raspberry Pi robot over the internet or your LAN.
This project is written in Python3, JavaScript and uses the Python library Flask for hosting the web app.

## The Robot

The Robot, I used for testing is based on a Coretec Robotics Tiny 4WD Chassis\* and a kit is available from [Pimoroni](https://shop.pimoroni.com/products/coretec-tiny-4wd-robot-rover) with a Raspberry Pi 4 model B as the brains and an [Adafruit Motor Bonnet](https://www.adafruit.com/product/4280) for controlling the motors.

 \*Full disclosure, I'm (Brian Corteil) the designer of the Coretec Tiny 4WD and receive a royalty for each kit sold by Pimoroni.

 Some other robot kits I would recommend are the 
 
[CamJam Robot kit](https://thepihut.com/collections/camjam-edukit/products/camjam-edukit-3-robotics) Great kit to start with great learning resources available.

Any of the [4tronix](https://shop.4tronix.co.uk/collections/robot-kits) kits.

## Dependencies

### Raspberry Pi OS

Install the latest verson of Raspberry Pi OS to a SD card, follow the instructions on the Raspberry Pi [website](https://www.raspberrypi.org/software/)

### Flask

Flask is a Python library for creating web apps and has a light weight webserver for testing, the web server is not recommended for production use. More details about Flask [here.](https://flask.palletsprojects.com/en/1.1.x/)

you can install flask by using the command line by entering the following

```

pip3 install Flask

```

### your libraries

You will also need to install any libraries you require if it is not part of the standard Raspberry Pi OS install.

## Download the code

Enter the following at the command line to download the project's code

```

git clone https://github.com/OpenPiRobotics/WebRobotControl.git

```

## Modify the appControl.py for your motor controller

You will need to modify the appControl.py to suit your motor controller.

modify line 42 to import your motor controller library
```

from adafruit_motorkit import MotorKit

```
and line 44 to setup your motor controller.
```

mh = MotorKit()

```

you will also need to modify the function set_speeds.

Change the lines 59 to 62. you will need to delete or hash out lines 61, 62, if your controller has only 2 channels
```

mh.motor1.throttle = power_right
mh.motor2.throttle = power_right
mh.motor3.throttle = power_left
mh.motor4.throttle = power_left

```

## Running the Code

Note: It is important not to change the project's folder structure for the code to work.

Run the appControl.py in the root of the project with.
```

python3 appControl.py

```
To start the Web interface use the web browser of your choice and enter the following replacing <ip address> with the IP address of your robot or it's host name and <port> is the port defined on line 165 of appControl.py
 ```
 
 http://<ip address>:<port>
 
 ```
 
 For example when I'm at home to access the web control interface, I would enter 
 ```
 
 testbed.lan:5080
 
 ```
 
 for debuging the web interface press F12
