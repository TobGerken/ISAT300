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
# << Complete the missing code below (1 line)

# >> Complete the missing code above

#*******************************************************************
#**    reading the thermocouple and printing output on screen      *
#*******************************************************************

# << Complete the missing code below (3 lines)

# >> Complete the missing code above
