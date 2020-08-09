from helpfunctions import *
# this section ensures wifi is up; only needed if you turn wifi off for power savings later
#cmd 'ifconfig wlan0 up'
#os.system(cmd)

f = open("spinfile.txt", "a")
f.write("-------------------------")
f.write(time.strftime("      %a %d-%m-%Y @ %H:%M:%S  {0}".format(current_milli_time() ) ) )
f.write("\n")



f.write("GPIOs are setup, digital potentiometer is enabled \n")

print "hello, fuck you"

#need to sleep for 2 minutes or so: everytime you reboot can ssh back in
#sleep(120)
#os.system('ifconfig wlan0 down')   #to save power?

# prep GPIOs for digital potentiometer
setClock(0)
setSDI(1)
setWLAT(1)
setSHDN(1)  #SHDN_bar pin is high, chip is on
setCS(1)


# ensure potentiometer is set to zero before turning on PWM
for n in range(256):
	decrement()
	sleep( 0.01 )


##### time for me to walk outside and lift drone (ensure scirpt is on 1s, 3 seconds to pick up controller, 7 seconds to rise it)
print('sleeping 0 seconds\n')
sleep( 4 )  #not there is about 6s of delay at least here, so totla is 11s from button press


# turn on PWM controller
GPIO.output(40, GPIO.HIGH)    #high signal  to gate of MOSFET for PWM 
print "pwm controller powered up and inital state at 0"
# this is about 5 seconds after button with no sleeptime added

slowdownFactor = 0.15
peakValue = 256  #use 34 for laucnhtest; at 40, one of the batteries turned off during steady state run
for n in range(peakValue):  #37 about it
	increment()
	print('we are at {0}'.format(n) )
	sleeptime = 0.01 + n * 0 * slowdownFactor   #ramping up at constant rate per interation
	sleep( sleeptime )

f.write(time.strftime("Digital Potentiometer set    %a %d-%m-%Y @ %H:%M:%S   {0}\n".format(current_milli_time() ) ) )
print "digital potentiometer set"
# WITH NO additional delays, the time to here is about 11 seconds

# delay for spin stabilization
sleeptime = 15
print('maintaining for {0} seconds'.format(sleeptime) )
f.write('maintaining for {0} seconds \n'.format(sleeptime) )
for n in range(sleeptime):
	sleep(1)
	print('maintaining for {0} seconds'.format(sleeptime-n-1) )
# end delay for spin stabilization, ready to fire

# optional loop to decrease spin
#print('dropping to 241\n')
#for n in range(15):
#	decrement()
#	sleep(0.01)

#print('at 241, hold 12 seconds \n')
#sleep(12)

# ignition firing. E9 engine takes 100mS from ignition to have enough lift to raise the rocket. time from GPIO high to ignition estimated at 50mS 
# note ignition to 5 foot altitude is 250 mS per OpenRocket.
f.write(time.strftime("About to fire Ignition::    %a %d-%m-%Y @ %H:%M:%S   {0}\n".format(current_milli_time() ) ) )
GPIO.output(32, GPIO.HIGH)    #turn on MOSFET for ignition
print("Ignition mosfet fired\n")
f.write(time.strftime("Fired Ignition MOSFET::    %a %d-%m-%Y @ %H:%M:%S   {0}\n".format(current_milli_time() ) ) )
f.close()
f = open("spinfile.txt", "a")
# end firing ignition ##########################################

sleep( 2.0 )   #want to ensure this thing has lift before cutting string. Expect up to 250mS for motor to launch. tough to say
GPIO.output(32, GPIO.LOW)      #power off ignition charge
sleep( 0.4 )

#fire string-cut charges. Note: ~50 mS delay from GPIO High to string broken.
print('about to blow string charge\n')
f.write(time.strftime("About to Fire  String Blowing MOSFET:    %a %d-%m-%Y @ %H:%M:%S  {0}\n".format(current_milli_time() ) ) )
GPIO.output(21, GPIO.HIGH)    #turn on MOSFET for string blowing
f.write(time.strftime("Fired String Blowing MOSFET:    %a %d-%m-%Y @ %H:%M:%S  {0}\n".format(current_milli_time() ) ) )
f.close()
f = open("spinfile.txt", "a")
##### done firing string ####################################

#### motor has 2.9s burn time. open rocket estimates 0.5s after burnout to apogee *if* all goes well  ####################
print("ignition and string gpios fired, pausing 3.2 seconds")
sleep(3)
GPIO.output(21, GPIO.LOW)    #power off string charge
f.write('firing ejection charge now\n')
GPIO.output(38, GPIO.HIGH)    #turn on MOSFET for ejection charge
print("fired ejection charge\n")
f.write(time.strftime("Fired Ejection Charge MOSFET:    %a %d-%m-%Y @ %H:%M:%S   {0}\n".format(current_milli_time() ) ) )
f.close()
sleep(2)
GPIO.output(38, GPIO.LOW)    #power off ejection charge
f = open("spinfile.txt", "a")
f.write('winding down potentiometer  \n')
print "winding down potentiometer"
# need to unwide potentiometer
for n in range(peakValue):
	decrement()
	sleeptime = 0.01 + 0 * (peakValue-n) * slowdownFactor
	sleep( sleeptime )
	print('we are at {0}'.format(peakValue-n) )

GPIO.output(40, GPIO.LOW)    #power off to PWM controller  on via MOSFET
GPIO.output(38, GPIO.LOW)    #power off ejection charge
GPIO.output(21, GPIO.LOW)    #power off string charge
GPIO.output(32, GPIO.LOW)      #power off ignition charge

f.write("logging completed\n\n\n\n")
f.close()
print "spintest completed completed"
