try:
    from mpd import MPDClient
except ImportError:
print "Could not import MPDClient"

import time
try:
    import RPi.GPIO as GPIO
except ImportError:
print "Could not import GPIO"

# pushbutton connected to this GPIO pin, using pin 5 for the shutdownbutton also has the benefit of
# waking / powering up Raspberry Pi when button is pressed
shutdownPin = 5
nextPin =
pausePin =
previousPin =

def connectMPD():
	try:
		client = MPDClient()               # create client object
		client.timeout = 200               # network timeout in seconds (floats allowed), default: None
		client.idletimeout = None  
		print "Connecting..."
		client.connect("localhost", 6600) 
		print "Connected!"
		return client
	except:
		print 'Could not connect to MPD server'

    
   
