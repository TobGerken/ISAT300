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

#print(temperature, "C")

import datetime

times = []
temperatures = []

for i in range(100):
    times.append(datetime.datetime.now())
    temperatures.append(thermocouple.temperature)
    
f = open("temperature_measurements.csv", "a")
f.write("Time,Temperature \n")
for i in range(100):
    f.write("{0},{1}\n".format(times[i], temperatures[i]))
f.close()
    
    


    