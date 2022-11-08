#********************************************************************
#   importing packages already on the RPi into this Python program  *
#********************************************************************

import board
import busio
import digitalio
import adafruit_max31856
import time
import RPi.GPIO as GPIO

#****************************************************************
#*      Setting up the LED to be controlled by GPIO pin 17      *
#****************************************************************

GPIO.setmode(GPIO.BCM)
GPIO_LED = (17)
GPIO.setup(GPIO_LED, GPIO.OUT)

GPIO.output(GPIO_LED, GPIO.LOW)

#***********************************
#   Setting up the thermocouple    *
#***********************************

# create an SPI object
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)

# allocate a Chi p Select pin for the thermocouple (CS pin) and set the direction
cs = digitalio.DigitalInOut(board.D5)
cs.direction = digitalio.Direction.OUTPUT

# create a thermocouple object with the above
thermocouple = adafruit_max31856.MAX31856(spi, cs)

#******************************************************************
#**    making a loop to continuously read the thermocouple        *
#**           until a set temperature is reached                  *
#******************************************************************

while thermocouple.temperature < 25:
    
#*******************************************************************
#**    reading the thermocouple and printing output on screen      *
#*******************************************************************

    print(thermocouple.temperature, "C")
    print(str(thermocouple.temperature * 9 / 5 + 32), "F")
    
    
#********************************************************************
#**     Making LED flash warning as Max Temp approaches             *
#**    and instructing LED to stay on if Max Temp exceeded          *
#********************************************************************
    if thermocouple.temperature > 10 :
        print ("Max Temp Exceeded!!!  Vaccine is RUINED!!!")
        GPIO.output(GPIO_LED, GPIO.HIGH)
    elif thermocouple.temperature > 5 :
        print ("Max Temp Approaching!!  Add more ice!!!")
        GPIO.output(GPIO_LED, GPIO.HIGH)
        time.sleep (0.20)
        GPIO.output(GPIO_LED, GPIO.LOW)
        time.sleep (0.20)
        GPIO.output(GPIO_LED, GPIO.HIGH)
        time.sleep (0.20)
        GPIO.output(GPIO_LED, GPIO.LOW)
        time.sleep (0.20)
        GPIO.output(GPIO_LED, GPIO.HIGH)
        time.sleep (0.20)
        GPIO.output(GPIO_LED, GPIO.LOW)
    else:
        GPIO.output(GPIO_LED, GPIO.LOW)
        