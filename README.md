# rpicar-gamepad
1. Developed on RPi2 with python3.7. Built the Elegoo Smart Robot Car Kit with substitution of a RPi2 for the Arduino Uno that comes with it, using the Adeept Motor HAT (057) on the RPi2 for easy wiring.
2. Control motion of rpicar using gamepad controller. Tested with Logitech Rumblepad2 (USB) and Logitech F710 (wireless). 
3. Webstreaming_module is independent script, using picamera. 
4. Both scripts run from terminal command line.
5. For run on boot, load the rpicar_modularized_F710.py using crontab, but it also runs from terminal or .bashrc.
6. Run the webstreaming_moudle.py using terminal with .bashrc.
7. The Logiech controller 'Back' button exits the rpicar program. 
8. The controller 'Start' button starts the program. 
9. On terminal ctrl+c exits the webstreaming program.
10. The left stick, x-direction rotates the camera servo. 
11. The left stick y-direction moves the left wheels forward and backward. 
12. The right stick y-direction moves the righ wheel.

Enjoy,
mike
