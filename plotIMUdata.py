#!/usr/bin/env python

from pylab import * 
import csv

print "fuck you"
close('all')

fileToRead = "IMU.txt"
f1 = open( fileToRead )
#f1 = csv.reader(  open( fileToRead , "rU") )

for a in range(1839):
	f1.readline()   #skip 1st 1839 lines

data = [ this_row for this_row in f1]

pitch = []
gx = []
gy = []
gz = []
az = []
Lx = []
Ly = []
Lz = []
Ltotal = []
time = []

counter = 0
temp = 0
for x in data:
	counter = counter + 1
	#print data[0].split(", ")[17]
	y = x.split(", ")
	Lx.append( float( y[17] ) )
	Ly.append( float( y[18] ) ) #y-linear acceleration
	Lz.append( float( y[19] ) )
	
	az.append( float( y[16] ) )
	
	gx.append( float( y[11] ) )
	gy.append( float( y[12] ) )
	gz.append( float( y[13] ) )
	
	pitch.append( float( y[2] ) )
	Ltotal.append( sqrt( pow( float( y[17] ), 2 ) + pow( float( y[18] ), 2 ) + pow( float( y[19] ), 2 ) ) )
	
	if(  (long(y[23]) - temp ) < 0 ):
		print counter
	
	temp = long( y[23] )
	time.append( long(  y[23] ) )
	




p = plot(time, gz, 'b')	
plt.setp(p,  linewidth=3.0) #thicken up plot
#p = plot(time, Ltotal, 'b')
#plt.setp(p,  linewidth=3.0) #thicken up plot



grid()
yLow = -10
yHigh =10
ylim( [yLow, yHigh] )
xlim( [1596252020655-1000, 1596252020655+44000])
plot( [1596252040850, 1596252040850],[yLow, yHigh],'r')  
plot( [1596252020655, 1596252020655],[yLow, yHigh],'r')  
plot( [1596252055885, 1596252055885], [yLow, yHigh], 'g')
plot( [1596252058291, 1596252058291], [yLow, yHigh], 'r')
plot( [1596252061299, 1596252061299], [yLow, yHigh], 'm')

#plot([1595112245326+50, 1595112245326+50],[-12.5,32.5],'g')

#plot([2484, 2484],[-100,100],'r')
#plot([5150, 5150],[-100,100],'r')
#plot([5850, 5850],[-100,100],'r')
title('Linear Acceleration (m/s^2)')
xlabel('Time (mS)')
plt.show()
