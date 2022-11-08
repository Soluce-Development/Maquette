import RPi.GPIO as GPIO

# GPIO Inputs
SENSOR_DOOR = 13
BTN_START = 5
BTN_DOOR = 19
BTN_EMERGENCY = 6
SENSOR_PEDAL = 26

# GPIO Outputs
ACTUATOR_DOOR = 22
ACTUATOR_JAW = 3
LED_START = 4
LED_DOOR = 27
LED_MACHINING = 17

# Initialisation
GPIO.setmode(GPIO.BOARD)

# Setting Inputs
INPUTS = (SENSOR_DOOR, BTN_START, BTN_DOOR, BTN_EMERGENCY, SENSOR_PEDAL)
GPIO.setup(INPUTS, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Setting Outputs
OUTPUTS = (ACTUATOR_DOOR, ACTUATOR_JAW, LED_START, LED_DOOR, LED_MACHINING)
GPIO.setup(OUTPUTS, GPIO.OUT, initial=GPIO.LOW)


# --- Callback functions ---

def toggle_start(pin):
    """Turn on/off the machine."""
    GPIO.output(LED_START, not GPIO.input(LED_START))


def open_door(pin):
    """Open the door."""
    GPIO.output(ACTUATOR_DOOR, GPIO.LOW)
    GPIO.output(LED_DOOR, GPIO.LOW)


def close_door(pin):
    """Close the door if the door is still closed."""
    if GPIO.input(SENSOR_DOOR):
        GPIO.output(ACTUATOR_DOOR, GPIO.HIGH)
        GPIO.output(LED_DOOR, GPIO.HIGH)


def door_closed(pin):
    """Turn on the LED_DOOR and closed the door."""
    GPIO.output(LED_DOOR, GPIO.HIGH)
    GPIO.output(ACTUATOR_DOOR, GPIO.HIGH)


def door_opened(pin):
    """Turn off the LED_DOOR."""
    GPIO.output(LED_DOOR, GPIO.LOW)


def toggle_jaw(pin):
    """Open/close the jaw."""
    GPIO.output(ACTUATOR_JAW, not GPIO.input(ACTUATOR_JAW))


# --- Add events ---

def add_events():
    GPIO.add_event_detect(BTN_START, GPIO.RISING, callback=toggle_start, bouncetime=500)

    GPIO.add_event_detect(BTN_DOOR, GPIO.RISING, callback=open_door, bouncetime=500)
    # GPIO.add_event_detect(BTN_DOOR, GPIO.FALLING, callback=close_door, bouncetime=500)

    GPIO.add_event_detect(SENSOR_DOOR, GPIO.RISING, callback=door_closed, bouncetime=500)
    # GPIO.add_event_detect(SENSOR_DOOR, GPIO.FALLING, callback=door_opened, bouncetime=500)

    GPIO.add_event_detect(SENSOR_PEDAL, GPIO.RISING, callback=toggle_jaw, bouncetime=500)
