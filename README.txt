Alexander Laevens, July 22, 2020

Simple temperature logger.

Stays running in the background to upload data to a google sheets spreadsheet
every 10 minutes, on the minute.

Requirements:

Requires a personal google credentials file (creds.json) to properly function.
-> https://www.youtube.com/watch?v=cnPlKLEGR7E (0:00 - 3:55)

Requires pip packages: gspread, oauth2client, w1thermsensor
-> pip3 install gspread
-> pip3 install oauth2client
-> pip3 install w1thermsensor

Requires a properly attatched One-Wire capable temperature sensor
such as the DS18B20


Suggested:
	Configure the script to start automatically, such as with a CronTab service
	at boot time
