# Drone-Rocket

The files that run on the raspberry pi zero w are:
- helpfunctions.py   # sets up GPIOs and adds some helper functions
- IMUandlog.py       # this initializes the IMU [BNO055 from Github], starts a calibration sequence, then logs data to IMU.txt
- spinFire.py        # this spins a spinmass [controls a digital potentiometer that connects to a dc motor], then fires an ignition charge, then a string charge, then the ejeciton charge, then winds down the spinmass. Writes data to spinfile.txt]

The logfiles from the launch are:
- IMU.txt   # output from IMUandlog.py. A lot of data, linear acceleration, gyroscope, system status, gravity, magnetic field. 
- spinfile.txt #output from spinFire.py. Basically gives me time stamps of major events so I can correlate them to the IMU file.

Auxilliary python file I used to process and plot the IMU.txt logfile:
- IMUandlog.py

Author: Peter Bevelacqua
Feel free to reuse code if you want, this is mainly in case you want to see how I implemented things.
