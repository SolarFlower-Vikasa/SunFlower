'''
Solar Tracking Code for Vikasa

This code was created for execution in Python3 and will not work in other
versions of Python (Pysolar only works when executed in Python3).
'''

# Initialization of Code

# importing modules
from pysolar.solar import * # Use for Pysolar data
from datetime import datetime # Use for getting instant time
import time # Use for time calls
import sys, select # Use for timed user input
from subprocess import call # Use for turning off the Pi

ServoBlaster = open('/dev/servoblaster', 'w') # opening servoblaster

# code structure: code must be put into boot-up sequence of pi for automation
#   - code saying wait 3 min for user interrupt
#       => if there is interrupt then stop the end the code but keep the pi on
#       => if there is no interrupt / time runs out run the rest of the code
#   - run the DC motor to extend the array
#   - run the solar tracker while loop for the servo motors
#       => choose to run code over range of degrees of altitude (ie greater than 15 deg)
#   - run code for DC motor to close array
#   - code saying wait 10 min for user interrupt
#       => if there is interrupt then stop the end the code but keep the pi on
#       => if there is no interrupt / time runs out run the rest of the code
#   - run code to turn off the pi

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
yaxis=[] # array for altitude values

while (alt>10): # setting the contraints in y axis degrees of motion
  d=datetime.now() # want to call this to update sun position
  alt=get_altitude(latitude, longitude, d) # current altitude
  azi=get_azimuth(latitude, longitude, d, elevation) # current azimuth
  yaxis.ammend(alt) # puts altitude values into an array
  time.sleep(30)
  d=datetime.now() # Adding a second value to the array to see if increasing or decreasing
  alt=get_altitude(latitude, longitude, d)
  azi=get_azimuth(latitude, longitude, d, elevation)
  yaxis.ammend(alt)
  w=all(earlier <= later for earlier, later in zip(yaxis, yaxis[1:])) # Tells if array values are increasing or decreasing
  if w==True: # Here make one end of the servo the starting point
      # angle is from 500us to 1500us
      servo_y=((alt/90)*1000)+500
  else:
      # angle is from 1501us to 2500us so code doesn't get stuck on 1500us
      servo_y=((alt/90)*1000)+1501
  if azi>0: # Code will work if servo head center made starting point
      servo_x=((azi/180)*1000)+1501
  else:
      servo_x=((azi/180)*1000)+500
  ServoBlaster.write('P1-11=' + str(servo_y) + 'us' + '\n')
  ServoBlaster.flush()
  ServoBlaster.write('P1-12=' + str(servo_x) + 'us' + '\n')
  ServoBlaster.flush()
  count=count+1 # Just to show how many iterations have been done
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
