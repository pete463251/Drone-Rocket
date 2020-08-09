#!/usr/bin/env python

from pylab import * 
import csv

print "hello"

f1 = csv.reader(  open( "IMU.txt" , "rU") )
data = [ this_row for this_row in f1]
print size(data)
	
temp = []
lz = []
az = []
tab = 12

for index, x in enumerate(data):
	#print index, x
	if( index > 2):
		#print x[20]
		temp.append( x[7] )
		lz.append( x[tab] )

	
			
time = range( len( lz ) )			
	
print lz
	
p = plot(time, lz, 'b')		

plt.setp(p,  linewidth=3.0)
grid()
ylim([-50, 50])
#plt.show()

 
 
 #need to do: sudo pigpio before running this
import RPi.GPIO as GPIO
import time 
from time import sleep
import pigpio

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

#GPIO.setup(18, GPIO.OUT)

frequencyHz = 50 #50Hz = 20mS period
#p = GPIO.PWM(18, frequencyHz)
pwm = pigpio.pi()
pwm.set_mode(18, pigpio.OUTPUT)
pwm.set_PWM_frequency(18, 50)

counts = 200
for x in range(counts):
        value_DC = 200*(5 + 5.*x/counts)
        print(value_DC)
        pwm.set_servo_pulsewidth(18,  value_DC )
        sleep(0.01)

pwm.set_PWM_dutycycle(18, 0)
pwm.set_PWM_frequency(18, 0)


