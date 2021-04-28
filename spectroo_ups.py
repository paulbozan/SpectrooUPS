#!/usr/bin/env python
import RPi.GPIO as GPIO
import os
import time
from datetime import datetime

GPIO.setmode(GPIO.BCM)
#do not use 
#PIN_FACTORY_RESET_17 = 17 #  factory reset
#PIN_UPS_PICO_1 = 27
#PIN_UPS_PICO_2 = 22

PIN_COM = 25
PIN_POWER_PRESENT = 22
#GPIO_10 True if SpectrooUPS installed
PIN_ID=10
GPIO.setwarnings(False)
GPIO.setup(PIN_POWER_PRESENT, GPIO.IN)
GPIO.setup(PIN_COM, GPIO.IN)
GPIO.setup(PIN_ID, GPIO.IN)
IS_UPS_INSTALLED=False
IS_SHUTDOWN_REQUIRED=False
TS_NOPOWER=None
print "Searching for Spectroo UPS..."
while(True):
	GPIO.setup(PIN_COM, GPIO.IN)
	PIN_COM_VALUE = GPIO.input(PIN_COM)
	PIN_ID_VALUE = GPIO.input(PIN_ID)
	#send 100ms 0 to UPS #watchdog
	GPIO.setup(PIN_COM, GPIO.OUT)
	GPIO.output(PIN_COM,False)
	time.sleep(0.1)

	if IS_UPS_INSTALLED == True and PIN_ID_VALUE == False:
                IS_UPS_INSTALLED=False
                print "Spectroo UPS disconected."

	if PIN_ID_VALUE == False:
		#sleep 5 seconds if UPS is not detected
		time.sleep(5)
		continue

	if IS_UPS_INSTALLED == False and PIN_ID_VALUE == True:
		IS_UPS_INSTALLED=True
	    	print "Spectroo UPS detected."

	if IS_UPS_INSTALLED == True and PIN_COM_VALUE == False:
		IS_SHUTDOWN_REQUIRED=True


	IS_POWER_PRESENT_VALUE = GPIO.input(PIN_POWER_PRESENT)
        if IS_UPS_INSTALLED == True and IS_POWER_PRESENT_VALUE == False:
                if TS_NOPOWER is None:
                        TS_NOPOWER=datetime.now()
                else:
			try:
	                        diff = (datetime.now() - TS_NOPOWER)
        	                diff = diff.total_seconds()
                	        if diff > 20:
                        	        IS_SHUTDOWN_REQUIRED=True
                                	print "Power not present for more than 20 seconds ... shutdown flag true"
			except:
				pass
	else:
		TS_NOPOWER=None
		IS_SHUTDOWN_REQUIRED=False

	#test id shutdown is notified by ups
	GPIO.setup(PIN_COM, GPIO.IN)
	time.sleep(0.2)
	PIN_COM_VALUE = GPIO.input(PIN_COM)
	if PIN_COM_VALUE == False:
    		IS_SHUTDOWN_REQUIRED=True
                print "Shutdown required by UPS."

 	if IS_UPS_INSTALLED == True and IS_SHUTDOWN_REQUIRED == True and IS_POWER_PRESENT_VALUE == False:
	        print "Shutdown procedure started.."
		os.system("shutdown -h now")
		time.sleep(15)
	
