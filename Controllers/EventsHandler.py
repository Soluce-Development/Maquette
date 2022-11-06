import RPi.GPIO as GPIO

# GPIO Inputs
SENSOR_DOOR = 5
BTN_START = 6
BTN_DOOR = 7
SENSOR_PEDAL = 9

# GPIO Outputs
ACTUATOR_DOOR = 10
ACTUATOR_JAW = 10
LED_START = 11
LED_DOOR = 12
LED_MACHINING = 13

# Initialisation
GPIO.setmode(GPIO.BOARD)

# Setting Inputs
INPUTS = (SENSOR_DOOR, BTN_START, BTN_DOOR, SENSOR_PEDAL)
GPIO.setup(INPUTS, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Setting Outputs
OUTPUTS = (ACTUATOR_JAW, LED_START, LED_DOOR, LED_MACHINING)
GPIO.setup(OUTPUTS, GPIO.OUT, initial=GPIO.LOW)


# --- Callback functions ---

def toggle_start():
    """Turn on/off the machine."""
    GPIO.output(LED_START, not GPIO.input(LED_START))


def open_door():
    """Open the door."""
    GPIO.output(ACTUATOR_DOOR, GPIO.LOW)
    GPIO.output(LED_DOOR, GPIO.LOW)


def close_door():
    """Close the door if the door is still closed."""
    if GPIO.input(SENSOR_DOOR):
        GPIO.output(ACTUATOR_DOOR, GPIO.HIGH)
        GPIO.output(LED_DOOR, GPIO.HIGH)


def door_closed():
    """Turn on the LED_DOOR and closed the door."""
    GPIO.output(LED_DOOR, GPIO.HIGH)
    GPIO.output(ACTUATOR_DOOR, GPIO.HIGH)


def door_opened():
    """Turn off the LED_DOOR."""
    GPIO.output(LED_DOOR, GPIO.LOW)


def toggle_jaw():
    """Open/close the jaw."""
    GPIO.output(ACTUATOR_JAW, not GPIO.input(ACTUATOR_JAW))


# --- Add events ---

def add_events():

    GPIO.add_event_detect(BTN_START, GPIO.RISING, callback=toggle_start, bouncetime=500)

    GPIO.add_event_detect(BTN_DOOR, GPIO.RISING, callback=open_door, bouncetime=500)
    GPIO.add_event_detect(BTN_DOOR, GPIO.FALLING, callback=close_door, bouncetime=500)

    GPIO.add_event_detect(SENSOR_DOOR, GPIO.RISING, callback=door_closed, bouncetime=500)
    GPIO.add_event_detect(SENSOR_DOOR, GPIO.FALLING, callback=door_opened, bouncetime=500)

    GPIO.add_event_detect(SENSOR_PEDAL, GPIO.RISING, callback=toggle_jaw, bouncetime=500)
