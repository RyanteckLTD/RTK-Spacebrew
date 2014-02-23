#!/usr/bin/python
#Import stuff
import json
import RPi.GPIO as GPIO
import time
from pySpacebrew.spacebrew import Spacebrew
#str2bool
def str2bool(v):
	return v.lower() in ("yes", "true", "t", "1")
#gogo
print "Booting up robot"
print "Configuring GPIO Pins"
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)

time.sleep(1)
print "Opening Configuration"
config = open('robotConfig.txt','r')
jsonData = json.load(config)

print "Robot loaded as: " + str(jsonData["robotName"])

#print "Checking if wi-fi configuration needs changing"
#if(jsonData['wifi-update']==1):
#	print"Updating Wi-Fi"

print "Attempting to connect to spacebrew server: " + str(jsonData["robotServer"])
brew = Spacebrew(name=str(jsonData["robotName"]), server=str(jsonData["robotServer"]))

#configure motors

brew.addSubscriber("motor1a","boolean")
brew.addSubscriber("motor1b","boolean")
brew.addSubscriber("motor2a","boolean")
brew.addSubscriber("motor2b","boolean")

#define functions
def motor1a(state):
	GPIO.output(17,str2bool(state))
def motor1b(state):
        GPIO.output(18,str2bool(state))
def motor2a(state):
        GPIO.output(22,str2bool(state))
def motor2b(state):
        GPIO.output(23,str2bool(state))


#add listeners
brew.subscribe("motor1a", motor1a)
brew.subscribe("motor1b", motor1b)
brew.subscribe("motor2a", motor2a)
brew.subscribe("motor2b", motor2b)

try:
	brew.start()
	print "Spacebrew Started"
	while 1:
		pass
finally:
	brew.stop()
	GPIO.cleanup()
