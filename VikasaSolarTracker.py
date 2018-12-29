#-------------------------------------------------------------
#-------------Solar Tracking Code for Vikasa------------------
#-------------------------------------------------------------

#-------------------------------------------------------------
# This code was created for execution in Python3 and will not work in other
# versions of Python (Pysolar only works when executed in Python3).
#-------------------------------------------------------------

# importing modules
from pysolar.solar import * # Use for Pysolar data
from datetime import datetime # Use for getting instant time
import time # Use for time calls
import sys, select # Use for timed user input
from subprocess import call # Use for turning off the Pi
import os

# Location code
latitude=38.895     # DC decimal north
longitude=-77.036   # DC decimal west
elevation=20        # DC Foggy Bottom elevation [meters]

count=0
for i in range(0,8): 
  d=datetime.now() # want to call this to update sun position
  alt=get_altitude(latitude, longitude, d) # current altitude
  azi=get_azimuth(latitude, longitude, d, elevation) # current azimuth
  count=count+1 # updating the iteration count
  print(d)
  print(alt)
  print(azi)
  print('Number of Iterations: ' + str(count))
  time.sleep(15)
  if alt>31: # For loop terminates if sun is up
    break
  if count==8:
    print('The sun is not high enough. Shutting down.')
    call("sudo shutdown -h now", shell=True) # Raspberry Pi shutdown command

ServoBlaster = open('/dev/servoblaster', 'w') # opening servoblaster

# increasing ServoBlaster's maximum allowable pulse width to 100% for DC motor
os.chdir("/home/pi/PiBits/ServoBlaster/user") # changing the directory to access the servod.c file
call("sudo ./servod --max=20000us", shell=True) # editing the servod.c file
call("pwd", shell=True) # printing the current directory to make sure we've changed directories
time.sleep(5)

ServoBlaster = open('/dev/servoblaster', 'w') # opening servoblaster

# DC motor code to open array
t_end=time.time() + 7 # arbitrary time chosen needed to open the origami array
while (time.time()<t_end):
  ServoBlaster.write('P1-15=80%' + '\n') # Tell the motor to run
  ServoBlaster.flush()
  print('Motor Running')
ServoBlaster.write('P1-15=0%' + '\n') # Tell the motor to stop
ServoBlaster.flush()

# lowering ServoBlaster's maximum allowable pulse width for servo safety
os.chdir("/home/pi/PiBits/ServoBlaster/user") # changing the directory to access the servod.c file
call("sudo ./servod --max=2500us", shell=True) # editing the servod.c file
call("pwd", shell=True) # printing the current directory to make sure we've changed directories
time.sleep(5)

# returning to the "home directory"
os.chdir("/home/pi") # changing the directory to access the servod.c file
call("pwd", shell=True) # printing the current directory to make sure we've changed directories
ServoBlaster = open('/dev/servoblaster', 'w') # opening servoblaster

# Tracking Code
servo_y=0 # initializing servo values
servo_y2=0
servo_x=0
servo_x2=0
alt=0 # initializing altitude and azimuth
azi=0
count=0 # used to count number of tracking iterations

d=datetime.now() # want to call this to update sun position
alt=get_altitude(latitude, longitude, d) # current altitude
azi=get_azimuth(latitude, longitude, d, elevation) # current azimuth

while (azi<=-255 and azi>=-360) or (azi<=0 and azi>=-105): # while loop only works in servo's range of motion
  d=datetime.now() # want to call this to update sun
  alt=get_altitude(latitude, longitude, d) 
  azi=get_azimuth(latitude, longitude, d, elevation) 
  if azi<=-255 and azi>=-360: # Pysolar goes from 0 at south to -180 at north and then -360 at south again
    servo_x=(-1000/105)*(azi+360)+1500 # actual desired x position of tracker 
    servo_x2=servo_x+100 # offset pulse x position 
  else:
    servo_x=(-1000/105)*(azi+105)+2500 # actual desired x position of tracker 
    servo_x2=servo_x+100 # offset pulse x position 
  servo_y=((alt/90)*880)+590 # actual desired y position of tracker 
  servo_y2=1470 # horizontal home position
  ServoBlaster.write('P1-11=' + str(servo_y2) + 'us' + '\n') # pulse to pin 11 "horizontal home position"
  ServoBlaster.flush()
  time.sleep(5)
  servo_y3=servo_y+100 # offset pulse y position
  # breaking each level into incramental steps
  u=(servo_y2-servo_y3)/7
  v=(servo_y2-servo_y3)/6
  w=(servo_y2-servo_y3)/5
  x=(servo_y2-servo_y3)/4
  y=(servo_y2-servo_y3)/3
  z=(servo_y2-servo_y3)/2
  # using servo_x2 to make sure servo always goes to servo_x properly
  # need to due this due to the low precision of the serrvo motors
  ServoBlaster.write('P1-12=' + str(servo_x2) + 'us' + '\n') # pulse to pin 11
  ServoBlaster.flush()
  time.sleep(5)
  ServoBlaster.write('P1-12=' + str(servo_x) + 'us' + '\n') # pulse to pin 12
  ServoBlaster.flush()
  time.sleep(5)
  print (servo_y2)
  if (servo_y2-servo_y3)>=700:
    for i in range(0,7):
      servo_y2=servo_y2-u # renamed servo_y2 to move servo up to "horizontal home position" in incraments
      ServoBlaster.write('P1-11=' + str(servo_y2) + 'us' + '\n') # pulse to pin 11
      ServoBlaster.flush()
      time.sleep(0.5)
  elif (servo_y2-servo_y3)>=600:
    for i in range(0,6):
      servo_y2=servo_y2-v
      ServoBlaster.write('P1-11=' + str(servo_y2) + 'us' + '\n') # pulse to pin 11
      ServoBlaster.flush()
      time.sleep(0.5)
  elif (servo_y2-servo_y3)>=500:
    for i in range(0,5):
      servo_y2=servo_y2-w
      ServoBlaster.write('P1-11=' + str(servo_y2) + 'us' + '\n') # pulse to pin 11
      ServoBlaster.flush()
      time.sleep(0.5)
  elif (servo_y2-servo_y3)>=400:
    for i in range(0,4):
      servo_y2=servo_y2-x
      ServoBlaster.write('P1-11=' + str(servo_y2) + 'us' + '\n') # pulse to pin 11
      ServoBlaster.flush()
      time.sleep(0.5)
  elif (servo_y2-servo_y3)>=300:
    for i in range(0,3):
      servo_y2=servo_y2-y
      ServoBlaster.write('P1-11=' + str(servo_y2) + 'us' + '\n') # pulse to pin 11
      ServoBlaster.flush()
      time.sleep(0.5)
  elif (servo_y2-servo_y3)>=200:
    for i in range(0,2):
      servo_y2=servo_y2-z
      ServoBlaster.write('P1-11=' + str(servo_y2) + 'us' + '\n') # pulse to pin 11
      ServoBlaster.flush()
      time.sleep(0.5)
  else:
    servo_y2=servo_y3
    ServoBlaster.write('P1-11=' + str(servo_y2) + 'us' + '\n') # pulse to pin 11
    ServoBlaster.flush()
    time.sleep(0.5)
  # now we are telling the servo motor to hold the desired y position to mirror the sun's position
  # we can control how long it holds this position by adjusting the max number in the range 
  # 1200s = 20 min
  for i in range(0,1200):
    ServoBlaster.write('P1-11=' + str(servo_y) + 'us' + '\n') # pulse to pin 11
    ServoBlaster.flush()
    time.sleep(0.5)
  # now we are asking the servo motor to bring the tracker back up to the "horizontal home position"
  while (servo_y<1270):
    servo_y=servo_y+100
    ServoBlaster.write('P1-11=' + str(servo_y) + 'us' + '\n') # pulse to pin 11
    ServoBlaster.flush()
    time.sleep(1)
  servo_y=1470 # horizontal home position
  ServoBlaster.write('P1-11=' + str(servo_y) + 'us' + '\n') # pulse to pin 11
  ServoBlaster.flush()
  time.sleep(1)
  count=count+1 # Shows how many iterations have been done
  print(count)
  print(str(d) + '\n')
  print(str(azi) + '\n')
  print(str(alt) + '\n')

# increasing ServoBlaster's maximum allowable pulse width to 100% for DC motor
os.chdir("/home/pi/PiBits/ServoBlaster/user") # changing the directory to access the servod.c file
call("sudo ./servod --max=20000us", shell=True) # editing the servod.c file
call("pwd", shell=True) # printing the current directory to make sure we've changed directories
time.sleep(5)

ServoBlaster = open('/dev/servoblaster', 'w') # opening servoblaster

# DC motor code to close array
t_end=time.time() + 10
while (time.time()<t_end):
  ServoBlaster.write('P1-16=100%' + '\n') # Tell the motor to run
  ServoBlaster.flush()
  print('Motor Running')
ServoBlaster.write('P1-16=0%' + '\n') # Tell the motor to stop
ServoBlaster.flush()

# lowering ServoBlaster's maximum allowable pulse width for servo safety
os.chdir("/home/pi/PiBits/ServoBlaster/user") # changing the directory to access the servod.c file
call("sudo ./servod --max=2500us", shell=True) # editing the servod.c file
call("pwd", shell=True) # printing the current directory to make sure we've changed directories
time.sleep(5)

# returning to the "home directory"
os.chdir("/home/pi") # changing the directory to access the servod.c file
call("pwd", shell=True) # printing the current directory to make sure we've changed directories

# Code to turn off the pi
call("sudo shutdown -h now", shell=True)


# ------------------------------------------------------------
# ---------------End of Working Code--------------------------
#-------------------------------------------------------------


# OPTIONAL CODE
#-------------------------------------------------------------

# use following code for a user interrupt to end the code prematurely 
# code isn't necessary but can be implemented if desired

#print ("You have 3 minutes to access the Pi!")
#i, o, e = select.select( [sys.stdin], [], [], 180 ) # 180 seconds
#if (i):
#  print ("Have fun with the Pi!")
#  sys.exit() # Stops the code and exits
#else:
#  print ("Commencing Solar Tracking!")
# Code continues if there is no input

#time.sleep(120)


# CODE EXPLANATION
#-------------------------------------------------------------

#General Pysolar Code
#latitude=38.895     # DC decimal north
#longitude=-77.036   # DC decimal west
#elevation=18        # DC Foggy Bottom meters
#d=datetime.datetime.now() # want to call this to update sun position
#alt=get_altitude(latitude, longitude, d) # degrees from horizon
#azi=get_azimuth(latitude, longitude, d, elevation) # degrees from south
# with pos number = east of south or CCW
#rad=radiation.get_radiation_direct(d, alt) # clear sky radiation

#General ServoBlaster code
#ServoBlaster.write('P1-11=2500us' + '\n')	# lets you write to file
#and hit enter
#ServoBlaster.flush() # lets the info go to the file immediately without it
# needing to be closed and opened first
