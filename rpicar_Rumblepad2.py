#!/usr/bin/env python3
#Python 3.7.3 (default, Jan 22 2021, 20:04:44) 
#[GCC 8.3.0] on linux
#Type "help", "copyright", "credits" or "license()" for more information.

import sys
from gpiozero import Servo
import numpy as np
import time
import os
import inputs #gamepad
import RPi.GPIO as GPIO
from time import sleep
from gpiozero.pins.pigpio import PiGPIOFactory
import camera_module
import usonic_module
import motor_module


print(__file__)
fd = os.open(__file__, os.O_RDWR)
blocking = False
os.set_blocking(fd, blocking) # change the blocking mode
print("Blocking mode changed")
print("Blocking Mode:", os.get_blocking(fd))
#import webstreaming_module
camera_module.rpicamera()
usonic_module.checkdist()
factory = PiGPIOFactory()
#the servo gpio is 3. BOARD pin number is 5,
servo = Servo(3, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000, pin_factory=factory)

servoPIN = 3
print('servoPIN ',servoPIN)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(servoPIN, GPIO.OUT)

print("Start servo mid range.")
servo.value=0
sleep(1)

pads = inputs.devices.gamepads

left_forward  = 1
left_backward = 0

right_forward = 0
right_backward= 1

if len(pads) == 0:
    raise Exception("Couldn't find any Gamepads!")

motor_module.init()

while True:
    try:
        events = inputs.get_gamepad()
        for event in events:
            if event.code == 'BTN_BASE3' and event.state == 0:             #9
                print("exit, break")
                sys.exit()
                break # if CTRL+C is pressed         
#                 camera.stop_preview()
#                 camera.stop_recording()
#                 camera.close() # stop camera
#                 time.sleep(0.01)
            if event.code == 'BTN_BASE4' and event.state == 0:             #10
                usonic_module.checkdist()
                time.sleep(0.01)
            if event.code == 'ABS_RZ':                                     #axis3 Rstick Vert
                right_speed_set = int(abs(event.state-128)/1.28)           #action: set right motor speed
                if event.state-128 < -70:
                    motor_module.motor_right(1, right_forward, right_speed_set)
                elif event.state-128 > 70:
                    motor_module.motor_right(1, right_backward, right_speed_set)
                else:
                    motor_module.motorStop()
            if event.code == 'ABS_X': #camera servo, axis2 Lstick Horiz
                deltaX=(event.state-128)/128
                if abs((event.state-128)/128) > 0.02:                
                    servo.value= -deltaX
                    time.sleep( 0.01 )
            if event.code == 'ABS_Y':                                      #axis1 Lstick Vert
                left_speed_set = int(abs(event.state-128)/1.28)            #action: set left motor speed
                if (event.state-128 < -70):
                    motor_module.motor_left(1, left_forward, left_speed_set)
                elif event.state-128 > 70:
                    motor_module.motor_left(1, left_backward, left_speed_set)
                else:
                    motor_module.motorStop()                                            #this stops motors after each time cycle, when commented-out continous motor action allowed.
    except KeyboardInterrupt:
        camera_module.camera_close()
        motor_module.motorStop() 
        print("break on CTRL+c")
        break # if CTRL+C is pressed

def destroy():
    motor_module.motorStop()
    GPIO.cleanup()             # Release resource



