#!/usr/bin/python
#
# This script is the brain of the water level
#  controller.
#

from enum import Enum
import RPi.GPIO as GPIO
import time

class GPIOPinAssociation(Enum):
    TANK_0_PERCENT     = 14
    TANK_25_PERCENT    = 7
    TANK_50_PERCENT    = 11
    TANK_100_PERCENT   = 13
    TANK_OVERFLOW      = 15
    TANK_WATER_INLET   = 16

    SUMP_0_PERCENT     = 20
    SUMP_50_PERCENT    = 18
    SUMP_100_PERCENT   = 22

    RELAY_MOTOR        = 31
    RELAY_BOREWELL     = 32
    MOTOR_BOREWELL_SWITCH = 40

    LED_WATER_FLOW     = 35
    LED_ERROR          = 36
    LED_TANK_CRITICAL_LOW = 37
    LED_SUMP_CRITICAL_LOW = 38

    BUZZER_SIGNAL      = 33


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
    Raspberry PI Pin associations
    -----------------------------

    LCD connections
    ----------------
    #1   - 3.3v - Vcc for LCD (128x64)
    #6   - GND -  Ground for LCD (128x64)
    #3   - SDA -  SDA input for LCD (128x64)
    #5   - SCL -  SCL for LCD (128x64)

    #29 - Switch to move between pages on the display - IN
        - Need a debounce capacitor circuit
        - One pin of switch to #29 and other to GND (pin #9)
        
    Power supply connections
    ------------------------
    #2 or #4  - +5V IN from power source
    #6  - Ground - Connected to Ground of Power supply

    Overhead tank sensor connections
    --------------------------------
    #14 - Tank 0  -  Ground - Will be always low (sink)
           - When all other tank level sensors are Low, Tank LOW LED must be turned ON (RED)
           -  and even one level sensor is High, the Tank LOW must be turned OFF

    #7  - Tank 25% - Sensor Input - can also be connected to a resistor+LED (GREEN) - IN - Pulled High
    #11 - Tank 50% - Sensor Input - can also be connected to a resistor+LED (GREEN) - IN - Pulled High
    #13 - Tank 100% - Sensor Input - can also be connected to a resistor+LED (GREEN) - IN - Pulled High

    #15 - Overflow - Sensor Input - IN - Pulled High
           - Error LED will start blinking with buzzer enabled as well 

    #19 - Water inlet - Sensor Input
           - Separate yellow LED will be blinking

    Sump sensor connections
    -----------------------
    #20 - Sump 0  -  Sensor Input - IN - Pulled High
           - When all other level sensors are Low, a separate LED must be turned ON (RED)
           -  and even one level sensor is High, this must be OFF

    #21 - Sump - 50% - Sensor Input - can also be connected to a resistor+LED (GREEN)
    #23 - Sump - 100% - Sensor Input - can also be connected to a resistor+LED (GREEN)
    
    Relay connections
    -----------------
    #31 - Motor Relay - OUT - Default Low
    #32 - Borewell Relay - OUT - Default Low
    #40 - Switch to indicate whether to control Motor OR Borewell - IN - Pulled High
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

    #16 - GREEN LED for Tank  25% - OUT - HIGH only when Tank 25% sensor goes HIGH
    #18 - GREEN LED for Tank  50% - OUT - HIGH only when Tank 50% sensor goes HIGH
    #22 - GREEN LED for Tank 100% - OUT - HIGH only when Tank 100% sensor goes HIGH

    #8  - GREEN LED for Sump 50%  - OUT - HIGH only when Sump 50% sensor goes HIGH
    #10 - GREEN LED for Sump 100% - OUT - HIGH only when Sump 100% sensor goes HIGH

    #35 - LED for Water flowing (Yellow + Blinking)

      Also send an email when the below happens

    #36 - LED for Error (Tank overflow, Dry run of motor or motor not started) (Red + blinking)
    #37 - LED for low water in overhead tank (RED) - TANK LOW
    #38 - LED for low water in sump (RED) - SUMP LOW

    Buzzer connections
    ------------------
    #33 - Buzzer - turned on when there is an error
    #30 - Ground - Buzzer ground

    '''

    #
    # Overhead tank sensor connections
    #
    GPIO.setup(TANK_0_PERCENT,      GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(TANK_25_PERCENT,     GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(TANK_50_PERCENT,     GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(TANK_100_PERCENT,    GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    GPIO.setup(TANK_OVERFLOW,       GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(TANK_WATER_INLET,    GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    #
    # Sump sensor connections
    #
    GPIO.setup(SUMP_0_PERCENT,      GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(SUMP_50_PERCENT,     GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(SUMP_100_PERCENT,    GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    #
    # Relay connections
    #
    GPIO.setup(RELAY_MOTOR,         GPIO.OUT, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(RELAY_BOREWELL,      GPIO.OUT, pull_up_down=GPIO.PUD_DOWN)

    #
    # LED connections
    #

    GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

 
if __name__ == '__main__':
    while True:
        if GPIO.input(7):
            print("Pin 7 is HIGH")
        else:
            print("Pin 7 is LOW")
        time.sleep(1)

