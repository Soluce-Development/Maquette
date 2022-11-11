import RPi.GPIO as GPIO

from Constants import *
from Models.ScreenModels import Screen


# Initialisation
GPIO.setmode(GPIO.BCM)

# Setting Inputs
INPUTS = (SENSOR_DOOR, BTN_DOOR, BTN_EMERGENCY, SENSOR_PEDAL)
GPIO.setup(INPUTS, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Setting Outputs
OUTPUTS = (ACTUATOR_DOOR, ACTUATOR_JAW, LED_DOOR, LED_MACHINING)
GPIO.setup(OUTPUTS, GPIO.OUT, initial=GPIO.LOW)


# --- Callback functions ---

# def toggle_start(pin):
#     """Turn on/off the machine."""
#     GPIO.output(LED_START, not GPIO.input(LED_START))


# def open_door(pin):
#     """Open the door."""
#     # GPIO.output(ACTUATOR_DOOR, GPIO.LOW)
#     GPIO.output(LED_DOOR, GPIO.LOW)


def open_door(pin):
    """Close the door if the door is still closed."""
    if not GPIO.input(BTN_DOOR):
        GPIO.output(LED_DOOR, GPIO.LOW)
    else:
        if not GPIO.input(SENSOR_DOOR):
            GPIO.output(LED_DOOR, GPIO.HIGH)



# def door_closed(pin):
#     """Turn on the LED_DOOR and closed the door."""
#     GPIO.output(LED_DOOR, GPIO.HIGH)
#     GPIO.output(ACTUATOR_DOOR, GPIO.HIGH)


# def door_opened(pin):
#     """Turn off the LED_DOOR."""
#     GPIO.output(LED_DOOR, GPIO.LOW)


def toggle_jaw(pin):
    """Open/close the jaw."""
    GPIO.output(ACTUATOR_JAW, not GPIO.input(ACTUATOR_JAW))


def toggle_led_door(pin):
    """Turn on/off the LED_DOOR."""
    # GPIO.output(LED_DOOR, not GPIO.input(LED_DOOR))

    if not GPIO.input(SENSOR_DOOR):
        GPIO.output(LED_DOOR, GPIO.HIGH)
    else:
        GPIO.output(LED_DOOR, GPIO.LOW)


def toggle_emergency(pin):
    """Emergency"""
    if not GPIO.input(BTN_EMERGENCY):
        Screen.navigation('EmergencyStop')
    else:
        Screen.navigation('ProgramsList')


# --- Add events ---

def add_events():
    GPIO.add_event_detect(BTN_DOOR, GPIO.BOTH, callback=open_door, bouncetime=500)

    GPIO.add_event_detect(SENSOR_DOOR, GPIO.BOTH, callback=toggle_led_door, bouncetime=100)

    GPIO.add_event_detect(BTN_EMERGENCY, GPIO.BOTH, callback=toggle_emergency, bouncetime=500)

    GPIO.add_event_detect(SENSOR_PEDAL, GPIO.RISING, callback=toggle_jaw, bouncetime=100)
