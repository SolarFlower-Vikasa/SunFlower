# SunFlower
# Solar Tracker Code for Vikasa

"""
Written and Developed by Zach Switzer copyright February 14th 2018. Duplication
or modification of this code can only be used for educational or non-profit
projects, or for any projects with the original developer's (Zach Switzer)
consent.

Vikasa translates to the opening or closing of a flower in Sanskrit, and is a
project developed at the George Washington University by Zach Switzer,
Ali Ahmed, Feng (Jason) Xiang, Aaron Patron, and Jacari Matthews. It is a
portable solar charging unit designed and created in order to tackle the issue
of access to clean and renewable power that arises in developing nations.
It incorperates a Raspberry Pi Zero W as a computer for those in developing
nations who do not already have a computer and as a controller for the
function of the system as a whole, a solar array that expands and contracts
through origami folding, and a battery pack with DC USB access. This project
was supported and funded by Amar Hanspal, Makerbot, and Ninjatek. Special
thanks to mentors who provided support and inspiration along the way including:
Shannon Zirbel (origami solar array), Larry Howell, Megan Leftwich, and
Kevin Patton.

This code was developed for a dual axis solar tracking system with 360 degree
rotation in the x axis and 180 degree rotation in the y axis. It is meant to
be used with 2 servo motors (each rotate 180 degrees) and employs the Pysolar
and ServoBlaster open source programs in order to track the sun's movement
and mirror it with motors.

This code was developed with the intent of it being used on a raspberry pi and
as a result it is assumed that both Pysolar and ServoBlaster have already been
downloaded onto the modified (for Pysolar) linux computer and can be called
upon and executed at will. It is meant to be executed on the raspberry pi's
bootup sequence.

This code was created for execution in Python3 and will not work in other
versions of Python (Pysolar only works when executed in Python3).
"""
