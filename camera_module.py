from picamera import PiCamera
import time

camera = PiCamera() # start picamera
def rpicamera():
    # camera presets
    camera.resolution = (1920,1080)
    camera.vflip = False
    camera.hflip = True
    camera.iso = 100
    time.sleep(2)
    camera.shutter_speed = camera.exposure_speed
    camera.exposure_mode = 'off'
    g = camera.awb_gains
    camera.awb_mode = 'off'
    camera.awb_gains = g
    camera.framerate = 30
    
    camera.start_preview()
    time.sleep(1)
    #import webstreaming_module
    
def camera_close():
    camera.stop_preview()
    camera.close()
    print('camera.close')
    