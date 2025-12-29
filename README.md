# Automation & Scripting Project

This project demonstrates the setup, programming, and integration of hardware components using the **Raspberry Pi Pico W**.  
It is part of my T Level IT coursework and focuses on developing practical automation and scripting skills through hands-on testing, coding, and component integration.

---
# Environment Sensor System

This project is a Raspberry Pi Pico W–based environment monitoring system developed as part of a T Level IT Automation & Scripting assignment.

The system was built incrementally, starting with development environment setup and board verification, followed by sensor integration. Further extensions (such as display output) were attempted and evaluated.

## Hardware Used
- Raspberry Pi Pico W
- DHT22 Temperature & Humidity Sensor
- Breadboard
- Jumper wires
- USB cable

## Software Used
- Thonny IDE
- MicroPython (Pico W firmware)

## Project Structure
- `setup_environment/` – initial setup and board verification
- `sensor_input/` – sensor integration and testing
- `display_output/` – display integration (experimental / future work)


## Project Overview

The project begins with setting up the development environment and verifying that the Pico W can be programmed successfully.  
After confirming the board works, additional stages will introduce sensors for input and a display for output.  
By the end, the Pico W will read environmental data, process it, and present the results visually.

---

## Setup & Initial Verification

To start, I installed **Thonny IDE** (v4.1.4) and flashed the **MicroPython v1.22.2** firmware to the Pico W.  
Using the default “blink” program, I verified that code could be uploaded and executed successfully.

### Blink Test Code
```python
from machine import Pin
import time

led = Pin("LED", Pin.OUT)

while True:
    led.value(1)
    time.sleep(0.5)
    led.value(0)
    time.sleep(0.5)
