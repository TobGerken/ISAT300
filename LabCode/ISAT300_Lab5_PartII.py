#********************************************************************
#   importing packages already on the RPi into this Python program  *
#********************************************************************

import board
import busio
import digitalio
import adafruit_max31856

#***********************************
#   Setting up the thermocouple    *
#***********************************
# This part of the code is difficult to understand, but 
# in essence it creates an object that allows phyton to communicate
# with the thermocouple. 

# create an SPI object
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)

# allocate a Chip Select pin for the thermocouple (CS pin) and set the direction
cs = digitalio.DigitalInOut(board.D5)
cs.direction = digitalio.Direction.OUTPUT


# create a thermocouple object with the above
thermocouple = adafruit_max31856.MAX31856(spi, cs)

#*******************************************************************
#**    reading the thermocouple and printing output on screen      *
#*******************************************************************

temperature = thermocouple.temperature

print(temperature, "C")


with open("thermometer.csv","a") as logfile:
    logfile.write("\n" + "Celsius, Fahrenheit")

with x in range(30):
    with open("thermometer.csv","a") as logfile:
        logfile.write("\n{0},{1}".format(str(temperature_C), str(temperature_F)))

#*******************************************************************
#**    turning on the LED if it is too hot or too cold      *
#*******************************************************************
        
    if temperature_C > 25.00 :
        print ("Warning!")
        GPIO.output(GPIO_LED, GPIO.HIGH)
    elif temperature_C <15.00 :
        print ("Warning!")
    else:
        GPIO.output(GPIO_LED, GPIO.LOW)
                  
                  