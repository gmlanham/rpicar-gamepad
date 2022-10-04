import sys
from gpiozero import Servo
import numpy as np
import time
import os
import inputs
import RPi.GPIO as GPIO
from gpiozero.pins.pigpio import PiGPIOFactory

pwm_A = 0
pwm_B = 0
Motor_A_EN    = 4 #right
Motor_B_EN    = 17 #left

Motor_A_Pin1  = 14
Motor_A_Pin2  = 15
Motor_B_Pin1  = 27
Motor_B_Pin2  = 18

Dir_forward   = 0
Dir_backward  = 1

motor_freq = 100
speed_lower_limit = 1.0
#speed_set = 0
left_speed_set = 0
right_speed_set = 0

def motorStop():#Motor stops
    GPIO.output(Motor_A_Pin1, GPIO.LOW)
    GPIO.output(Motor_A_Pin2, GPIO.LOW)
    GPIO.output(Motor_B_Pin1, GPIO.LOW)
    GPIO.output(Motor_B_Pin2, GPIO.LOW)
    GPIO.output(Motor_A_EN, GPIO.LOW)
    GPIO.output(Motor_B_EN, GPIO.LOW)
    
def init():
    global pwm_A, pwm_B
    GPIO.setup(Motor_A_EN, GPIO.OUT)
    GPIO.setup(Motor_B_EN, GPIO.OUT)
    GPIO.setup(Motor_A_Pin1, GPIO.OUT)
    GPIO.setup(Motor_A_Pin2, GPIO.OUT)
    GPIO.setup(Motor_B_Pin1, GPIO.OUT)
    GPIO.setup(Motor_B_Pin2, GPIO.OUT)    
    motorStop()
    try:
        pwm_A = GPIO.PWM(Motor_A_EN, motor_freq)
        pwm_B = GPIO.PWM(Motor_B_EN, motor_freq)
    except:
        pass

def motor_left(status, direction, left_speed_set):
    if (left_speed_set < 100 and left_speed_set > speed_lower_limit):
        if status == 0: # stop
            GPIO.output(Motor_B_Pin1, GPIO.LOW)
            GPIO.output(Motor_B_Pin2, GPIO.LOW)
            GPIO.output(Motor_B_EN, GPIO.LOW)
        else:
            if direction == Dir_backward:
                GPIO.output(Motor_B_Pin1, GPIO.HIGH)
                GPIO.output(Motor_B_Pin2, GPIO.LOW)
                pwm_B.start(1)
                pwm_B.ChangeDutyCycle(left_speed_set)
            elif direction == Dir_forward:
                GPIO.output(Motor_B_Pin1, GPIO.LOW)
                GPIO.output(Motor_B_Pin2, GPIO.HIGH)
                pwm_B.start(0)
                pwm_B.ChangeDutyCycle(left_speed_set)
            

def motor_right(status, direction, right_speed_set):
    if (right_speed_set < 100 and right_speed_set > speed_lower_limit):
        if status == 0: # stop
            GPIO.output(Motor_A_Pin1, GPIO.LOW)
            GPIO.output(Motor_A_Pin2, GPIO.LOW)
            GPIO.output(Motor_A_EN, GPIO.LOW)
        else:
            if direction == Dir_backward:           
                GPIO.output(Motor_A_Pin1, GPIO.LOW)
                GPIO.output(Motor_A_Pin2, GPIO.HIGH)
                pwm_A.start(1)
                pwm_A.ChangeDutyCycle(right_speed_set)
            elif direction == Dir_forward:          
                GPIO.output(Motor_A_Pin1, GPIO.HIGH)
                GPIO.output(Motor_A_Pin2, GPIO.LOW)
                pwm_A.start(0)
                pwm_A.ChangeDutyCycle(right_speed_set)
