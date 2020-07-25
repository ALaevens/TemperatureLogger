#!/usr/bin/env python3

from w1thermsensor import W1ThermSensor
from datetime import datetime
from datetime import timedelta
import time
import gspread
import requests
from oauth2client.service_account import ServiceAccountCredentials

def checkOnline():
    try:
        req = requests.get('http://clients3.google.com/generate_204')
        if req.status_code == 204:
            return True
        else:
            return False
    except:
        return False


def createSheet():
	scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
	creds = ServiceAccountCredentials.from_json_keyfile_name("/home/admin/temperature/creds.json", scope)
	client = gspread.authorize(creds)
	sheet = client.open("Temperature Data").sheet1  # Open the spreadhseet
	return sheet

def main():
	sheet = createSheet() # retrieve reference to the sheet

	sensor = W1ThermSensor() # Open the temperature sensor

	queue = []

	running = True
	while running:
		try:
			tCurrent = datetime.now()

			# Using the current system time, calculate the time of the next 10 minute interval
			tNext = tCurrent.replace(microsecond = 0, second = 0, minute = 0) + timedelta(minutes = 10) * (tCurrent.minute // 10 + 1)

			# Wait until the next measurement should be read
			while tCurrent <= tNext and running:
				tCurrent = datetime.now()
				time.sleep(0.2)

			temp = sensor.get_temperature()
			timeString = datetime.now().strftime("%Y/%m/%d %H:%M")
			print(f"Temperature at [{timeString}]: {temp} deg Celcius")
			
			newRow = [timeString, temp]
			queue.append(newRow)

			# Upload time and temperature to google sheets if there is an internet connection
			if checkOnline():
				for row in queue:
					sheet.append_row(row, value_input_option='USER_ENTERED')

					# hopefully the APIError exception occurs before this line,
					# so any unsent data rows can be retried at 10min intervals
					print(row, " sent to sheet")
					queue.remove(row)

			print("Current Queue:", queue, "\n")

		except KeyboardInterrupt:
			print("Quitting")
			running = False
		except Exception as e:
			print("Exception! Row added to queue to the queue instead")
			print(repr(e))
			print(e)

if __name__ == "__main__":
	main()
