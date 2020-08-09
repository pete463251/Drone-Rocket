# Simple Adafruit BNO055 sensor reading example.  Will print the orientation
# and calibration data every second.
#
# Copyright (c) 2015 Adafruit Industries
# Author: Tony DiCola
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
import logging
import sys
import time

from Adafruit_BNO055 import BNO055

f = open("IMU.txt", "a")
f.write("-------------------------")
f.write(time.strftime("      %a %d-%m-%Y @ %H:%M:%S") )
f.write("\n")

current_milli_time = lambda: int(round(time.time() * 1000))  #prints out time in milliseconds; current_milli_time()


# Create and configure the BNO sensor connection.  Make sure only ONE of the
# below 'bno = ...' lines is uncommented:
# Raspberry Pi configuration with serial UART and RST connected to GPIO 18:
bno = BNO055.BNO055(serial_port='/dev/ttyAMA0', rst=6)
# BeagleBone Black configuration with default I2C connection (SCL=P9_19, SDA=P9_20),
# and RST connected to pin P9_12:
#bno = BNO055.BNO055(rst='P9_12')



###### This section changes the accelerometer range to be 16G #######
### based on https://forums.adafruit.com/viewtopic.php?f=1&t=85097
### Notes:
### 0x08 = BNO055_ACC_CONFIG_ADDR
### 0x07 = BNO055_PAGE_ID_ADDR
### default accelerometer setting is 4G, last two bits of register 08 is 01
### change to last two bits being 11. Data sheet here, look for Table 3-8
### https://cdn-shop.adafruit.com/datasheets/BST_BNO055_DS000_12.pdf 
###
time.sleep(0.1)
savePageID = bno._read_byte(0x07)
time.sleep(0.1)
bno._write_byte(0x07, 0x01)     
time.sleep(0.1)
print bno._read_byte(0x07)      
time.sleep(0.1)
print bno._read_byte(0x08)   
time.sleep(0.1)
bno._write_byte(0x08, 0xFF)       
time.sleep(0.1)
print bno._read_byte(0x08) 
time.sleep(0.1)
print "got"
bno._write_byte(0x07, savePageID & 0xFF)
print "here"
######## End section on changing accelerometer range #########


# Enable verbose debug logging if -v is passed as a parameter.
if len(sys.argv) == 2 and sys.argv[1].lower() == '-v':
    logging.basicConfig(level=logging.DEBUG)

# Initialize the BNO055 and stop if something went wrong.
if not bno.begin():
    raise RuntimeError('Failed to initialize BNO055! Is the sensor connected?')
    f.write('Failed toinitialize BNO055')

# Print system status and self test result.
status, self_test, error = bno.get_system_status()
print('System status: {0}'.format(status))
f.write('System status: {0}'.format(status))
print('Self test result (0x0F is normal): 0x{0:02X}'.format(self_test))
f.write('Self test result (0x0F is normal): 0x{0:02X}'.format(self_test))
f.write('\n')

# Print out an error if system status is in error mode.
if status == 0x01:
    print('System error: {0}'.format(error))
    print('See datasheet section 4.3.59 for the meaning.')
    f.write('System error: {0}'.format(error))
    f.write('See datasheet section 4.3.59 for the meaning.')

# Print BNO055 software revision and other diagnostic data.
sw, bl, accel, mag, gyro = bno.get_revision()
print('Software version:   {0}'.format(sw))
print('Accelerometer ID:   0x{0:02X}'.format(accel))
print('Magnetometer ID:    0x{0:02X}'.format(mag))
print('Gyroscope ID:       0x{0:02X}\n'.format(gyro))

print('Reading BNO055 data, press Ctrl-C to quit...')

print('starting 60 seconds with no logging')
# for about 60 seconds, print out data but don't log
counter = 0
for n in range(30):
    # Read the Euler angles for heading, roll, pitch (all in degrees).
    heading, roll, pitch = bno.read_euler()
    # Read the calibration status, 0=uncalibrated and 3=fully calibrated.
    sys, gyro, accel, mag = bno.get_calibration_status()
    # Print everything out.
    print('Heading={0:0.2F} Roll={1:0.2F} Pitch={2:0.2F}\tSys_cal={3} Gyro_cal={4} Accel_cal={5} Mag_cal={6}'.format(
    		heading, roll, pitch, sys, gyro, accel, mag))

    time.sleep(3)


print('starting 5 minutes of logging')
# now for 5 minutes, log data. Should be sufficient time to spin up and launch
counter = 0
while True:
    # Read the Euler angles for heading, roll, pitch (all in degrees).
    heading, roll, pitch = bno.read_euler()
    # Read the calibration status, 0=uncalibrated and 3=fully calibrated.
    sys, gyro, accel, mag = bno.get_calibration_status()
    # Print everything out.

    if( counter == 450): #every 40 cycles is about 1 second 
	    counter = 0
	    #print('Heading={0:0.2F} Roll={1:0.2F} Pitch={2:0.2F}\tSys_cal={3} Gyro_cal={4} Accel_cal={5} Mag_cal={6}'.format(
            #	  heading, roll, pitch, sys, gyro, accel, mag))
	    f.close()                       #every second close and reopen file to ensure it gets saved
	    f = open("IMU.txt", "a")
		
    else:
	counter = counter + 1

    if( counter == 1200 ):
	break
    # Other values you can optionally read:
    # Orientation as a quaternion:
    #x,y,z,w = bno.read_quaterion()
    # Sensor temperature in degrees Celsius:
    temp_c = bno.read_temp()
    #print('Temperature = {0:0.2F}'.format(temp_c) )
    # Magnetometer data (in micro-Teslas):
    mx,my,mz = bno.read_magnetometer()
    #print('Magnetometer x,y,z = {0:0.2F}, {1:0.2F}, {2:0.2F}'.format(x,y,z) )
    # Gyroscope data (in degrees per second):
    gx,gy,gz = bno.read_gyroscope()
    #print('Gyroscope x,y,z = {0:0.2F}, {1:0.2F}, {2}'.format(x,y,z) )
    # Accelerometer data (in meters per second squared):
    ax,ay,az = bno.read_accelerometer()
    #print('Accelerometer x,y,z = {0:0.2F}, {1:0.2F}, {2}'.format(x,y,z) )
    # Linear acceleration data (i.e. acceleration from movement, not gravity--
    # returned in meters per second squared):
    lx,ly,lz = bno.read_linear_acceleration()
    #print('Linear Acceleration x,y,z = {0:0.2F}, {1:0.2F}, {2}'.format(x,y,z) )
    # Gravity acceleration data (i.e. acceleration just from gravity--returned
    # in meters per second squared):
    grx,gry,grz = bno.read_gravity()
    #print('Gravity x,y,z = {0:0.2F}, {1:0.2F}, {2}'.format(x,y,z) )

    f.write('{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11}, {12}, {13}, {14}, {15}, {16}, {17}, {18}, {19}, {20}, {21}, {22}, {23}\n'.format(heading, roll, pitch, sys, gyro, accel, mag, temp_c, mx, my, mz, gx, gy, gz, ax, ay, az, lx, ly, lz, grx, gry, grz, current_milli_time() ) )
    # Sleep for a second until the next reading.
    time.sleep(0.001)


f.write("-------------------------")
f.close()
