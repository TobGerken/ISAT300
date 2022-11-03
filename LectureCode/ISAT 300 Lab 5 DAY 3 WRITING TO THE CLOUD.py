#********************************************
#**      Program by Chris Bachmann         **
#**   for the ISAT 300 Thermocouple Lab    **
#********************************************


from __future__ import print_function
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import os.path
import http.client, urllib
import board
import busio
import digitalio
import requests
import time
import datetime
import adafruit_max31856
from time import sleep, strftime, time



#*************************************************
#*            Setting up the LED                 *
#*************************************************

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
ledPin = 17
GPIO.setup(ledPin, GPIO.OUT)

print("Starting Temperature Log!")
GPIO.output(ledPin, GPIO.LOW)

#*************************************************
#*        setting up Google Sheets API           *
#*************************************************

# This SCOPE asks to read and write to Google Sheets.  IF you change it, delete the file token.json and get a new one.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# This line specifies YOUR Google Sheets spreadsheet. You must change the Spreadsheet ID to match your Google Sheet.
SAMPLE_SPREADSHEET_ID = '1msNhsYEx-PA1BhHheZRpffooX74_ko3zf8mgWfse_60'
RANGE_NAME = 'A2:C2'

# This specifies how the input data should be interpreted.
value_input_option = 'USER_ENTERED'  

# This specifies how the input data should be inserted.
insert_data_option = 'INSERT_ROWS' 


#*************************************
#*   Setting up the thermocouple     *
#*************************************


# create an spi object
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)

# allocate a CS pin and set the direction
cs = digitalio.DigitalInOut(board.D5)
cs.direction = digitalio.Direction.OUTPUT

# create a thermocouple object with the above
thermocouple = adafruit_max31856.MAX31856(spi, cs)


#***********************************************
#*       reading the thermocouple              *
#*    and writing data to local files          *
#*  both .txt and .csv files will be created   *
#***********************************************

while thermocouple.temperature < 30:
    thermocouple = adafruit_max31856.MAX31856(spi, cs)
    # writing to a txt file
    f = open("Kiln.log", "a")
    f.write("\n" + str(datetime.datetime.now()))
    f.write("\t Celcius = ")
    f.write(str(thermocouple.temperature))
    f.write("\t Farhenheit = ")
    f.write(str(thermocouple.temperature * 9 / 5 + 32))
    if thermocouple.temperature > 5.00:
        f.write("\n Warning!!! Approaching Maximum temperature!!!")
    f.close()
    #  writing to a CSV file
    with open("Templog.csv", "a") as log:
        log.write("{0},{1},{2}\n".format(strftime("%Y-%m-%d %H:%M:%S"),str(thermocouple.temperature),str(thermocouple.temperature*9/5+32)))



#******************************************************************
#*        Connecting to Google Sheets using Google API            *
#*   the first section is for authentication of cyber security    *
#* if the token.json file has expired, it will request a new one  *
#******************************************************************
    values = [
        [
           str(datetime.datetime.now()), str(thermocouple.temperature), str((thermocouple.temperature * 9 / 5 + 32))
        ],
        # Additional rows ...
    ]
    body = {
        'values': values
    }

    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    #######  update will change the values within a spreadsheet for use with a guage  ####
    result = service.spreadsheets().values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=RANGE_NAME, valueInputOption=value_input_option, body=body).execute()

    
    #####  append to add a new row to the spreadsheet for logging over time  ####
    result = service.spreadsheets().values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=RANGE_NAME, valueInputOption=value_input_option, body=body).execute()

#******************************************************************************************
#*           HERE IS WHERE THE ACTUAL PRINTING TO THE GOOGLE SHEETS OCCURS                *
#*                                                                                        *
#*       this line will change the values just below the header of your spreadsheet       *
#*   we will use these first lines of the spreadsheet to make a Graphical User Interface  *
#*         showin a guage that changes the temperature reading in real time               *
#******************************************************************************************
    
    result = service.spreadsheets().values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=RANGE_NAME, valueInputOption=value_input_option, body=body).execute()

#*********************************************************************************************
#*   this next line will append your spreadsheet and add lines to the end of the data set    *
#*     we will use all the lines of the spreadsheet to make a Graphical User Interface       *
#*         showin a graph that shows temperature readings over the entire time               *
#*********************************************************************************************

    result = service.spreadsheets().values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=RANGE_NAME, valueInputOption=value_input_option, body=body).execute()

#********************************************************************************************************
#*  we will also print the temperature to the screen so you can see the delay in writing to the cloud   *
#********************************************************************************************************

    print(thermocouple.temperature, "C     ", str((thermocouple.temperature * 9 / 5 + 32)), "F" )
    

#***************       this is the end of the temperature reading/logging loop         ******************



#********************************************************
#*       Activating the LED when the run is done        *
#*    you will change this to make a flashing warning   *
#*        and vaccine status indicator next week        *
#*      it is optional to include the LED this week     *
#********************************************************


print("Run is over.")
GPIO.output(ledPin, GPIO.HIGH)



#************************************************************************************
#*               writing the final temperature reading to Google Sheets             *
#*   this is needed because the loop kicks-out just before the Max temp is reached  *
#************************************************************************************

values = [
    [
       str(datetime.datetime.now()), str(thermocouple.temperature), str((thermocouple.temperature * 9 / 5 + 32))        ],
        # Additional rows ...
]
body = {
    'values': values
}

creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
     if creds and creds.expired and creds.refresh_token:
         creds.refresh(Request())
     else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
with open('token.json', 'w') as token:
    token.write(creds.to_json())

#********************************************************
#*    writing final values to Google Sheets             *
#********************************************************
    
service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()
    
#######  update will change the values within a spreadsheet for use with a guage  ####
result = service.spreadsheets().values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=RANGE_NAME, valueInputOption=value_input_option, body=body).execute()

    
#####  append to add a new row to the spreadsheet for logging over time  ####
result = service.spreadsheets().values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=RANGE_NAME, valueInputOption=value_input_option, body=body).execute()




