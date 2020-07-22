#!/usr/bin/env python3

from w1thermsensor import W1ThermSensor
from datetime import datetime
from datetime import timedelta
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def createSheet():
	scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
	creds = ServiceAccountCredentials.from_json_keyfile_name("/home/admin/temperature/creds.json", scope)
	client = gspread.authorize(creds)
	sheet = client.open("Temperature Data").sheet1  # Open the spreadhseet
	return sheet

def main():
	sheet = createSheet() # retrieve reference to the sheet

	sensor = W1ThermSensor() # Open the temperature sensor

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
			
			# Upload time and temperature to google sheets
			row = [timeString, temp]
			sheet.append_row(row, value_input_option='USER_ENTERED')
		except KeyboardInterrupt:
			print("Quitting")
			running = False
		except Exception as e:
			print("Closing due to error :(")
			running = False
			print(repr(e))
			print(e)
			print(e.args)

if __name__ == "__main__":
	main()
