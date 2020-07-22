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
	sheet = createSheet()

	sensor = None
	sensor = W1ThermSensor()

	tCurrent = datetime.now()


	running = True
	while running:
		try:
			tCurrent = datetime.now()
			tNext = tCurrent.replace(microsecond = 0, second = 0, minute = 0) + timedelta(minutes = 10) * (tCurrent.minute // 10 + 1)

			while tCurrent < tNext and running:
				tCurrent = datetime.now()
				time.sleep(0.2)

			temp = sensor.get_temperature()
			print("Current Temperature:", temp, "deg Celcius")
			timeString = datetime.now().strftime("%Y/%m/%d %H:%M")
			row = [timeString, temp]
			print(row)
			sheet.append_row(row, value_input_option='USER_ENTERED')
		except KeyboardInterrupt:
			print("Quitting")
			running = False
		except:
			print("Closing due to error :(")
			running = False


if __name__ == "__main__":
	main()
