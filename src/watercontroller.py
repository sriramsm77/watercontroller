#!/usr/bin/python
#
# This script is the brain of the water level
#  controller.
#

import RPi.GPIO as GPIO
import time

#
# The main GPIO initialization routine
#
def initGPIOPins():
    #
    # We set the GPIO mode to board, which means
    # that the pin numbers are the actual pin numbers
    # as depicted in the Raspberry PI diagrams
    #
    GPIO.setmode(GPIO.BOARD)

    # Set the input and output modes for all the required
    #  GPIO pins 

    '''
    Pin associations
    ----------------

    LCD connections
    ----------------
    #1   - 3.3v - Vcc for LCD (128x64)
    #9   - GND -  Ground for LCD (128x64)
    #3   - SDA -  SDA input for LCD (128x64)
    #5   - SCL -  SCL for LCD (128x64)

    #29 - Switch to move between pages on the display - IN
        - Need a debounce capacitor circuit
        
    Power supply connections
    ------------------------
    #4  - +5V IN from power source
    #6  - Ground - Connected to Ground of Power supply

    Overhead tank sensor connections
    --------------------------------
    #14 - Tank 0  -  Sensor Input - IN - Pulled High
           - When all other level sensors are Low, a separate LED must be turned ON (RED)
           -  and even one level sensor is High, this must be OFF

    #7  - Tank 25% - Sensor Input - can also be connected to a resistor+LED (GREEN) - IN - Pulled Low
    #11 - Tank 50% - Sensor Input - can also be connected to a resistor+LED (GREEN) - IN - Pulled Low
    #13 - Tank 75% - Sensor Input - can also be connected to a resistor+LED (GREEN) - IN - Pulled Low

    #15 - Overflow - Sensor Input - IN - Pulled Low
           - Error LED will start blinking with buzzer enabled as well 

    #16 - Water inlet - Sensor Input
           - Separate yellow LED will be blinking

    Sump sensor connections
    -----------------------
    #20 - Sump 0  -  Sensor Input - IN - Pulled High
           - When all other level sensors are Low, a separate LED must be turned ON (RED)
           -  and even one level sensor is High, this must be OFF

    #18 - Sump - 50% - Sensor Input - can also be connected to a resistor+LED (GREEN)
    #22 - Sump - 100% - Sensor Input - can also be connected to a resistor+LED (GREEN)
    
    Relay connections
    -----------------
    #31 - Motor Relay
    #32 - Borewell Relay
    #40 - Switch to indicate whether to control Motor OR Borewell
            - ON - BOREWELL - System will use Borewell to pump water 
                    Sump GPIO pins will be made OUT and turned OFF
                    LCD will show Borewell
                    No email will be send when Sump input is low
                    Email will be sent when other errors occur

            - OFF - MOTOR (DEFAULT) - System will use Motor to pump water
                    Sump GPIO pins will be made IN
                    LCD will show Motor
                    Email will be sent when Sump is low and other errors occur

    LED connections
    ---------------
      These LEDs must be controlled by the program (blinking, turning ON/OFF etc)

    #35 - LED for Water flowing (Yellow + Blinking)

      Also send an email when the below happens

    #36 - LED for Error (Tank overflow, Dry run of motor or motor not started) (Red + blinking)
    #37 - LED for low water in overhead tank (RED)
    #38 - LED for low water in sump (RED)

    Buzzer connections
    ------------------
    #33 - Buzzer - turned on when there is an error
    #34 - Ground - Buzzer ground

    '''

    GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

 
if __name__ == '__main__':
    while True:
        if GPIO.input(7):
            print("Pin 7 is HIGH")
        else:
            print("Pin 7 is LOW")
        time.sleep(1)

