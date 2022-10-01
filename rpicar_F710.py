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
#from webstreaming_module import *
import usonic_module
import motor_module

#import webstreaming_module
#import camera_module
#camera_module.rpicamera()
usonic_module.checkdist()

print(__file__)
fd = os.open(__file__, os.O_RDWR)
blocking = False
os.set_blocking(fd, blocking) # change the blocking mode
print("Blocking mode changed")
print("Blocking Mode:", os.get_blocking(fd))

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
            #print(event.code, event.state)
            if event.code == 'BTN_SELECT' and event.state == 0:             #9
                print("exit, break")
                sys.exit()
                break # if CTRL+C is pressed         
#                 camera.stop_preview()
#                 camera.stop_recording()
#                 camera.close() # stop camera
#                 time.sleep(0.01)
            if event.code == 'BTN_START' and event.state == 0:             #10
                print('streaming browser 192.168.0.11')
                usonic_module.checkdist()
                time.sleep(0.01)
            if event.code == 'ABS_RY':                                     #axis3 Rstick Vert                
                #print(('RY',(event.state-327.68)/327.68))
                right_speed_set = (abs(event.state)/327.68)          #action: set right motor speed
                if ((event.state-327.68)/327.68 < -50):
                    motor_module.motor_right(1, right_forward, right_speed_set)
                elif ((event.state-327.68)/327.68 > 50):
                    motor_module.motor_right(1, right_backward, right_speed_set)
                else:
                    motor_module.motorStop()
            if event.code == 'ABS_X': #camera servo, axis2 Lstick Horiz
                deltaX=(event.state)/32768
                #print('event.state=',event.state,'deltaX=',deltaX)
                #time.sleep( 0.1 )
                #print(event.state)
                #time.sleep( 0.1 )
                #print('ABS_X',event.state)
                print('-deltaX',-deltaX)
                if abs(deltaX)> 0.1:                  
                    servo.value= -deltaX
                    time.sleep( 0.01 )
            if event.code == 'ABS_Y':                                      #axis1 Lstick Vert
                #print('ABS_Y',event.state)
                #print(('Y',(event.state-327.68)/327.68))
                left_speed_set = (abs(event.state)/327.68)            #action: set left motor speed
                #print(left_speed_set)
                if ((event.state-327.68)/327.68 < -50):
                    motor_module.motor_left(1, left_forward, left_speed_set)
                elif ((event.state-327.68)/327.68 > 50):
                    motor_module.motor_left(1, left_backward, left_speed_set)
                else:
                    motor_module.motorStop()                                            #this stops motors after each time cycle, when commented-out continous motor action allowed.
            
    except KeyboardInterrupt:
        #camera_module.camera_close()
        motor_module.motorStop() 
        print("break on CTRL+c")
        break # if CTRL+C is pressed

def destroy():
    motor_module.motorStop()
    GPIO.cleanup()             # Release resource



