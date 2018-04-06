'''
Solar Tracking Code for Vikasa

This code was created for execution in Python3 and will not work in other
versions of Python (Pysolar only works when executed in Python3).
'''

# importing modules
from pysolar.solar import * # Use for Pysolar data
from datetime import datetime # Use for getting instant time
import time # Use for time calls
import sys, select # Use for timed user input
from subprocess import call # Use for turning off the Pi

ServoBlaster = open('/dev/servoblaster', 'w') # opening servoblaster

# code for timed user interrupt to end code
print ("You have 3 minutes to access the Pi!")
i, o, e = select.select( [sys.stdin], [], [], 180 ) # 180 seconds = 3 min
if (i):
  print ("Have fun with the Pi!")
  sys.exit() # Stops the code and exits
else:
  print ("Commencing Solar Tracking!")
# Code continues if there is no input

# Location code
latitude=38.895     # DC decimal north
longitude=-77.036   # DC decimal west
elevation=18        # DC Foggy Bottom meters

# Waiting 5 minutes for the sun to come up
# Terminates code if sun doesn't come up in time
count=0
for i in range(0,20): 
  d=datetime.now() # want to call this to update sun position
  alt=get_altitude(latitude, longitude, d) # current altitude
  azi=get_azimuth(latitude, longitude, d, elevation) # current azimuth
  count=count+1
  print(d)
  print(alt)
  print(azi)
  print('Number of Iterations: ' + str(count))
  time.sleep(15)
  if alt>10: # For loop terminates if sun is up
    break
  if count==20:
    print('The sun never came up. Shutting down.')
    call("sudo shutdown -h now", shell=True) # Raspberry Pi shutdown command
  
# DC motor code to open array
ServoBlaster.write('P1-15=2500us' + '\n') # Tell the motor to run
ServoBlaster.flush()
time.sleep(10) # Tell the motor to run for x amount of seconds
ServoBlaster.write('P1-15=500us' + '\n') # Tell the motor to stop
ServoBlaster.flush()

# Tracking Code
servo_y=0 # initializing servo values
servo_x=0
alt=0 # initializing altitude and azimuth
azi=0
count=0 # used to count number of tracking iterations

while (alt>10): # setting the contraints in y axis degrees of motion
  d=datetime.now() # want to call this to update sun position
  alt=get_altitude(latitude, longitude, d) # current altitude
  azi=get_azimuth(latitude, longitude, d, elevation) # current azimuth
  servo_y=((alt/90)*1000)+500
  servo_x=((azi/180)*1000)+1500 # Put servo in center position
  ServoBlaster.write('P1-11=' + str(servo_y) + 'us' + '\n') # pulse to pin 11
  ServoBlaster.flush()
  ServoBlaster.write('P1-12=' + str(servo_x) + 'us' + '\n') # pulse to pin 12
  ServoBlaster.flush()
  count=count+1 # Shows how many iterations have been done
  print(count)
  print(str(d) + '\n')
  print(str(servo_y) + '\n')
  print(str(servo_x) + '\n')
  time.sleep(600) # Sleep for 10 min before next iteration

# DC motor code to close array
ServoBlaster.write('P1-16=2500us' + '\n') # Tell the motor to run in the opposite direction
ServoBlaster.flush()
time.sleep(10) # Tell the motor to run for x amount of seconds
ServoBlaster.write('P1-16=500us' + '\n') # Tell the motor to stop
ServoBlaster.flush()

# Last chance to acces the Pi before it turns off
print ("You have 3 minutes to access the Pi!")
i, o, e = select.select( [sys.stdin], [], [], 600 ) # 600 seconds = 10 min
if (i):
  print ("Have fun with the Pi!")
  sys.exit() # Stops the code and exits
else:
  print ("Turning the Pi Off")
# Code continues if there is no input

# Code to turn off the pi
call("sudo shutdown -h now", shell=True)

# End of working code

'''
General Pysolar Code
latitude=38.895     # DC decimal north
longitude=-77.036   # DC decimal west
elevation=18        # DC Foggy Bottom meters
d=datetime.datetime.now() # want to call this to update sun position
alt=get_altitude(latitude, longitude, d) # degrees from horizon
azi=get_azimuth(latitude, longitude, d, elevation) # degrees from south
# with pos number = east of south or CCW
rad=radiation.get_radiation_direct(d, alt) # clear sky radiation

General ServoBlaster code
ServoBlaster.write('P1-11=2500us' + '\n')	# lets you write to file
and hit enter
ServoBlaster.flush() # lets the info go to the file immediately without it
# needing to be closed and opened first
'''
