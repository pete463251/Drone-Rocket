import RPi.GPIO as GPIO
from time import sleep
import time
import os

current_milli_time = lambda: int(round(time.time() * 1000))  #prints out time in milliseconds

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT, initial=GPIO.LOW)  #pin 11, GPIO0 - SHDNbar
GPIO.setup(13, GPIO.OUT, initial=GPIO.LOW)  #pin 13, GPIO2 - WLATbar
GPIO.setup(15, GPIO.OUT, initial=GPIO.LOW)  #pin 15, GPIO3 - SDI
GPIO.setup(16, GPIO.OUT, initial=GPIO.LOW)  #pin 16, GPIO4 - chip select (CSbar)
GPIO.setup(18, GPIO.OUT, initial=GPIO.LOW)  #pin 18, GPIO5 - CLOCK SCK

GPIO.setup(38, GPIO.OUT, initial=GPIO.LOW)  #pin 38, MOSFET gate for ejection charge
GPIO.setup(40, GPIO.OUT, initial=GPIO.LOW)  #pin 40, MOSFET gate for PWM Controller
GPIO.setup(21, GPIO.OUT, initial=GPIO.LOW)  #pin 19, GPIO12, MOSFET gate for blowing string
GPIO.setup(32, GPIO.OUT, initial=GPIO.LOW)  #pin 32, GPIO 26, MOSFET gate for ignition

def setClock(inp):
	if( inp ):
		GPIO.output(18, GPIO.HIGH)
	else:
		GPIO.output(18, GPIO.LOW)


def setSDI(inp):
	if( inp ):
		GPIO.output(15, GPIO.HIGH)
	else:
		GPIO.output(15, GPIO.LOW)

def setWLAT(inp):
        if( inp ):
                GPIO.output(13, GPIO.HIGH)
        else:
                GPIO.output(13, GPIO.LOW)

def setSHDN(inp):
        if( inp ):
                GPIO.output(11, GPIO.HIGH)
        else:
                GPIO.output(11, GPIO.LOW)

def setCS(inp):
        if( inp ):
                GPIO.output(16, GPIO.HIGH)
        else:
                GPIO.output(16, GPIO.LOW)


def sendBit(inp):
        setSDI(inp)
        setClock(1)
        setClock(0)


# start of increment [0x04] and decrement [0x08] are the same
def sendCommonStartBits():
       #confirm expected starting point for pins
        setCS(1)
        setWLAT(1)
        setClock(0)
        
        sleep(0.01)

        setCS(0) #pull CSbar low
        setWLAT(0)
        
        sendBit(0) #first bit
        sendBit(0) #2nd
        sendBit(0) #3rd
        sendBit(0)


# end of increment and decrement commands are the same
def sendCommonEndBits():
	sendBit(0)
	sendBit(0) #8th bit
	sleep(0.01)
	setWLAT(1)
	setCS(1)

# send command 0000 0100 to increment
def increment():
	
	sendCommonStartBits()

	sendBit(0) #5th
	sendBit(1) #6th

	sendCommonEndBits()

# send command 0000 1000 to decrement
def decrement():
	sendCommonStartBits()

	sendBit(1) #5th bit
	sendBit(0) #6th bit

	sendCommonEndBits()


