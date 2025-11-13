from machine import Pin
import time

led = Pin("LED", Pin.OUT)  # onboard LED

while True:
    led.value(1)       # LED on
    time.sleep(0.1)    # wait 0.5 seconds
    led.value(0)       # LED off
    time.sleep(0.1)    # wait 0.5 seconds

