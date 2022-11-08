#********************************************
#**      Program by Chris Bachmann         **
#**   (modifed by Tobias Gerken, 11/3/22) **
#**   for the ISAT 300 Thermocouple Lab    **
#********************************************

#
# Neccesary modules and packages for writing to the cloud
#

from __future__ import print_function
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import os.path
import http.client, urllib
import requests
import time
import datetime
from time import sleep, strftime #, time (this overwrites the time module, removed)

# Packages needed for thermocouple setup
#>>> In this space add the packages that are needed for the thermocouple
# These packages are imported similar to the ones above (check your previous code)

#<<<

#*************************************************
#*            Setting up the LED                 *
#*************************************************
#>>> In the space below add all the code that is needed to set up the 2 LEDs


#<<<
#*************************************************
#*        setting up Google Sheets API           *
#*************************************************

# This SCOPE asks to read and write to Google Sheets.  IF you change it, delete the file token.json and get a new one.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# This line specifies YOUR Google Sheets spreadsheet. You must change the Spreadsheet ID to match your Google Sheet.
SAMPLE_SPREADSHEET_ID = '1j6RHOCMIGHgzPYeUxdflxm2muTyaSzHe3r13pyAvqdI'
RANGE_NAME = 'A2:C2'

# This specifies how the input data should be interpreted.
value_input_option = 'USER_ENTERED'  

# This specifies how the input data should be inserted.
insert_data_option = 'INSERT_ROWS' 


#*************************************
#*   Setting up the thermocouple     *
#*************************************
#>>> In the space below add all the code that is needed to set up the thermocouple


#<<<

#******************************************************************
#*        Connecting to Google Sheets using Google API            *
#*   the first section is for authentication of cyber security    *
#* if the token.json file has expired, it will request a new one  *
#******************************************************************

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

# The below two lines connect to the google service (google sheets in our case and authenticate using the credentials. )
service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()



#***********************************************
#*       reading the thermocouple              *
#*    and writing data to local files          *
#*  AND write data to the cloud                *
#***********************************************

# The below code executes a loop and writes data to the google sheet. 
# 1. Modify the code such that it writes to your google sheet (see above)
# 2. Execute the code and see what values it writes to file. 
# 3. Identify which lines of code set the values that are written to file
# 4. Identify which lines of code write the set values to file. 
# 5. Modify the loop by adding ortions of your thermocouple code such that in each iteration of the loop
#   a. the uncoupled thermocouple is read out
#   b. uncalibrated and calibrated thermocouple temperatures are printed to the screen
#   c. uncalibrated and calibrated thermocouple temperatures are written to a csv file
#   d. calibrated theremocouple temperatures are written to the cloud
#   e. the LEDs are switched ON or OFF depending on the thermocouple temperature condition 

for i in range(10):


# Question: What does this do? 

    values = [
        [
           str(datetime.datetime.now()), str(i), str(i+1)
        ],
        # Additional rows ...
    ]
    body = {
        'values': values
    }


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



    #********************************************************
    #*       Activate LEDs                                  *
    #*    you will change this to make a flashing warning   *
    #*        and vaccine status indicator next week        *
    #*      it is optional to include the LED this week     *
    #********************************************************

    #***************       this is the end of the temperature reading/logging loop         ******************

    # We are adding a small wait period. This becomes important for later.  
    time.sleep(0.1)

print("Run is over.")



# the below code will be important later. We will talk about this during the lab. 
#************************************************************************************
#*               writing the final temperature reading to Google Sheets             *
#*   this is needed because the loop kicks-out just before the Max temp is reached  *
#************************************************************************************

values = [
    [
       str(datetime.datetime.now()), str(i), str(i+1)        ],
        # Additional rows ...
]
body = {
    'values': values
}


#********************************************************
#*    writing final values to Google Sheets             *
#********************************************************  
    
#######  update will change the values within a spreadsheet for use with a guage  ####
result = service.spreadsheets().values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=RANGE_NAME, valueInputOption=value_input_option, body=body).execute()

    
#####  append to add a new row to the spreadsheet for logging over time  ####
result = service.spreadsheets().values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=RANGE_NAME, valueInputOption=value_input_option, body=body).execute()




