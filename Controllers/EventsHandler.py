import RPi.GPIO as GPIO
from PyQt5.QtCore import pyqtSignal

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

def open_door(pin):
    """Close the door if the door is still closed."""
    if not GPIO.input(BTN_DOOR):
        GPIO.output(LED_DOOR, GPIO.LOW)
    else:
        if not GPIO.input(SENSOR_DOOR):
            GPIO.output(LED_DOOR, GPIO.HIGH)


def toggle_led_door(pin):
    """Turn on/off the LED_DOOR."""
    if not GPIO.input(SENSOR_DOOR):
        GPIO.output(LED_DOOR, GPIO.HIGH)
    else:
        GPIO.output(LED_DOOR, GPIO.LOW)


def toggle_jaw(pin):
    """Open/close the jaw."""
    GPIO.output(ACTUATOR_JAW, not GPIO.input(ACTUATOR_JAW))


# --- Add events ---

def initial_events():
    open_door(BTN_DOOR)
    toggle_led_door(SENSOR_DOOR)
    toggle_jaw(SENSOR_PEDAL)


def add_events():
    GPIO.add_event_detect(BTN_DOOR, GPIO.BOTH, callback=open_door)
    GPIO.add_event_detect(SENSOR_DOOR, GPIO.BOTH, callback=toggle_led_door, bouncetime=10)
    GPIO.add_event_detect(SENSOR_PEDAL, GPIO.RISING, callback=toggle_jaw, bouncetime=100)
