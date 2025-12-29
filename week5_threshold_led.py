"""
Week 5 — Add Threshold Logic

Rule:
- If temperature (C) > THRESHOLD_C -> LED ON
- Else -> LED OFF

Threshold is configurable via THRESHOLD_C.
"""

from machine import Pin
import dht
import time

# --- Config ---
THRESHOLD_C = 25.0          # change this to your setpoint
SENSOR_GPIO = 22            # change if your DHT data pin is different
READ_DELAY_S = 2

# --- Hardware ---
sensor = dht.DHT22(Pin(SENSOR_GPIO))
led = Pin("LED", Pin.OUT)   # on-board LED on Pico W

time.sleep(2)  # allow sensor to stabilise

while True:
    try:
        sensor.measure()
        temp_c = sensor.temperature()
        hum = sensor.humidity()

        # --- Threshold logic ---
        if temp_c > THRESHOLD_C:
            led.value(1)
            state = "ALERT (LED ON)"
        else:
            led.value(0)
            state = "OK (LED OFF)"

        print(f"Temp: {temp_c:.1f} C | Hum: {hum:.1f} % | Threshold: {THRESHOLD_C:.1f} C | {state}")

    except OSError as e:
        led.value(0)  # fail safe
        print("Sensor read failed:", e)

    time.sleep(READ_DELAY_S)
