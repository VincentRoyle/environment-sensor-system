# Setup Environment

## Purpose
This stage covers setting up the development environment for the Raspberry Pi Pico W, installing required software, and verifying that the board can run code successfully.

---

## Hardware Used
- Raspberry Pi Pico W  
- USB-C to USB-A cable (data capable)

---

## Software Used
- Thonny IDE – v4.1.4  
- MicroPython Firmware – v1.22.2 (Raspberry Pi Pico W build)  
- Windows 10

---

## Steps Performed
1. Installed **Thonny IDE** from [thonny.org](https://thonny.org).  
2. Flashed the **MicroPython UF2 firmware** to the Pico W using **BOOTSEL mode**.  
3. Connected the Pico W in Thonny using the **MicroPython (Raspberry Pi Pico)** interpreter.  
4. Ran a **blink test** to verify the onboard LED could be controlled.

---

## Blink Test Code
```python
from machine import Pin
import time

led = Pin("LED", Pin.OUT)  # Pico W onboard LED

while True:
    led.value(1)       # LED on
    time.sleep(0.5)    # wait 0.5 seconds
    led.value(0)       # LED off
    time.sleep(0.5)    # wait 0.5 seconds
