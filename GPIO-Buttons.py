from mpd import MPDClient
import time
import RPi.GPIO as GPIO
from subprocess import call
from datetime import datetime


# Change into the GPIO Pins you are jusing
# pushbutton connected to this GPIO pin, using pin 5 for the shutdownbutton also has the benefit of
# waking / powering up Raspberry Pi when button is pressed
shutdownPin = 5
nextPin = 40
pausePin = 38
previousPin = 36

# if button pressed for at least this long then shutdown. If Button pressed for at least rebootdownSeconds then Reboot.
shutdownSeconds = 0.25
rebootdownSeconds = 5
pressmin = 0.25

GPIO.setmode(GPIO.BOARD)
chan_list = [shutdownPin, nextPin, pausePin, previousPin]
GPIO.setup(chan_list, GPIO.IN, pull_up_down=GPIO.PUD_UP)

buttonPressedTime = None
presstime = None

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

def buttonshutdownChanged(pin):
	global buttonPressedTime
	if not (GPIO.input(pin)):
		# button is down
		print "shutdown down"
		if buttonPressedTime is None:
			buttonPressedTime = datetime.now()
	else:
        	# button is up
		print "shutdown up"
		if buttonPressedTime is not None:
			elapsed = (datetime.now() - buttonPressedTime).total_seconds()
			buttonPressedTime = None
			print elapsed
			if elapsed >= rebootdownSeconds:
                		# button pressed for more than specified time, reboot
				call(['shutdown', '-r', 'now'], shell=False)
			elif elapsed >= shutdownSeconds:
                		# button pressed for a shorter time, shutdown
				call(['shutdown', '-h', 'now'], shell=False)
	
def buttonnextChanged(pin):

	global buttonPressedTime
	global presstime
	if not (GPIO.input(pin)):
		# button is down
		print "next down"
		if buttonPressedTime is None:
			buttonPressedTime = datetime.now()
			# Fast Forward
			presstime = datetime.now()
		
		
	else:
        	# button is up
		print "next up"
		if buttonPressedTime is not None:
			elapsed = (datetime.now() - buttonPressedTime).total_seconds()
			buttonPressedTime = None
			presstime = None
			print elapsed
			if elapsed >= pressmin:	
				client = connectMPD()
				client.next()
				client.play()
				client.close()

def buttonpauseChanged(pin):

	global buttonPressedTime
	if not (GPIO.input(pin)):
		# button is down
		print "pause down"
		if buttonPressedTime is None:
			buttonPressedTime = datetime.now()
	else:
        	# button is up
		print "pause up"
		if buttonPressedTime is not None:
			elapsed = (datetime.now() - buttonPressedTime).total_seconds()
			buttonPressedTime = None
			print elapsed
			print pressmin
			if elapsed >= pressmin:
				print "elapsed bigger or equal pressmin"
				client = connectMPD()
				client.pause()
				client.close()
			else:
				print "noe mach ich nich"


def buttonpreviousChanged(pin):

	global buttonPressedTime
	if not (GPIO.input(pin)):
		# button is down
		if buttonPressedTime is None:
			buttonPressedTime = datetime.now()
	else:
        # button is up
		if buttonPressedTime is not None:
			elapsed = (datetime.now() - buttonPressedTime).total_seconds()
			buttonPressedTime = None
			if elapsed >= pressmin:	
				client = connectMPD()
				client.previous()
				client.play()
				client.close()

   
# subscribe to button presses
GPIO.add_event_detect(shutdownPin, GPIO.BOTH, callback=buttonshutdownChanged)
GPIO.add_event_detect(nextPin, GPIO.BOTH, callback=buttonnextChanged)
GPIO.add_event_detect(pausePin, GPIO.BOTH, callback=buttonpauseChanged)
GPIO.add_event_detect(previousPin, GPIO.BOTH, callback=buttonpreviousChanged)


while True:
	# sleep to reduce unnecessary CPU usage
	if not (GPIO.input(40)):
				if (presstime- buttonPressedTime).total_seconds()>=2:
					client = connectMPD()
					client.seekcur(+5)
	time.sleep(5)
