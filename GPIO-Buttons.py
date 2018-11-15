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
nextPin = 36
pausePin = 38
previousPin = 40

# if button pressed for at least this long then shutdown. If Button pressed for at least rebootdownSeconds then Reboot.
shutdownSeconds = 0.5
rebootdownSeconds = 10

GPIO.setmode(GPIO.BOARD)
chan_list = [shutdownPin, nextPin, pausePin, previousPin]
GPIO.setup(chan_list, GPIO.IN, pull_up_down=GPIO.PUD_UP)


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

def buttonshutdownChanged(pin)
   
# subscribe to button presses
GPIO.add_event_detect(shutdownPin, GPIO.BOTH, callback=buttonshutdownChanged)
GPIO.add_event_detect(nextPin, GPIO.BOTH, callback=buttonnextChanged)
GPIO.add_event_detect(pausePin, GPIO.BOTH, callback=buttonpauseChanged)
GPIO.add_event_detect(previousPin, GPIO.BOTH, callback=buttonpreviousChanged)


while True:
    # sleep to reduce unnecessary CPU usage
time.sleep(5)
