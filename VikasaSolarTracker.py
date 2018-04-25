#Solar Tracking Code for Vikasa

#This code was created for execution in Python3 and will not work in other
#versions of Python (Pysolar only works when executed in Python3).

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
  if alt>15: # For loop terminates if sun is up
    break
  if count==20:
    print('The sun is not high enough. Shutting down.')
    call("sudo shutdown -h now", shell=True) # Raspberry Pi shutdown command
  
# DC motor code to open array
t_end=time.time() + 10
while (time.time()<t_end):
  ServoBlaster.write('P1-15=2500us' + '\n') # Tell the motor to run
  ServoBlaster.flush()
  print('Motor Running')
time.sleep(10) # Tell the motor to run for x amount of seconds

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

while (azi<=105 and azi>=-105): 
  d=datetime.now() # want to call this to update sun
  alt=get_altitude(latitude, longitude, d) 
  azi=get_azimuth(latitude, longitude, d, elevation) 
  servo_x=((azi/180)*1000)+1500 
  servo_x2=((azi/180)*1000)+1650
  servo_y=((alt/90)*845)+625
  servo_y2=1470
  ServoBlaster.write('P1-11=' + str(servo_y2) + 'us' + '\n') # pulse to pin 11
  ServoBlaster.flush()
  time.sleep(5)
  servo_y3=servo_y+100
  w=(servo_y2-servo_y3)/5
  x=(servo_y2-servo_y3)/4
  y=(servo_y2-servo_y3)/3
  z=(servo_y2-servo_y3)/2
  ServoBlaster.write('P1-12=' + str(servo_x2) + 'us' + '\n') # pulse to pin 11
  ServoBlaster.flush()
  time.sleep(5)
  ServoBlaster.write('P1-12=' + str(servo_x) + 'us' + '\n') # pulse to pin 11
  ServoBlaster.flush()
  time.sleep(5)
  print (servo_y2)
  if (servo_y2-servo_y3)>=500:
    for i in range(0,5):
      servo_y2=servo_y2-w
      ServoBlaster.write('P1-11=' + str(servo_y2) + 'us' + '\n') # pulse to pin 12
      ServoBlaster.flush()
      time.sleep(0.5)
  elif (servo_y2-servo_y3)>=400:
    for i in range(0,4):
      servo_y2=servo_y2-x
      ServoBlaster.write('P1-11=' + str(servo_y2) + 'us' + '\n') # pulse to pin 12
      ServoBlaster.flush()
      time.sleep(0.5)
  elif (servo_y2-servo_y3)>=300:
    for i in range(0,3):
      servo_y2=servo_y2-y
      ServoBlaster.write('P1-11=' + str(servo_y2) + 'us' + '\n') # pulse to pin 12
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
  for i in range(0,1200):
    ServoBlaster.write('P1-11=' + str(servo_y) + 'us' + '\n') # pulse to pin 11
    ServoBlaster.flush()
    time.sleep(0.5)
  while (servo_y<1270):
    servo_y=servo_y+100
    ServoBlaster.write('P1-11=' + str(servo_y) + 'us' + '\n') # pulse to pin 11
    ServoBlaster.flush()
    time.sleep(1)
  servo_y=1470
  ServoBlaster.write('P1-11=' + str(servo_y) + 'us' + '\n') # pulse to pin 11
  ServoBlaster.flush()
  time.sleep(1)
  count=count+1 # Shows how many iterations have been done
  print(count)
  print(str(d) + '\n')
  print(str(azi) + '\n')
  print(str(alt) + '\n')

# DC motor code to close array
t_end=time.time() + 10
while (time.time()<t_end):
  ServoBlaster.write('P1-16=2500us' + '\n') # Tell the motor to run
  ServoBlaster.flush()
  print('Motor Running')
time.sleep(10) # Tell the motor to run for x amount of seconds

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
