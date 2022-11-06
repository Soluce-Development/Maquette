import RPi.GPIO as GPIO

channel = 3
state = GPIO.HIGH

# Initialisation
GPIO.setmode(GPIO.BOARD)

# GPIO.PUD_UP ou GPIO.PUD_DOWN
GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# State can be 0 / GPIO.LOW / False or 1 / GPIO.HIGH / True.
GPIO.setup(channel, GPIO.OUT, initial=GPIO.HIGH)

# channel
# chan_list = [11,12]
# chan_list = (11,12)

# To read the value of a GPIO pin:
# State can be 0 / GPIO.LOW / False or 1 / GPIO.HIGH / True.
GPIO.input(channel)

# To set the value of a GPIO pin:
# State can be 0 / GPIO.LOW / False or 1 / GPIO.HIGH / True.
GPIO.output(channel, state)

# block execution of your program until an edge is detected
# GPIO.RISING, GPIO.FALLING or GPIO.BOTH
# f you only want to wait for a certain length of time, you can use the timeout parameter: timeout=5000
GPIO.wait_for_edge(channel, GPIO.RISING)

# add rising edge detection on a channel, ignoring further edges for 200ms for switch bounce handling
# add a 0.1uF capacitor across your switch.
GPIO.add_event_detect(channel, GPIO.RISING, callback=my_callback, bouncetime=200)
do_something()
if GPIO.event_detected(channel):
    print('Button pressed')


# If for some reason, your program no longer wishes to detect edge events, it is possible to stop them:
GPIO.remove_event_detect(channel)


GPIO.add_event_callback(channel, my_callback_one, bouncetime=200)
GPIO.add_event_callback(channel, my_callback_two)


# At the end any program, it is good practice to clean up any resources you might have used
GPIO.cleanup()
